
//  delete color_detail api
function delete_color_detail_api(slug_id){

    const api_url = `${delete_color_detail_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

