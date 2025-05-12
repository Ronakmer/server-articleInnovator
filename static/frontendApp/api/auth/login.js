


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
            get_user_workspce();
        
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















