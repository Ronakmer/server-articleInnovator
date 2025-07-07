
//  delete role api
function delete_competitor_api(slug_id){

    const api_url = `${delete_competitor_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

