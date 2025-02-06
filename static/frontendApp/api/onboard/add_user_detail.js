

let set_workspace_ids = [];

async function add_user_detail_api() {

    let temp_avatar_image_id = '';
    if (user_avatar_image_id){

        temp_avatar_image_id = user_avatar_image_id.replace('/media/', '');
    }


    // Get the form element
    const user_detail_form = document.querySelector('[name="user_detail_form"]');

    // Collect form data using the name attributes
    const full_name = user_detail_form.querySelector('[name="full_name"]').value;
    const email = user_detail_form.querySelector('[name="email"]').value;
    const password = user_detail_form.querySelector('[name="password"]').value;
    // const workspace_slug_id = user_detail_form.querySelector('[name="workspace_id"]').value;
    const profile_image = user_detail_form.querySelector('[name="profile_image"]');

    const data = new FormData();
    data.append("full_name", full_name);
    data.append("email", email);
    data.append("password", password);
    // data.append("workspace_slug_id", workspace_slug_id);

    if(temp_avatar_image_id){
        data.append("avatar_image_path", temp_avatar_image_id);
    }



    if (profile_image && profile_image.files && profile_image.files[0]) {
        data.append('profile_image', profile_image.files[0]);
    }


    
    try {
        const access_token = sessionStorage.getItem("access_token");
        const onboard_workspace_slug_id = sessionStorage.getItem("onboard_workspace_slug_id");
        
        
        if(onboard_workspace_slug_id){
            data.append("workspace_slug_id", onboard_workspace_slug_id);
        }

        // Perform the API call
        const response = await fetch(add_user_detail_url, {
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

