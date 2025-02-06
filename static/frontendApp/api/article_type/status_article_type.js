


function status_article_type_api(slug_id, is_checked) {
    console.log(`article_type ${slug_id} status changed to: ${is_checked ? 'true' : 'false'}`);

       // Prepare the data object
       const data = {
        status: is_checked,
    };

    (async ()=>{ 
        await status_api(update_article_type_url, data, slug_id, list_article_type_page_url);
    })()

}


