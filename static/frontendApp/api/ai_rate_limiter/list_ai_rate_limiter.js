


// list api
async function ai_rate_limiter_api() {
    try {

        const access_token = localStorage.getItem("access_token");
        
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");

        const query_params = new URLSearchParams({});

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }

        const response = await fetch(`${list_ai_rate_limiter_url}?${query_params.toString()}`, {
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
            ai_rate_limiter_provider_data(data.data.ai_rate_limiter_provider_data)
            ai_rate_limiter_worker_data(data.data.ai_rate_limiter_worker_data)
            ai_rate_limiter_message_tbody_data(data.data.ai_rate_limiter_worker_data)

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

ai_rate_limiter_api();