

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
            // console.log('Login successful:', data);
           
            // Store tokens securely
            const access_token = data.access_token;
            const refresh_token = data.refresh_token;

            if (access_token && refresh_token) {
                // localStorage.setItem("access_token", access_token);
                // localStorage.setItem("refresh_token", refresh_token);
                sessionStorage.setItem("access_token", access_token);
                sessionStorage.setItem("refresh_token", refresh_token);
                
            }

            // Store workspce
            if (data.workspaces_data && data.workspaces_data.length > 0) {
                const first_workspace_slug_id = data.workspaces_data[1].slug_id;
                const all_workspace_slug_id = JSON.stringify(data.workspaces_data);
                // console.log("all_workspace_slug_id:", all_workspace_slug_id);
                // console.log("First workspace slug_id:", first_workspace_slug_id);
                // sessionStorage.setItem("workspace_slug_id", first_workspace_slug_id);
                sessionStorage.setItem("all_workspace_slug_id", all_workspace_slug_id);
            }

            show_toast("success", "Signed in successfully");

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

