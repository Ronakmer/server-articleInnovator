


function status_language_api(slug_id, is_checked) {
    console.log(` ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_language_url, data, slug_id, list_language_page_url);
    })()

}


