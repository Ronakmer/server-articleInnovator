


function render_data_to_table(response_data, current_page, limit){
    
    table_data_article_type_field('article_type_field_tbody', response_data, 'delete_article_type_field_api', 'status_article_type_field_api', update_article_type_field_page_url, current_page, limit)

}

// list article_type_field api
async function list_article_type_field_api() {
  


    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    // const filters = {};
    const filters = {
        search: searchInput ? searchInput.value : '',

    };


    const response_data = await list_api(list_article_type_field_url, 'article_type_field_tbody', offset, limit, filters, 'delete_article_type_field_api', 'status_article_type_field_api', update_article_type_field_page_url, current_page, 'article_type_fields', '', render_data_to_table);
    console.log(response_data,'0')
    
    
}

list_article_type_field_api()


