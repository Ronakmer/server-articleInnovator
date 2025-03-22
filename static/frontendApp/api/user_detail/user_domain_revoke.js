

// domain revoke api 
async function user_domain_revoke_api(domain_slug_id, role_type) {

    const access_token = localStorage.getItem("access_token");

    const temp_url = new URL(window.location.href);
    const pathname = temp_url.pathname; 
    const slug_id = pathname.split('/').pop();

    const workspace_slug_id = localStorage.getItem("workspace_slug_id");

    const data = {
        'workspace_slug_id': workspace_slug_id,
        'domain_slug_id': domain_slug_id,
        'role_type': role_type,
    };

    try {

        const api_url = `${user_domain_revoke_url}${slug_id}`

        // Perform the API call
        const response = await fetch(`${api_url}`, {
            method: 'POST',
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
                    window.location.reload();
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



















// user add  api 
async function user_domain_add_api() {

    const access_token = localStorage.getItem("access_token");

    const temp_url = new URL(window.location.href);
    const pathname = temp_url.pathname; 
    const slug_id = pathname.split('/').pop();

    const workspace_slug_id = document.querySelector('[name="new_workspace_id"]').value;
    const domain_slug_id = document.querySelector('[name="new_domain_id"]').value;
    
    let role_type = '';
    const selected_radio = document.querySelector('input[name="user_type_radio"]:checked');
    if (selected_radio) {
        role_type =  selected_radio.value;  // Returns the value of the selected radio button (either "manager" or "writer")
    } 
    
    const data = {
        'workspace_slug_id': workspace_slug_id,
        'domain_slug_id': domain_slug_id,
        'slug_id': slug_id,
        'role_type': role_type,
    };
    try {

        // Perform the API call
        const response = await fetch(user_domain_add_url, {
            method: 'POST',
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
                    window.location.reload();
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



