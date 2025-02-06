
//  delete user_detail api
function delete_user_detail_api(slug_id){

    const api_url = `${delete_user_detail_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

