
// logout api 

async function logout_api() {

    try {
        // Perform the API call
        const response = await fetch(logout_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            
            // Clear all local storage
            localStorage.clear();

            show_toast("success", `${data.message}`);
            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    window.location.href = login_page_url;
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

