

function add_ai_configuration_api() {

    // Get the form element
    const ai_configuration_form = document.querySelector('[name="ai_configuration_form"]');

    // Collect form data using the name attributes
    const api_provider = ai_configuration_form.querySelector('[name="api_provider"]').value;
    const api_type = ai_configuration_form.querySelector('[name="api_type"]').value;
    const api_version = ai_configuration_form.querySelector('[name="api_version"]').value;
    const api_key = ai_configuration_form.querySelector('[name="api_key"]').value;
    const api_model = ai_configuration_form.querySelector('[name="api_model"]').value;
    const api_url = ai_configuration_form.querySelector('[name="api_url"]').value;
    const email = ai_configuration_form.querySelector('[name="email"]').value;

    const data = new FormData();
    data.append("api_provider", api_provider);
    data.append("api_type", api_type);
    data.append("api_version", api_version);
    data.append("api_key", api_key);
    data.append("api_model", api_model);
    data.append("api_url", api_url);
    data.append("email", email);



    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_ai_configuration_url, data, slug_id, list_ai_configuration_page_url);
        } else {
            await add_api(add_ai_configuration_url, data, list_ai_configuration_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_ai_configuration_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const ai_configuration_form = document.querySelector('[name="ai_configuration_form"]');

        const api_provider = ai_configuration_form.querySelector('[name="api_provider"]');
        const api_type = ai_configuration_form.querySelector('[name="api_type"]');
        const api_version = ai_configuration_form.querySelector('[name="api_version"]');
        const api_key = ai_configuration_form.querySelector('[name="api_key"]');
        const api_model = ai_configuration_form.querySelector('[name="api_model"]');
        const api_url = ai_configuration_form.querySelector('[name="api_url"]');
        const email = ai_configuration_form.querySelector('[name="email"]');
    
        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            api_provider.value = data_obj.data[0].api_provider;
            api_type.value = data_obj.data[0].api_type;
            api_version.value = data_obj.data[0].api_version;
            api_key.value = data_obj.data[0].api_key;
            api_model.value = data_obj.data[0].api_model;
            api_url.value = data_obj.data[0].api_url;
            email.value = data_obj.data[0].email;
        } else {
            // name.value = ''; 
            window.location.href = error_page;
        }
        
    }
})()
     

