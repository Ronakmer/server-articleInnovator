
//  delete configuration_settings api
function delete_configuration_settings_api(slug_id){

    const api_url = `${delete_configuration_settings_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

