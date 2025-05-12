

async function get_user_permissions(){

    const access_token = localStorage.getItem("access_token");
    try {
        // Perform the API call
        const response = await fetch(fetch_user_permissions_url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
            },
            // body: JSON.stringify(data),
        });
        

        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
           
            console.log(data)
           
            // Store permission
            if (data.permissions_data && data.permissions_data.length > 0) {
                const all_permissions_data = JSON.stringify(data.permissions_data);
                localStorage.setItem("all_permissions_data", all_permissions_data);
            }

            // show_toast("success", "Signed in successfully");
            // Calculate the time for 90 minutes later
            const now = new Date().getTime();
            const delayUntil = now + 90 * 60 * 1000; // 90 minutes in milliseconds

            // Function to check when it's time to call get_access_token
            const checkTimeToCall = () => {
                const currentTime = new Date().getTime();
                if (currentTime >= delayUntil) {
                    get_access_token();
                } else {
                    // Call this function again after a short delay (e.g., 1 second) to keep checking
                    setTimeout(checkTimeToCall, 1000); // Check every 1 second
                }
            };

            // Start checking after 1 second (after the current call)
            setTimeout(checkTimeToCall, 1000);

            handle_permissions();

        } else {
            
            const error_data = responseData;

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

document.addEventListener("DOMContentLoaded", function () {
    get_user_permissions();
});
