
//  delete image_kit_configuration api
function delete_image_kit_configuration_api(slug_id){

    const api_url = `${delete_image_kit_configuration_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

