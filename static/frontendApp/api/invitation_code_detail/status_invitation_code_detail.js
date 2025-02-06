


function status_invitation_code_detail_api(slug_id, is_checked) {
    console.log(`invitation_code_detail ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_invitation_code_detail_url, data, slug_id, list_invitation_code_detail_page_url);
    })()

}


