



function render_data_to_table(response_data, current_page, limit){
    
    table_data_notification('notification_tbody', response_data, current_page, limit, 'delete_notification_api')

}

// list notification api
async function list_notification_api() {
  
    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    const filters = {
        search: searchInput ? searchInput.value : '',
    };


    const response_data = await list_api(list_notification_url, 'notification_tbody', offset, limit, filters, 'delete_notification_api', '', '', current_page, 'notifications', '', render_data_to_table);
    console.log(response_data,'0')
    
}

list_notification_api()


