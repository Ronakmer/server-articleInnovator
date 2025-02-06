


// table_tab_content_api
async function table_tab_content_api() {
    try {
        const access_token = sessionStorage.getItem("access_token");
        
        const current_page_url = window.location.href;
        const domain_slug_id = current_page_url.split('/').pop();


        const query_params = new URLSearchParams({});
        if (domain_slug_id) {
            query_params.append("domain_slug_id", domain_slug_id);
        }


        const response = await fetch(`${console_metrics_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('table_tab_content_api:', data);

            return data;
                

            // show_toast("success", "Roles fetched successfully");
        } else {
            const error_data = await response.json();
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
