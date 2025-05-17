

// user revoke api 
async function user_workspace_revoke_api(workspace_slug_id) {

    const access_token = localStorage.getItem("access_token");

    const temp_url = new URL(window.location.href);
    const pathname = temp_url.pathname; 
    const slug_id = pathname.split('/').pop();

    const data = {
        'workspace_slug_id': workspace_slug_id,
    };
    try {

        const api_url = `${user_workspace_revoke_url}${slug_id}`

        // Perform the API call
        const response = await fetch(api_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,

            },
            body: JSON.stringify(data),
        });
        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
           
            console.log(data)
            show_toast("success", `${data.message}`);

            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            }
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









// user add  api 
async function user_workspace_add_api() {

    const access_token = localStorage.getItem("access_token");

    const temp_url = new URL(window.location.href);
    const pathname = temp_url.pathname; 
    const slug_id = pathname.split('/').pop();

    const workspace_slug_id = document.querySelector('[name="workspace_id"]').value;

    const data = {
        'workspace_slug_id': workspace_slug_id,
        'slug_id': slug_id,
    };
    try {

        // Perform the API call
        const response = await fetch(user_workspace_add_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,

            },
            body: JSON.stringify(data),
        });
        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
           
            console.log(data)
            show_toast("success", `${data.message}`);

            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            }
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


