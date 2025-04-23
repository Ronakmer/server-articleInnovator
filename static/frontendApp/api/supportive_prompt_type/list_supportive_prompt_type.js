
function render_data_to_table(response_data, current_page, limit){
    
    table_data_supportive_prompt_type('supportive_prompt_type_tbody', response_data, 'delete_supportive_prompt_type_api', 'status_supportive_prompt_type_api', update_supportive_prompt_type_page_url,current_page, limit)
   
}

// list supportive_prompt_types api
async function list_supportive_prompt_type_api() {

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


    const response_data = await  list_api(list_supportive_prompt_type_url, 'supportive_prompt_type_tbody', offset, limit, filters, 'delete_supportive_prompt_type_api', 'status_supportive_prompt_type_api', update_supportive_prompt_type_page_url, current_page, 'supportive_prompt_types', '', render_data_to_table);
    console.log(response_data,'0')
    
   
}
list_supportive_prompt_type_api()

