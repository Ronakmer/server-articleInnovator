


let manager_data = '';
let writer_data = '';
let set_manager_ids = '';
let set_writer_ids = '';



async function add_domain_api() {

    // Get the form element
    const domain_form = document.querySelector('[name="domain_form"]');

    // Collect form data using the name attributes
    const name = domain_form.querySelector('[name="domain_name"]').value;
    wordpress_username = wp_username 
    wordpress_application_password = wp_password 
    
    const data = new FormData();
    data.append("name", name);
    data.append("wordpress_username", wordpress_username);
    data.append("wordpress_application_password", wordpress_application_password);


  
    
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
                    window.location.href = dashboard_page_url;
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


