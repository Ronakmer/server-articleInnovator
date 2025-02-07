




// fetch_wp_data  api
async function fetch_wp_data_api() {
    try {
        const temp_url = new URLSearchParams(window.location.search);
        const domain_slug_id = temp_url.get('domain_slug_id');
        
        const access_token = sessionStorage.getItem("access_token");
        
        const workspace_slug_id = sessionStorage.getItem("workspace_slug_id");

        // const domain_slug_id = sessionStorage.getItem("domain_slug_id");

        const query_params = new URLSearchParams({});

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }
        if (domain_slug_id) {
            query_params.append("domain_slug_id", domain_slug_id);
        }

        const response = await fetch(`${fetch_wp_data_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('Roles fetched successfully:', data);
            
           
                

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

fetch_wp_data_api()