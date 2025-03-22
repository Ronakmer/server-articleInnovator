
// user_profile_api
async function user_profile_api() {
    try {

        const access_token = localStorage.getItem("access_token");

        const response = await fetch(`${user_profile_url}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('fetched successfully:', data);
            
            const obj = data.user_data;
            set_profile(obj)

            // show_toast("success", "Roles fetched successfully");
        } else {
            const error_data = await response.json();
            console.error('Failed to fetch roles:', error_data);

            const errorMessage = error_data.error || "Something went wrong";
            show_toast("error", `Error: ${errorMessage}`);
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later.");
    }
}



user_profile_api()



function set_profile(data) {
    const user_profile_form = document.querySelector('[name="user_profile_form"]');

    const full_name = user_profile_form.querySelector('[name="full_name"]');
    full_name.value = data.full_name;
}




// update_user_profile_api
async function update_user_profile_api(){

    let temp_avatar_image_id = '';
    if (avatar_image_id){

        temp_avatar_image_id = avatar_image_id.replace('/media/', '');
    }

    const user_profile_form = document.querySelector('[name="user_profile_form"]');

    const full_name = user_profile_form.querySelector('[name="full_name"]').value;
    const password = user_profile_form.querySelector('[name="password"]').value;
    const profile_image = user_profile_form.querySelector('[name="profile_image"]');


    const data = new FormData();
    data.append("full_name", full_name);
    if(password){
        data.append("password", password);
    }
    if(temp_avatar_image_id){
        data.append("avatar_image_path", temp_avatar_image_id);
    }
    if (profile_image && profile_image.files && profile_image.files[0]) {
        data.append('profile_image', profile_image.files[0]);
    }


    const access_token = localStorage.getItem("access_token");

    try {
        // Perform the API call
        const response = await fetch(update_user_profile_url, {
            method: 'PATCH',
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