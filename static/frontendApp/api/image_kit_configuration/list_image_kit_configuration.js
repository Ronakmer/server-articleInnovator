
function render_data_to_table(response_data, current_page, limit){
    
    table_data_image_kit_configuration('image_kit_configuration_tbody', response_data, 'delete_image_kit_configuration_api', 'status_image_kit_configuration_api', update_image_kit_configuration_page_url, current_page, limit)

}



// list image_kit_configuration api
async function list_image_kit_configuration_api() {

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


    const response_data = await list_api(list_image_kit_configuration_url, 'image_kit_configuration_tbody', offset, limit, filters, 'delete_image_kit_configuration_api', 'status_image_kit_configuration_api', update_image_kit_configuration_page_url, current_page, 'image_kit_configurations', '', render_data_to_table);
    console.log(response_data,'0')
    
    
}

list_image_kit_configuration_api()


