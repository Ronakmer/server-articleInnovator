


function render_data_to_table(response_data, current_page, limit){
    
    table_data_country('country_tbody', response_data, 'delete_country_api', 'status_country_api', update_country_page_url, current_page, limit)

}


// list countrys api
async function list_country_api() {
 
    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    const filters = {
        search: searchInput ? searchInput.value : '',

    };



    const response_data = await  list_api(list_country_url, 'country_tbody', offset, limit, filters, 'delete_country_api', 'status_country_api', update_country_page_url, current_page, 'countrys', '', render_data_to_table);
    console.log(response_data,'0')
    
   
}
list_country_api()


