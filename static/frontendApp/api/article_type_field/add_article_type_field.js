

function add_article_type_field_api() {

    // Get the form element
    const article_type_field_form = document.querySelector('[name="article_type_field_form"]');

    // Collect form data using the name attributes
    const name = article_type_field_form.querySelector('[name="name"]').value;
    const label = article_type_field_form.querySelector('[name="label"]').value;
    const placeholder = article_type_field_form.querySelector('[name="placeholder"]').value;
    const field_type = article_type_field_form.querySelector('[name="field_type"]').value;
    const required = article_type_field_form.querySelector('[name="required"]').checked;

    // Prepare the data object
    // const data = {
    //     name: name,
    //     label: label,
    //     placeholder: placeholder,
    //     field_type: field_type,
    //     required: required,
    // };
    const data = new FormData();
    data.append("name", name);
    data.append("label", label);
    data.append("placeholder", placeholder);
    data.append("field_type", field_type);
    data.append("required", required);


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_article_type_field_url, data, slug_id, list_article_type_field_page_url);
        } else {
            await add_api(add_article_type_field_url, data, list_article_type_field_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_article_type_field_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const article_type_field_form = document.querySelector('[name="article_type_field_form"]');

        // Collect form data using the name attributes
        const name = article_type_field_form.querySelector('[name="name"]');
        const label = article_type_field_form.querySelector('[name="label"]');
        const placeholder = article_type_field_form.querySelector('[name="placeholder"]');
        const field_type = article_type_field_form.querySelector('[name="field_type"]');
        const required = article_type_field_form.querySelector('[name="required"]');

        
        if (data_obj && data_obj.article_type_fields && data_obj.article_type_fields.length > 0) {
            name.value = data_obj.article_type_fields[0].name;
            label.value = data_obj.article_type_fields[0].label;
            placeholder.value = data_obj.article_type_fields[0].placeholder;
            field_type.value = data_obj.article_type_fields[0].field_type;
            required.checked  = data_obj.article_type_fields[0].required;
        } else {
            // name.value = ''; 
            window.location.href = error_page;
        }
        
    }
})()
     

