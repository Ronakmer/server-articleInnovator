

async function add_ai_configuration_api() {

    // Get the form element
    const ai_configuration_form = document.querySelector('[name="ai_configuration_form"]');

    // Collect form data using the name attributes
    const api_provider = ai_configuration_form.querySelector('[name="api_provider"]').value;
    const api_type = ai_configuration_form.querySelector('[name="api_type"]').value;
    const api_version = ai_configuration_form.querySelector('[name="api_version"]').value;
    const api_key = ai_configuration_form.querySelector('[name="api_key"]').value;
    const api_model = ai_configuration_form.querySelector('[name="api_model"]').value;
    const api_url = ai_configuration_form.querySelector('[name="api_url"]').value;
    const email = ai_configuration_form.querySelector('[name="email"]').value;

    const data = new FormData();
    data.append("api_provider", api_provider);
    data.append("api_type", api_type);
    data.append("api_version", api_version);
    data.append("api_key", api_key);
    data.append("api_model", api_model);
    data.append("api_url", api_url);
    data.append("email", email);
    
    try {
        const access_token = sessionStorage.getItem("access_token");
        const onboard_workspace_slug_id = sessionStorage.getItem("onboard_workspace_slug_id");
        
        
        if(onboard_workspace_slug_id){
            data.append("workspace_slug_id", onboard_workspace_slug_id);
        }

        // Perform the API call
        const response = await fetch(add_ai_configuration_url, {
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
                    nextStep()
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

