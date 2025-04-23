


function status_supportive_prompt_api(slug_id, is_checked) {
    console.log(`supportive_prompt ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_supportive_prompt_url, data, slug_id, list_supportive_prompt_page_url);
    })()

}


