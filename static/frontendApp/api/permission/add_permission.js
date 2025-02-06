

function add_permission_api() {

    // Get the form element
    const permission_form = document.querySelector('[name="permission_form"]');

    // Collect form data using the name attributes
    const name = permission_form.querySelector('[name="name"]').value;

    // Prepare the data object
    // const data = {
    //     name: name,
    // };
    const data = new FormData();
    data.append("name", name);



    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_permission_url, data, slug_id, list_permission_page_url);
        } else {
            await add_api(add_permission_url, data, list_permission_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_permission_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const permission_form = document.querySelector('[name="permission_form"]');

        // Collect form data using the name attributes
        const name = permission_form.querySelector('[name="name"]');

        if (data_obj && data_obj.permissions && data_obj.permissions.length > 0) {
            name.value = data_obj.permissions[0].name;
        } else {
            // name.value = ''; 
            window.location.href = error_page;
        }
        
    }
})()
     

