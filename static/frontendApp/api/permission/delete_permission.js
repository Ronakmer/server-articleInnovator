
//  delete permission api
function delete_permission_api(slug_id){

    const api_url = `${delete_permission_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

