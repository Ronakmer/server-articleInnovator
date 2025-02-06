

async function add_dynamic_avatar_image_api() {

    // Get the form element
    const dynamic_avatar_image_form = document.querySelector('[name="dynamic_avatar_image_form"]');

    // Collect form data using the name attributes
    const avatar_type = dynamic_avatar_image_form.querySelector('[name="avatar_type"]').value;
    const avatar_image = dynamic_avatar_image_form.querySelector('[name="avatar_image"]');

    // // Prepare the data object
    // const data = {
    //     name: name,
    //     dynamic_avatar_image_flag: base64Image,
    // };

    const data = new FormData();
    data.append("avatar_type", avatar_type);
    if (avatar_image && avatar_image.files && avatar_image.files[0]) {
        data.append('avatar_image', avatar_image.files[0]);
    }
    // data.append("avatar_image", avatar_image);


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_dynamic_avatar_image_url, data, slug_id, list_dynamic_avatar_image_page_url);
        } else {
            await add_api(add_dynamic_avatar_image_url, data, list_dynamic_avatar_image_page_url);
        }
    })()

}



(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_dynamic_avatar_image_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const dynamic_avatar_image_form = document.querySelector('[name="dynamic_avatar_image_form"]');

        // Collect form data using the name attributes
        const avatar_type = dynamic_avatar_image_form.querySelector('[name="avatar_type"]');

        if (data_obj && data_obj.dynamic_avatar_images && data_obj.dynamic_avatar_images.length > 0) {
            avatar_type.value = data_obj.dynamic_avatar_images[0].avatar_type;
        } else {
            // name.value = ''; 
            window.location.href = error_page;
        }
        
    }
})()
     

