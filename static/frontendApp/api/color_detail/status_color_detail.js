


function status_color_detail_api(slug_id, is_checked) {
    console.log(` ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_color_detail_url, data, slug_id, list_color_detail_page_url);
    })()

}


