
//  delete prompt api
function delete_prompt_api(slug_id){

    const api_url = `${delete_prompt_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

