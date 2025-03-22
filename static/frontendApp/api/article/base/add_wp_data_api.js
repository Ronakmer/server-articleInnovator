

// add_wp_data_api api 
async function add_wp_data_api(api_url, data, redirect_url) {

    const access_token = localStorage.getItem("access_token");

    // const workspace_slug_id = localStorage.getItem("workspace_slug_id");
    const workspace_slug_id = '77b4ad49-db8a-4434-aad5-c2351c953cc7';

    data.append("workspace_slug_id", workspace_slug_id);


    try {
        // Perform the API call
        const response = await fetch(api_url, {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,

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
                    domain_slug_value()
                    const closeModalButton = document.querySelector('.close-modal');
                    if (closeModalButton) {
                        closeModalButton.click();
                    }                    
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


