


// set data api
async function set_data_api(api_url, slug_id) {
    try {
        const access_token = localStorage.getItem("access_token");

        const workspace_slug_id = localStorage.getItem("workspace_slug_id");
        
        const query_params = new URLSearchParams();

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }

        
        // Perform the GET API call
        const response = await fetch(`${api_url}&${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
                // 'slug_id': `${slug_id}`,
            },
        });

        const responseData = await response.json();

        check_authentication_error(responseData)
        
        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('Roles fetched successfully:', data);

            return data

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