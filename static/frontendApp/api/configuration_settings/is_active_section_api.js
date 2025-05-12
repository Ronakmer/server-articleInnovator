
// default_section api 
async function is_active_section_api(slug_id, is_checked) {

    const access_token = localStorage.getItem("access_token");

    const temp_api_url = `${update_configuration_settings_url}${slug_id}`;

    const data = {
        is_active: is_checked,
    };


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



