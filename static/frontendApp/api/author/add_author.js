

function add_author_api() {

    const current_page_url = window.location.href;
    
    let temp_avatar_image_id = '';
    if (avatar_image_id){
        temp_avatar_image_id = avatar_image_id.replace('/media/', '');
    }
    
    // Get the form element
    const author_form = document.querySelector('[name="author_form"]');
    
    // Collect form data using the name attributes
    const username = author_form.querySelector('[name="username"]').value;
    const password = author_form.querySelector('[name="password"]').value;
    const first_name = author_form.querySelector('[name="first_name"]').value;
    const last_name = author_form.querySelector('[name="last_name"]').value;
    const bio = author_form.querySelector('[name="bio"]').value;
    const email = author_form.querySelector('[name="email"]').value;
    const author_default_section = author_form.querySelector('[name="author_default_section"]').checked;
    const author_wp_id = author_form.querySelector('[name="wp_author_id"]').value;
    const author_slug_id = author_form.querySelector('[name="author_slug_id"]').value;
    const domain_slug_id = current_page_url.split('/').pop();
    const profile_image = author_form.querySelector('[name="profile_image"]');

    
    const data = new FormData();
    data.append("username", username);
    data.append("password", password);
    data.append("first_name", first_name);
    data.append("last_name", last_name);
    data.append("bio", bio);
    data.append("email", email);
    data.append("domain_slug_id", domain_slug_id);
    data.append("author_wp_id", author_wp_id);
    // data.append("name", name);
    data.append("default_section", author_default_section);
    data.append("derived_by", 'user');
    
    if (profile_image && profile_image.files && profile_image.files[0]) {
        data.append('profile_image', profile_image.files[0]);
    }

    if(temp_avatar_image_id){

        data.append("avatar_image_path", temp_avatar_image_id);
    }
    
    (async ()=>{ 

        if(author_slug_id){
            await update_api(update_author_url, data, author_slug_id, current_page_url);
        }else{
            await add_api(add_author_url, data, current_page_url);

        }
    })()
    

}

