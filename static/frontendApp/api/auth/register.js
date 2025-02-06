// register


async function check_invitation_code_api(){
    
    const access_token = sessionStorage.getItem("access_token");

    const invitation_code = document.querySelector('[name="invitation_code"]').value;
    const data = new FormData();
    data.append("invitation_code", invitation_code);

    try {
        // Perform the API call
        const response = await fetch(check_invitation_code_url, {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json',
                // 'Authorization': `Bearer ${access_token}`,

            },
            // body: JSON.stringify(data),
            body: data,
        });
        

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
           
            console.log(data)
            show_toast("success", `${data.message}`);

            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    step_2()
                }, 1000);
            }

        } else {
            
            const error_data = await response.json();

            console.log(error_data)
            // Show api error
            var error_message = error_message_data(error_data);
            

            // Show the toast
            show_toast("error", `Error: ${error_message}`);
        
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("Network error. Please try again later");
    }
}








// admin_registration
async function admin_registration_api(){
    
    // const access_token = sessionStorage.getItem("access_token");

    const invitation_code = document.querySelector('[name="invitation_code"]').value;
    const full_name = document.querySelector('[name="full_name"]').value;
    const email = document.querySelector('[name="registration_email"]').value;
    const password = document.querySelector('[name="registration_password"]').value;

    const data = {
        invitation_code: invitation_code,
        full_name: full_name,
        email: email,
        password: password,
    };
    
    
    sessionStorage.setItem("registration_email", email);

    try {
        const response = await fetch(admin_registration_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 'Authorization': `Bearer ${access_token}`,
            },
            body: JSON.stringify(data),
            // body: data,
        });
        

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
           
            console.log(data)
            show_toast("success", `${data.message}`);

            // Redirect or show a success message
            alert(data)
            if (response.ok) {
                setTimeout(() => {
                    window.location.href = registration_enter_otp_page;
                }, 1000);
            }

        } else {
            
            const error_data = await response.json();

            console.log(error_data)
            // Show api error
            var error_message = error_message_data(error_data);
            

            // Show the toast
            show_toast("error", `Error: ${error_message}`);
        
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("Network error. Please try again later");
    }
}







// verify_otp
async function verify_otp_api(){
    
    // const access_token = sessionStorage.getItem("access_token");

    const registration_email = sessionStorage.getItem("registration_email");
    const verify_form = document.querySelector('#verify_form');

    const otp = [
        verify_form.querySelector('[id="otp-1"]').value,
        verify_form.querySelector('[id="otp-2"]').value,
        verify_form.querySelector('[id="otp-3"]').value,
        verify_form.querySelector('[id="otp-4"]').value
    ].join(''); 
        
    alert(registration_email)


    const data = {
        email: registration_email,
        otp: otp, 
    };
    
    try {
        const response = await fetch(registration_check_otp, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 'Authorization': `Bearer ${access_token}`,
            },
            body: JSON.stringify(data),
            // body: data,
        });
        

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
           
            console.log(data)
            show_toast("success", `${data.message}`);

            // Redirect or show a success message
            alert(data)
            if (response.ok) {
                setTimeout(() => {
                    window.location.href = page_url;
                }, 1000);
            }

        } else {
            
            const error_data = await response.json();

            console.log(error_data)
            // Show api error
            var error_message = error_message_data(error_data);
            

            // Show the toast
            show_toast("error", `Error: ${error_message}`);
        
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("Network error. Please try again later");
    }
}




