


function status_dynamic_avatar_image_api(slug_id, is_checked) {
    console.log(`dynamic_avatar_image ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_dynamic_avatar_image_url, data, slug_id, list_dynamic_avatar_image_page_url);
    })()

}


