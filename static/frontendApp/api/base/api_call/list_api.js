


// list api
async function list_api(api_url, table_name, offset, limit, filters, delete_function_name, status_function_name, update_page_url, current_page, response_key, domain_slug_id, render_data_to_table=()=>{}) {
    try {
        
        const access_token = localStorage.getItem("access_token");
        
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");

        const query_params = new URLSearchParams({
            offset,
            limit,
            ...filters,
        });

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }
        if (domain_slug_id) {
            query_params.append("domain_slug_id", domain_slug_id);
        }
    

        const response = await fetch(`${api_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        const responseData = await response.json();

        check_authentication_error(responseData)

        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('fetched successfully:', data);
            console.log('fetched successfully:', data.pagination.total_count);
            const total_count = data.pagination.total_count;
            
            render_pagination(total_count, limit, current_page, api_url, table_name, filters, delete_function_name, status_function_name, update_page_url, response_key, render_data_to_table, domain_slug_id);
            render_data_to_table(data, current_page, limit)
            
            // if (["author_tbody", "tag_tbody", "categories_tbody"].includes(table_name)) {

            // if (["author_tbody","categories_tbody"].includes(table_name)) {
            //     render_pagination( total_count, limit, current_page, api_url, table_name, filters, delete_function_name, status_function_name, update_page_url, response_key, render_data_to_table, domain_slug_id);
            //     render_data_to_table_categories_tbody(data, current_page, limit);
            // }else{
            //     render_pagination( total_count, limit, current_page, api_url, table_name, filters, delete_function_name, status_function_name, update_page_url, response_key, render_data_to_table, domain_slug_id);
            //     render_data_to_table(data, current_page, limit);
            // }

            return data;
                

            // show_toast("success", "Roles fetched successfully");
        } else {
            const error_data = responseData;
            console.error('Failed to fetch roles:', error_data);

            const errorMessage = error_data.error || "Something went wrong";
            show_toast("error", `Error: ${errorMessage}`);
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later.");
    }
}
