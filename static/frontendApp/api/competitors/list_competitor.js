function render_data_to_table_competitor(response_data, current_page, limit){
    
    table_data_competitor('competitor_tbody', response_data, 'delete_competitor_api', 'status_competitor_api', '',current_page, limit)
   
}

async function list_competitor_api(){
    try {
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
    console.log(filters,'filters')
    const response_data = await list_api(list_competitor_url, 'competitor_tbody', offset, limit, filters, 'delete_competitor_api', 'status_competitor_api', '', current_page, 'competitors', '', render_data_to_table_competitor);
    console.log(response_data,'response_data')
    
        
    } catch (error) {
        console.log(error,'error')
    }
}

list_competitor_api()

