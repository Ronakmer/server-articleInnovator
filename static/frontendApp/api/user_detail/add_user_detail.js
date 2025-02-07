

let set_workspace_ids = [];

async function add_user_detail_api() {

    // Get the form element
    const user_detail_form = document.querySelector('[name="user_detail_form"]');

    let temp_avatar_image_id = '';
    if (avatar_image_id){

        temp_avatar_image_id = avatar_image_id.replace('/media/', '');
    }

    // Collect form data using the name attributes
    const full_name = user_detail_form.querySelector('[name="full_name"]').value;
    const email = user_detail_form.querySelector('[name="email"]').value;
    const password = user_detail_form.querySelector('[name="password"]').value;
    const workspace_slug_id = user_detail_form.querySelector('[name="workspace_id"]').value;
    const profile_image = user_detail_form.querySelector('[name="profile_image"]');


    const data = new FormData();
    data.append("full_name", full_name);
    data.append("email", email);
    data.append("password", password);
    data.append("workspace_slug_id", workspace_slug_id);

    if (profile_image && profile_image.files && profile_image.files[0]) {
        data.append('profile_image', profile_image.files[0]);
    }

    if(temp_avatar_image_id){

        data.append("avatar_image_path", temp_avatar_image_id);
    }


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_user_detail_url, data, slug_id, list_user_detail_page_url);
        } else {
            await add_api(add_user_detail_url, data, list_user_detail_page_url);
        }
    })()

}



(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_user_detail_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const user_detail_form = document.querySelector('[name="user_detail_form"]');

        // Collect form data using the name attributes
        const full_name = user_detail_form.querySelector('[name="full_name"]');
        const email = user_detail_form.querySelector('[name="email"]');
        const password = user_detail_form.querySelector('[name="password"]');
        const workspace_id = user_detail_form.querySelector('[name="workspace_id"]');
            
        if (data_obj && data_obj.user_details && data_obj.user_details.length > 0) {
            full_name.value = data_obj.user_details[0].full_name;
            email.value = data_obj.user_details[0].user_id.email;
            password.value = data_obj.user_details[0].password;

            set_workspace_ids = data_obj.user_details[0].workspace_id.map(field => field.slug_id).join(', ')

        } else {
            window.location.href = error_page;
        }
        
    }
})()
     


function get_workspace_data(){

    workspace_data = get_data_api(list_workspace_url)
}
get_workspace_data()
