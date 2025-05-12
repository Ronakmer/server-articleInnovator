

// verify_api 
async function verify_api() {

    const access_token = localStorage.getItem("access_token");
    const private_key = image_kit_configuration_form.querySelector('[name="private_key"]').value;
    const public_key = image_kit_configuration_form.querySelector('[name="public_key"]').value;
    const url_endpoint = image_kit_configuration_form.querySelector('[name="url_endpoint"]').value;


    const data = new FormData();
    data.append("private_key", private_key);
    data.append("public_key", public_key);
    data.append("url_endpoint", url_endpoint);

    const workspace_slug_id = localStorage.getItem("workspace_slug_id");

    if (!data.has("workspace_slug_id")) {
        // data.append("workspace_slug_id", workspace_slug_id);   
        if(workspace_slug_id){
            data.append("workspace_slug_id", workspace_slug_id);
        }
    }

    
    try {
        // Perform the API call
        const response = await fetch(verify_image_kit_configuration_url, {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,

            },
            body: data,
        });
        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
           
            console.log(data)
            if (response.ok) {
                console.log("API Response:", data);
                show_toast("success", "API verified successfully");
            } else {
                console.error("API Verification Failed:", data);
                const error_message = error_message_data(data);
                show_toast("error", `Error: ${error_message}`);
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


