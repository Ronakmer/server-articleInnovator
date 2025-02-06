
//  delete article_type api
function delete_article_type_api(slug_id){

    const api_url = `${delete_article_type_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

