


// login api 

async function login_api() {
    // Get the form element
    const login_form = document.querySelector('form');

    // Collect form data using the name attributes
    const email = login_form.querySelector('[name="login_email"]').value;
    const password = login_form.querySelector('[name="login_password"]').value;

    // Prepare the data object
    const data = {
        email: email,
        password: password,
    };

    try {
        // Perform the API call
        const response = await fetch(login_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
           
            // Store tokens securely
            const access_token = data.access_token;
            const refresh_token = data.refresh_token;
            const user_email = data.email;
            console.log(refresh_token,'refresh_token')
            if (access_token && refresh_token) {
                localStorage.setItem("access_token", access_token);
                localStorage.setItem("refresh_token", refresh_token);
            }
           
            
            show_toast("success", "Signed in successfully");
            setTimeout(get_access_token, 6300000);
            get_user_workspce(data.email)

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














async function get_user_workspce(email){

    const access_token = localStorage.getItem("access_token");
    // const user_email = localStorage.getItem("user_email");
    // Prepare the data object
    const data = {
        // email: user_email,
        email: email,
    };

    try {
        // Perform the API call
        const response = await fetch(fetch_user_workspaces_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
            },
            body: JSON.stringify(data),
        });
        

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
           
            console.log(data)
           
            // Store workspce
            if (data.workspaces_data && data.workspaces_data.length > 0) {
                const all_workspace_slug_id = JSON.stringify(data.workspaces_data);
                localStorage.setItem("all_workspace_slug_id", all_workspace_slug_id);
            }

            // Store permission
            if (data.permissions_data && data.permissions_data.length > 0) {
                const all_permissions_data = JSON.stringify(data.permissions_data);
                localStorage.setItem("all_permissions_data", all_permissions_data);
            }

            // show_toast("success", "Signed in successfully");
            setTimeout(get_access_token, 6300000);

            if(data.workspaces_status == false){

                // Redirect or show a success message
                if (response.ok) {
                    setTimeout(() => {
                        window.location.href = onboard_page_url;
                    }, 1000);
                }
            }else{
                // Redirect or show a success message
                if (response.ok) {
                    setTimeout(() => {
                        window.location.href = dashboard_page_url;
                    }, 1000);
                }
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
