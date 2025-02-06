
//  delete image_tag api
function delete_image_tag_api(slug_id){

    const api_url = `${delete_image_tag_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

