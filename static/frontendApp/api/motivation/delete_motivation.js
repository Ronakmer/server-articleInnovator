
//  delete motivation api
function delete_motivation_api(slug_id){

    const api_url = `${delete_motivation_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

