async function send_url_for_aticle_api() {
    const data = new FormData();
    data.append("competitor_domain_mapping_slug_id", localStorage.getItem("competitor_domain_mapping_slug_id"));

    // ⬅️ Use await to resolve the promise
    const response_data = await add_api(send_article_url_to_create_article_api_url, data, null);

    console.log(response_data, 'response_data');

    if (response_data.success === true) {
        console.log(response_data.success, 'response_data.success');
        if (typeof list_competitor_page_url !== 'undefined' && list_competitor_page_url) {
            setTimeout(() => {
                window.location.href = list_competitor_page_url;
            }, 1000);
        }
    }
}
