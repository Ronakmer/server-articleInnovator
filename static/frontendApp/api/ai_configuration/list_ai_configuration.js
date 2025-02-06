

function render_data_to_table(response_data, current_page, limit){
    
    table_data_ai_configuration('ai_configuration_tbody', response_data, 'delete_ai_configuration_api', 'status_ai_configuration_api', update_ai_configuration_page_url, current_page, limit)
   
}


// list ai_configuration api
async function list_ai_configuration_api() {
  


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


    const response_data = await list_api(list_ai_configuration_url, 'ai_configuration_tbody', offset, limit, filters, 'delete_ai_configuration_api', 'status_ai_configuration_api', update_ai_configuration_page_url, current_page, 'ai_configurations', '', render_data_to_table);
    console.log(response_data,'0')
    
    // table_data_ai_configuration('ai_configuration_tbody', response_data, 'delete_ai_configuration_api', 'status_ai_configuration_api', update_ai_configuration_page_url)
    
}

list_ai_configuration_api()


