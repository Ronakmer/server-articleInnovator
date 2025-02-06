
//  delete workspace api
function delete_workspace_api(slug_id){

    const api_url = `${delete_workspace_url}${slug_id}`;

    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id)

}

