
function render_data_to_table(response_data, current_page, limit){
    
    table_data_dynamic_avatar_image('dynamic_avatar_image_tbody', response_data, 'delete_dynamic_avatar_image_api', 'status_dynamic_avatar_image_api', update_dynamic_avatar_image_page_url,current_page, limit)

}



// list dynamic_avatar_images api
async function list_dynamic_avatar_image_api() {
 
    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    const filters = {
        search: searchInput ? searchInput.value : '',

    };



    const response_data = await  list_api(list_dynamic_avatar_image_url, 'dynamic_avatar_image_tbody', offset, limit, filters, 'delete_dynamic_avatar_image_api', 'status_dynamic_avatar_image_api', update_dynamic_avatar_image_page_url, current_page, 'dynamic_avatar_images', '', render_data_to_table);
    console.log(response_data,'0')
    
   
}
list_dynamic_avatar_image_api()


