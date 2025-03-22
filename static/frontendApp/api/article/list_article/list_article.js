


function render_data_to_table(response_data, current_page, limit){
    
    table_data_article('article_tbody', response_data, 'delete_article_api', 'status_article_api', update_article_page_url, current_page, limit)

}




// list article api
async function list_article_api() {
  
    const selected_sort = document.querySelector('input[name="order_by"]:checked').value;
    console.log("Selected Sort:", selected_sort); // Debugging purpose


    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    const filters = {
        search: searchInput ? searchInput.value : '',
        order_by:selected_sort,
        
    };
    const current_page_url = window.location.href;
    const domain_slug_id = current_page_url.split('/').pop();

    const response_data = await list_api(list_article_url, 'article_tbody', offset, limit, filters, 'delete_article_api', 'status_article_api', '', current_page, 'articles', domain_slug_id, render_data_to_table);
    console.log(response_data,'0')
    


    // remove extra session 
    const sessionKeys = [
        "current_step",
        "step_expiry",
        "article_type_category",
        "article_type_title", 
        "current_url",
        "article_type_slug_id"
    ];
    
    // Clear each session key
    sessionKeys.forEach(key => localStorage.removeItem(key));


}

list_article_api()


