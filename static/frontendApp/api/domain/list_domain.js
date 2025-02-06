
function render_data_to_table(response_data, current_page, limit){
    
    table_data_domain('domain_tbody', response_data, 'delete_domain_api', 'status_domain_api', update_domain_page_url, detail_domain_page_url,current_page, limit)

}

// list domain api
async function list_domain_api() {
  


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


    const response_data = await list_api(list_domain_url, 'domain_tbody', offset, limit, filters, 'delete_domain_api', 'status_domain_api', update_domain_page_url, current_page, 'domains', '', render_data_to_table);
    console.log(response_data,'0')
    
    // table_data_domain('domain_tbody', response_data, 'delete_domain_api', 'status_domain_api', update_domain_page_url, detail_domain_page_url)
    
}

list_domain_api()


    