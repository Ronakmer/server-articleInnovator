

function add_tag_api() {

    const current_page_url = window.location.href;
    
    
    // Get the form element
    const tag_form = document.querySelector('[name="tag_form"]');
    
    // Collect form data using the name attributes
    const name = tag_form.querySelector('[name="name"]').value;
    const slug = tag_form.querySelector('[name="slug"]').value;
    const description = tag_form.querySelector('[name="description"]').value;
    const tag_wp_id = tag_form.querySelector('[name="wp_tag_id"]').value;
    const tag_slug_id = tag_form.querySelector('[name="tag_slug_id"]').value;
    const domain_slug_id = current_page_url.split('/').pop();

    
    const data = new FormData();
    data.append("name", name);
    data.append("slug", slug);
    data.append("description", description);
    data.append("domain_slug_id", domain_slug_id);
    data.append("tag_wp_id", tag_wp_id);
    data.append("name", name);
    data.append("derived_by", 'user');

    
    (async ()=>{ 

        if(tag_slug_id){
            await update_api(update_tag_url, data, tag_slug_id, current_page_url);
        }else{
            await add_api(add_tag_url, data, current_page_url);

        }
    })()
    

}

