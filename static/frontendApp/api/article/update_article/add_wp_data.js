
function add_category_api(){

    // Get the form element
    const category_form = document.querySelector('[name="category_form"]');

    // Collect form data using the name attributes
    const name = category_form.querySelector('[name="name"]').value;
    const slug = category_form.querySelector('[name="slug"]').value;
    const description = category_form.querySelector('[name="description"]').value;
    const category_wp_id = category_form.querySelector('[name="wp_cat_id"]').value;
    const category_slug_id = category_form.querySelector('[name="category_slug_id"]').value;
    // const domain_slug_id = current_page_url.split('/').pop();
    const set_manual_domain_slug_id = document.querySelector('[name="manual_domain_slug_id"]');

    const domain_slug_id = set_manual_domain_slug_id.value.trim();

    
    const data = new FormData();
    data.append("name", name);
    data.append("slug", slug);
    data.append("description", description);
    data.append("domain_slug_id", domain_slug_id);
    data.append("category_wp_id", category_wp_id);
    data.append("name", name);
    
    // const dropdown_function_name = ''
    (async ()=>{ 
        await add_wp_data_api(add_category_url, data, '');
    })()
    

}





function add_tag_api() {
    
    // Get the form element
    const tag_form = document.querySelector('[name="tag_form"]');
    
    // Collect form data using the name attributes
    const name = tag_form.querySelector('[name="name"]').value;
    const slug = tag_form.querySelector('[name="slug"]').value;
    const description = tag_form.querySelector('[name="description"]').value;
    const tag_wp_id = tag_form.querySelector('[name="wp_tag_id"]').value;
    const tag_slug_id = tag_form.querySelector('[name="tag_slug_id"]').value;
    // const domain_slug_id = current_page_url.split('/').pop();
    const set_manual_domain_slug_id = document.querySelector('[name="manual_domain_slug_id"]');

    const domain_slug_id = set_manual_domain_slug_id.value.trim();

    
    const data = new FormData();
    data.append("name", name);
    data.append("slug", slug);
    data.append("description", description);
    data.append("domain_slug_id", domain_slug_id);
    data.append("tag_wp_id", tag_wp_id);
    data.append("name", name);

    (async ()=>{ 
        await add_wp_data_api(add_tag_url, data, '');
    })()

}





function add_author_api() {

    // const current_page_url = window.location.href;
    
    
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
    // const domain_slug_id = current_page_url.split('/').pop();
    const set_manual_domain_slug_id = document.querySelector('[name="manual_domain_slug_id"]');

    const domain_slug_id = set_manual_domain_slug_id.value.trim();

    
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

    
    (async ()=>{ 
        await add_wp_data_api(add_author_url, data, '');
    })()

}
