
//  delete country api
function delete_country_api(slug_id){

    const api_url = `${delete_country_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

