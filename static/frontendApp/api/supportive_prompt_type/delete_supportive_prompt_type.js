
//  delete supportive_prompt_type api
function delete_supportive_prompt_type_api(slug_id){

    const api_url = `${delete_supportive_prompt_type_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

