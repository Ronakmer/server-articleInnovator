
//  delete language api
function delete_language_api(slug_id){

    const api_url = `${delete_language_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

