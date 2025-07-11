

// verify_api 
async function verify_api() {

    const access_token = localStorage.getItem("access_token");
    const api_key = ai_configuration_form.querySelector('[name="api_key"]').value;
    const api_provider = ai_configuration_form.querySelector('[name="api_provider"]').value;
    const api_model = ai_configuration_form.querySelector('[name="api_model"]').value;
    const api_version = ai_configuration_form.querySelector('[name="api_version"]').value;
    const api_url = ai_configuration_form.querySelector('[name="api_url"]').value;


    const data = new FormData();
    data.append("api_provider", api_provider);
    data.append("api_version", api_version);
    data.append("api_key", api_key);
    data.append("api_model", api_model);
    data.append("api_url", api_url);

    try {
        // Perform the API call
        const response = await fetch(verify_ai_configuration_url, {
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
            // if(data.message == true){
            //     show_toast("success", `API verified successfully`);
            // }else{
            //     show_toast("error", `API verification failed`);
            // }


            if (!data.failed_models || data.failed_models.length === 0) {
                show_toast("success", "API verified successfully");
                const save_btn = ai_configuration_form.querySelector('[id="save_btn"]');
                if (save_btn) {
                    save_btn.classList.remove("hidden");
                }

            } else {
                let errorMessage = "API verification failed.";
                if (data.failed_models && data.failed_models.length > 0) {
                    errorMessage += ` Failed models: ${data.failed_models.join(", ")}.`;
                }
                show_toast("error", errorMessage);
            }


            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    //window.location.href = redirect_url;
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


