


function status_article_type_field_api(slug_id, is_checked) {
    console.log(`article_type_field ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_article_type_field_url, data, slug_id, list_article_type_field_page_url);
    })()

}


