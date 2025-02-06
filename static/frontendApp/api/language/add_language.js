

function add_language_api() {

    // Get the form element
    const language_form = document.querySelector('[name="language_form"]');

    // Collect form data using the name attributes
    const name = language_form.querySelector('[name="name"]').value;

    // Prepare the data object
    // const data = {
    //     name: name,
    // };
    const data = new FormData();
    data.append("name", name);


    // add_api(add_language_url, data, list_language_page_url);

    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_language_url, data, slug_id, list_language_page_url);
        } else {
            await add_api(add_language_url, data, list_language_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_language_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const language_form = document.querySelector('[name="language_form"]');

        // Collect form data using the name attributes
        const name = language_form.querySelector('[name="name"]');

        if (data_obj && data_obj.languages && data_obj.languages.length > 0) {
            name.value = data_obj.languages[0].name;
        } else {
            // name.value = ''; 
            window.location.href = error_page;
        }
        
    }
})()
     

