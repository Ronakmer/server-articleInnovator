
//  delete notification api
function delete_notification_api(slug_id){

    const api_url = `${delete_notification_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

