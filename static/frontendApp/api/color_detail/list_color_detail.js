
function render_data_to_table(response_data, current_page, limit){
    
    // table_data_permission('permission_tbody', response_data, 'delete_permission_api', 'status_permission_api', update_permission_page_url, current_page, limit)
    table_data_color_detail('color_detail_tbody', response_data, 'delete_color_detail_api', 'status_color_detail_api', update_color_detail_page_url, current_page, limit)

}

// list color_detail api
async function list_color_detail_api() {
  


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


    const response_data = await list_api(list_color_detail_url, 'color_detail_tbody', offset, limit, filters, 'delete_color_detail_api', 'status_color_detail_api', update_color_detail_page_url, current_page, 'color_details', '', render_data_to_table);
    console.log(response_data,'0')
    
    // table_data_color_detail('color_detail_tbody', response_data, 'delete_color_detail_api', 'status_color_detail_api', update_color_detail_page_url)
    
}

list_color_detail_api()


