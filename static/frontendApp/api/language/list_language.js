
function render_data_to_table(response_data, current_page, limit){
    
    table_data_language('language_tbody', response_data, 'delete_language_api', 'status_language_api', update_language_page_url, current_page, limit)

}



// list language api
async function list_language_api() {

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


    const response_data = await list_api(list_language_url, 'language_tbody', offset, limit, filters, 'delete_language_api', 'status_language_api', update_language_page_url, current_page, 'languages', '', render_data_to_table);
    console.log(response_data,'0')
    
    
}

list_language_api()


