

function add_image_kit_configuration_api() {

    // Get the form element
    const image_kit_configuration_form = document.querySelector('[name="image_kit_configuration_form"]');

    // Collect form data using the name attributes
    const public_key = image_kit_configuration_form.querySelector('[name="public_key"]').value;
    const private_key = image_kit_configuration_form.querySelector('[name="private_key"]').value;
    const url_endpoint = image_kit_configuration_form.querySelector('[name="url_endpoint"]').value;

    const data = new FormData();
    data.append("public_key", public_key);
    data.append("private_key", private_key);
    data.append("url_endpoint", url_endpoint);


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_image_kit_configuration_url, data, slug_id, list_image_kit_configuration_page_url);
        } else {
            await add_api(add_image_kit_configuration_url, data, list_image_kit_configuration_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_image_kit_configuration_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const image_kit_configuration_form = document.querySelector('[name="image_kit_configuration_form"]');

        // Collect form data using the name attributes
        const public_key = image_kit_configuration_form.querySelector('[name="public_key"]');
        const private_key = image_kit_configuration_form.querySelector('[name="private_key"]');
        const url_endpoint = image_kit_configuration_form.querySelector('[name="url_endpoint"]');

        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            public_key.value = data_obj.data[0].public_key;
            private_key.value = data_obj.data[0].private_key;
            url_endpoint.value = data_obj.data[0].url_endpoint;
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     

