
function render_data_to_table(response_data, current_page, limit){
    
    table_data_role('role_tbody', response_data, 'delete_role_api', 'status_role_api', update_role_page_url,current_page, limit)
   
}

// list roles api
async function list_role_api() {

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


    const response_data = await  list_api(list_role_url, 'role_tbody', offset, limit, filters, 'delete_role_api', 'status_role_api', update_role_page_url, current_page, 'roles', '', render_data_to_table);
    console.log(response_data,'0')
    
   
}
list_role_api()

