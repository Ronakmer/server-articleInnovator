


function status_user_detail_api(slug_id, is_checked) {
    console.log(`user_detail ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_user_detail_url, data, slug_id, list_user_detail_page_url);
    })()

}


