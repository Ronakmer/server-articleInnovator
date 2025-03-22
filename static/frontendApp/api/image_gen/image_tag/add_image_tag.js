

function add_image_tag_api() {

    // Get the form element
    const image_tag_form = document.querySelector('[name="image_tag_form"]');

    // Collect form data using the name attributes
    const name = image_tag_form.querySelector('[name="name"]').value;
    const workspace_slug_id = localStorage.getItem("workspace_slug_id");

    const data = new FormData();
    data.append("name", name);
    data.append("workspace_slug_id", workspace_slug_id);


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_image_tag_url, data, slug_id, list_image_tag_page_url);
        } else {
            await add_api(add_image_tag_url, data, list_image_tag_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_image_tag_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const image_tag_form = document.querySelector('[name="image_tag_form"]');

        // Collect form data using the name attributes
        const name = image_tag_form.querySelector('[name="name"]');

        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            name.value = data_obj.data[0].name;
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     

