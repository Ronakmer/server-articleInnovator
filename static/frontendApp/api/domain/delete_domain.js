
//  delete domain api
function delete_domain_api(slug_id){

    const api_url = `${delete_domain_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

