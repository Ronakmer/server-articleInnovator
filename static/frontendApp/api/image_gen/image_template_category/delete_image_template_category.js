
//  delete image_template_category api
function delete_image_template_category_api(slug_id){

    const api_url = `${delete_image_template_category_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

