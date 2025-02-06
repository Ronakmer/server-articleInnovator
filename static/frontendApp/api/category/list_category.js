
function render_data_to_table(response_data, current_page, limit){
    
    table_data_category('categories_tbody', response_data, 'delete_category_api', 'status_category_api', '', current_page, limit)

}


// list category api
async function list_category_api() {

    let current_page = 1; // Initialize current page
    const limit = 3; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    // const filters = {};
    const filters = {
        // status: document.getElementById('status-filter').value,
        // search: document.getElementById('search-input').value,
        search: searchInput ? searchInput.value : '',

    };
    const current_page_url = window.location.href;
    const domain_slug_id = current_page_url.split('/').pop();



    // const api_url = `${list_category_url}&domain_slug_id=${domain_slug_id}`

    const response_data = await list_api(list_category_url, 'categories_tbody', offset, limit, filters, 'delete_category_api', 'status_category_api', '', current_page, 'categorys', domain_slug_id, render_data_to_table);
    console.log(response_data,'0')
    
    // table_data_category('categories_tbody', response_data, 'delete_category_api', 'status_category_api', '')
    
}

// list_category_api()


