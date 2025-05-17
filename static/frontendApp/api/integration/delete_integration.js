
//  delete integration api
function delete_integration_api(slug_id){

    const api_url = `${delete_integration_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

