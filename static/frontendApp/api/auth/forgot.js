


//  forgot
async function forgot_api() {
    // Get the form element
    const forgot_form = document.querySelector('form');

    // Collect form data using the name attributes
    const email = forgot_form.querySelector('[name="login_email"]').value;

    
    // Prepare the data object
    const data = {
        email: email,
    };
    try {
        // Perform the API call
        const response = await fetch(forgot_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('Login successful:', data);
           
            show_toast("success", "otp send successfully");

            // Set email and expiration time in sessionStorage
            const expirationTime = Date.now() + 15 * 60 * 1000; // 15 minutes from now
            localStorage.setItem("email", email);
            localStorage.setItem("email_expiration", expirationTime);

            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    window.location.href = otp_page_url;
                }, 1000);
            }

        } else {
            const error_data = await response.json();
            console.error('Login failed:', error_data);
        
            // Check if error_data contains a message field and display it
            const errorMessage = error_data.error || "Something went wrong";
        
            // Show the error toast with the error message
            show_toast("error", `Error: ${errorMessage}`);
        
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("Network error. Please try again later");
    }
}






// otp
async function otp_api() {
    // Get the form element
    const forgot_form = document.querySelector('#otp_form');

    const otp = [
        forgot_form.querySelector('[id="otp-1"]').value,
        forgot_form.querySelector('[id="otp-2"]').value,
        forgot_form.querySelector('[id="otp-3"]').value,
        forgot_form.querySelector('[id="otp-4"]').value
    ].join(''); // Concatenate OTP values
        
    const user_email = localStorage.getItem("email");


    // Prepare the data object
    const data = {
        otp: otp,
        user_email : user_email,
    };

    try {
        // Perform the API call
        const response = await fetch(otp_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            // Handle successful response
            const response_data = await response.json();
            console.log('OTP sent successfully:', response_data);

            // Set otp and expiration time in sessionStorage
            const expirationTime = Date.now() + 15 * 60 * 1000; // 15 minutes from now
            localStorage.setItem("otp", otp);
            localStorage.setItem("email_expiration", expirationTime);
            

            // Show success toast
            show_toast("success", "OTP sent successfully");

            // Redirect to OTP page after a delay
            setTimeout(() => {
                window.location.href = new_password_page_url;
            }, 1000);

        } else {
            // Handle errors
            const error_data = await response.json();
            console.error('OTP request failed:', error_data);

            // Display error message
            const error_message = error_data.error || "Something went wrong";
            show_toast("error", `Error: ${error_message}`);
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later");
    }
}





//  resend otp api
async function resend_otp_api() {

    const user_email = localStorage.getItem("email");

    
    // Prepare the data object
    const data = {
        email: user_email,
    };
    try {
        // Perform the API call
        const response = await fetch(forgot_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('Login successful:', data);
           
            show_toast("success", "otp send successfully");

            
        } else {
            const error_data = await response.json();
            console.error('Login failed:', error_data);
        
            // Check if error_data contains a message field and display it
            const errorMessage = error_data.error || "Something went wrong";
        
            // Show the error toast with the error message
            show_toast("error", `Error: ${errorMessage}`);
        
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("Network error. Please try again later");
    }
}





//  set new password api
async function new_password_api() {

    const new_password_form = document.querySelector('form');
    const new_password = new_password_form.querySelector('[name="new_password"]').value;
    const confirm_password = new_password_form.querySelector('[name="confirm_password"]').value;
    
    const otp = localStorage.getItem("otp");
    const user_email = localStorage.getItem("email");


    
    // Prepare the data object
    const data = {
        new_password : new_password,
        confirm_password : confirm_password,
        email : user_email,
        otp : otp,
    };
    try {
        // Perform the API call
        const response = await fetch(new_password_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('Login successful:', data);
           
            show_toast("success", "otp send successfully");

            
        } else {
            const error_data = await response.json();
            console.error('Login failed:', error_data);
        
            // Check if error_data contains a message field and display it
            const errorMessage = error_data.error || "Something went wrong";
        
            // Show the error toast with the error message
            show_toast("error", `Error: ${errorMessage}`);
        
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("Network error. Please try again later");
    }
}
