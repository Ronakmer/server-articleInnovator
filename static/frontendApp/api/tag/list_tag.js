


function render_data_to_table(response_data, current_page, limit){
    
    table_data_tag('tag_tbody', response_data, 'delete_tag_api', 'status_tag_api', '', current_page, limit)

}



// list tag api
async function list_tag_api() {
  


    let current_page = 1; // Initialize current page
    const limit = 10; // Number of items per page
    const offset = (current_page - 1) * limit; // Calculate offset based on current page

    const searchInput = document.getElementById('search-input');

    const filters = {
        search: searchInput ? searchInput.value : '',
        // order_by:selected_sort,

    };
    const current_page_url = window.location.href;
    const domain_slug_id = current_page_url.split('/').pop();



    const response_data = await list_api(list_tag_url, 'tag_tbody', offset, limit, filters, 'delete_tag_api', 'status_tag_api', '', current_page, 'tags', domain_slug_id, render_data_to_table);
    console.log(response_data,'0')
    
    
}


