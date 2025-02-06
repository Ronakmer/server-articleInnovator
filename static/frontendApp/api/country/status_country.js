


function status_country_api(slug_id, is_checked) {
    console.log(`country ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_country_url, data, slug_id, list_country_page_url);
    })()

}


