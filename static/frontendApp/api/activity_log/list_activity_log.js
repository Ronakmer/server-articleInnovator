



function render_data_to_table(response_data, current_page, limit){
    
    table_data_activity_log('activity_log_tbody', response_data, current_page, limit)

}

// list activity_log api
async function list_activity_log_api() {
  
    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    const filters = {
        search: searchInput ? searchInput.value : '',
    };


    const response_data = await list_api(list_activity_log_url, 'activity_log_tbody', offset, limit, filters, '', '', '', current_page, 'activity_logs', '', render_data_to_table);
    console.log(response_data,'0')
    
}

list_activity_log_api()


