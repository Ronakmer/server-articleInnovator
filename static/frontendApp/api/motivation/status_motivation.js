


function status_motivation_api(slug_id, is_checked) {
    console.log(` ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_motivation_url, data, slug_id, list_motivation_page_url);
    })()

}


