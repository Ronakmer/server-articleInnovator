
//  delete tag api
function delete_tag_api(slug_id){

    const api_url = `${delete_tag_url}${slug_id}`;

    const current_page_url = window.location.href;
    const domain_slug_id = current_page_url.split('/').pop();


    // delete_api(api_url, slug_id)
    delete_toast(api_url, slug_id, domain_slug_id)

}

