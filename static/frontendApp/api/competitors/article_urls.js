function render_data_to_table_article_urls(response_data, current_page, limit){

    table_data_article_urls('article_tbody', response_data, 'delete_role_api', 'status_role_api', update_role_page_url,current_page, limit)
}

async function get_article_urls() {

    const competitor_domain_mapping_slug_id = localStorage.getItem('competitor_domain_mapping_slug_id');
    
    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page
    const searchInput = document.getElementById('search-input');

    const filters = {
        search: searchInput ? searchInput.value : '',
        order_by:'-created_date',

        competitor_domain_mapping_slug_id: competitor_domain_mapping_slug_id,
    };

    const response_data = await list_api(scrap_articles_url, 'article_tbody', offset, limit, filters, '', '', null, current_page, '', '', render_data_to_table_article_urls);
    if(response_data.success){
        console.log(response_data);
    }
    else{
        console.log(response_data);
    }
}



async function add_article_urls() {

    const competitor_domain_mapping_slug_id = localStorage.getItem('competitor_domain_mapping_slug_id');
    
    // Get selected article objects from checkboxes (contains URL and competitor_selected_url_slug_id)
    const selectedArticles = getSelectedArticleUrls();
    
    if (selectedArticles.length === 0) {
        alert('Please select at least one URL');
        return;
    }

    const data = new FormData();
    data.append("competitor_domain_mapping_slug_id", competitor_domain_mapping_slug_id);
    data.append("selected_articles", JSON.stringify(selectedArticles));
    data.append("created_by", "1");
    
    console.log('Sending selected articles:', selectedArticles);

    const response = await add_api(add_article_url_url, data);
    if(response.success){

        current_step = 4;
        showStep(current_step);
    }
    else{
        console.log(response);
    }
}