
//  delete article api
function delete_article_api(slug_id){

    alert(0)
    const api_url = `${delete_article_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

