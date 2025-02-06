

function add_category_api() {

    const current_page_url = window.location.href;
    
    
    // Get the form element
    const category_form = document.querySelector('[name="category_form"]');
    
    // Collect form data using the name attributes
    const name = category_form.querySelector('[name="name"]').value;
    const slug = category_form.querySelector('[name="slug"]').value;
    const description = category_form.querySelector('[name="description"]').value;
    const category_wp_id = category_form.querySelector('[name="wp_cat_id"]').value;
    const category_slug_id = category_form.querySelector('[name="category_slug_id"]').value;
    const domain_slug_id = current_page_url.split('/').pop();

    
    const data = new FormData();
    data.append("name", name);
    data.append("slug", slug);
    data.append("description", description);
    data.append("domain_slug_id", domain_slug_id);
    data.append("category_wp_id", category_wp_id);
    data.append("name", name);

    
    (async ()=>{ 

        if(category_slug_id){
            await update_api(update_category_url, data, category_slug_id, current_page_url);
        }else{
            await add_api(add_category_url, data, current_page_url);

        }
    })()
    

}

