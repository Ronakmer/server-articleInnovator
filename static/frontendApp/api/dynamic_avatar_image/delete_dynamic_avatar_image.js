
//  delete dynamic_avatar_image api
function delete_dynamic_avatar_image_api(slug_id){

    const api_url = `${delete_dynamic_avatar_image_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

