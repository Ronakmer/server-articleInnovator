

function add_author_api() {

    const current_page_url = window.location.href;
    
    
    // Get the form element
    const author_form = document.querySelector('[name="author_form"]');
    
    // Collect form data using the name attributes
    const username = author_form.querySelector('[name="username"]').value;
    const password = author_form.querySelector('[name="password"]').value;
    const first_name = author_form.querySelector('[name="first_name"]').value;
    const last_name = author_form.querySelector('[name="last_name"]').value;
    const bio = author_form.querySelector('[name="bio"]').value;
    const email = author_form.querySelector('[name="email"]').value;
    const author_wp_id = author_form.querySelector('[name="wp_author_id"]').value;
    const author_slug_id = author_form.querySelector('[name="author_slug_id"]').value;
    const domain_slug_id = current_page_url.split('/').pop();

    
    const data = new FormData();
    data.append("username", username);
    data.append("password", password);
    data.append("first_name", first_name);
    data.append("last_name", last_name);
    data.append("bio", bio);
    data.append("email", email);
    data.append("domain_slug_id", domain_slug_id);
    data.append("author_wp_id", author_wp_id);
    data.append("name", name);
    data.append("derived_by", 'user');

    
    (async ()=>{ 

        if(author_slug_id){
            await update_api(update_author_url, data, author_slug_id, current_page_url);
        }else{
            await add_api(add_author_url, data, current_page_url);

        }
    })()
    

}

