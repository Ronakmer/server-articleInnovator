

async function add_workspace_api() {
    
    // Get the form element
    const workspace_form = document.querySelector('[name="workspace_form"]');

    let temp_avatar_image_id = '';
    if (avatar_image_id){

        temp_avatar_image_id = avatar_image_id.replace('/media/', '');
    }

    // Collect form data using the name attributes
    const name = workspace_form.querySelector('[name="name"]').value;
    const logo = workspace_form.querySelector('[name="logo"]');

    const data = new FormData();
    data.append("name", name);
    if(temp_avatar_image_id){

        data.append("avatar_image_path", temp_avatar_image_id);
    }

    if (logo && logo.files && logo.files[0]) {
        data.append('logo', logo.files[0]);
    }


    try {
        const access_token = sessionStorage.getItem("access_token");

        // Perform the API call
        const response = await fetch(add_workspace_url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${access_token}`,

            },
            body: data,
        });
        

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
           
            console.log(data)
            const temo_slug_id = data.workspace.slug_id
            alert(temo_slug_id)
            sessionStorage.setItem("onboard_workspace_slug_id", temo_slug_id);

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



     

