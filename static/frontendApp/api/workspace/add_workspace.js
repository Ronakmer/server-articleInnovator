

async function add_workspace_api() {
    
    // Get the form element
    const workspace_form = document.querySelector('[name="workspace_form"]');

    let temp_avatar_image_id = '';
    if (avatar_image_id){

        temp_avatar_image_id = avatar_image_id.replace('/media/', '');
    }

    // Collect form data using the name attributes
    const name = workspace_form.querySelector('[name="name"]').value;
    const logo = workspace_form.querySelector('[name="logo"]');

    // // Prepare the data object
    // const data = {
    //     name: name,
    //     logo: base64Image,
    // };

    const data = new FormData();
    data.append("name", name);
    if(temp_avatar_image_id){

        data.append("avatar_image_path", temp_avatar_image_id);
    }

    if (logo && logo.files && logo.files[0]) {
        data.append('logo', logo.files[0]);
    }
    // data.append("logo", logo);


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_workspace_url, data, slug_id, list_workspace_page_url);
        } else {
            await add_api(add_workspace_url, data, list_workspace_page_url);
        }
    })()

}



(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_workspace_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);

        // Get the form element
        const workspace_form = document.querySelector('[name="workspace_form"]');

        // Collect form data using the name attributes
        const name = workspace_form.querySelector('[name="name"]');
        // const logo = workspace_form.querySelector('[name="logo"]');
        // console.log(logo)
        // console.log(data_obj.workspaces[0].logo)

        if (data_obj && data_obj.workspaces && data_obj.workspaces.length > 0) {
            name.value = data_obj.workspaces[0].name;
            // logo.src = data_obj.workspaces[0].logo.files[0];
        } else {
            // name.value = ''; 
            window.location.href = error_page;
        }
        
    }
})()
     

