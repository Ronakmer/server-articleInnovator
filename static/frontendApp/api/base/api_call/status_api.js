


// status api 
async function status_api(api_url, data, slug_id, redirect_url) {

    const access_token = localStorage.getItem("access_token");

    const temp_api_url = `${api_url}${slug_id}`;

    const workspace_slug_id = localStorage.getItem("workspace_slug_id");
    if(workspace_slug_id){
        data["workspace_slug_id"] = workspace_slug_id; 
    }

    try {
        // Perform the API call
        const response = await fetch(temp_api_url, {
            // method: 'PUT',
            method: 'PATCH',
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
            show_toast("success", `${data.message}`);

            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    // window.location.reload();
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


