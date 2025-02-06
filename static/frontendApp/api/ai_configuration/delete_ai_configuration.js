
//  delete ai_configuration api
function delete_ai_configuration_api(slug_id){

    const api_url = `${delete_ai_configuration_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

