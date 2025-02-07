


function render_data_to_table(response_data, current_page, limit){
    
    table_data_image_tag('image_tag_tbody', response_data, 'delete_image_tag_api', 'status_image_tag_api', update_image_tag_page_url,current_page, limit)

}

// list image_tag api
async function list_image_tag_api() {
  


    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    const filters = {
        search: searchInput ? searchInput.value : '',

    };


    const response_data = await list_api(list_image_tag_url, 'image_tag_tbody', offset, limit, filters, 'delete_image_tag_api', 'status_image_tag_api', update_image_tag_page_url, current_page, 'image_tags','', render_data_to_table);
    console.log(response_data,'0')
    
}

list_image_tag_api()


