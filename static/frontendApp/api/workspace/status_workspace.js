


function status_workspace_api(slug_id, is_checked) {
    console.log(`workspace ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_workspace_url, data, slug_id, list_workspace_page_url);
    })()

}


