


function status_role_api(slug_id, is_checked) {
    console.log(`Role ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_role_url, data, slug_id, list_role_page_url);
    })()

}


