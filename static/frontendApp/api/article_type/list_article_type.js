
function render_data_to_table(response_data, current_page, limit){
    
    table_data_article_type('article_type_tbody', response_data, 'delete_article_type_api', 'status_article_type_api', update_article_type_page_url, current_page, limit)
   
}


// list article_type api
async function list_article_type_api() {
  


    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    // const filters = {};
    const filters = {
        // status: document.getElementById('status-filter').value,
        // search: document.getElementById('search-input').value,
        search: searchInput ? searchInput.value : '',

    };


    const response_data = await list_api(list_article_type_url, 'article_type_tbody', offset, limit, filters, 'delete_article_type_api', 'status_article_type_api', update_article_type_page_url, current_page, 'article_types', '', render_data_to_table);
    console.log(response_data,'0')
    
    // table_data_article_type('article_type_tbody', response_data, 'delete_article_type_api', 'status_article_type_api', update_article_type_page_url)
    
}

list_article_type_api()


