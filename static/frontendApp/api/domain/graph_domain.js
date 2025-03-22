






// domain_console_graph_api 
async function domain_console_graph_api(api_url, domain_slug_id, start_date, end_date) {
    try {
        const access_token = localStorage.getItem("access_token");

        const query_params = new URLSearchParams({});
        if (domain_slug_id) {
            query_params.append("domain_slug_id", domain_slug_id);
        }
        if (start_date) {
            query_params.append("start_date", start_date);
        }
        if (end_date) {
            query_params.append("end_date", end_date);
        }

        const response = await fetch(`${api_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('domain_console_graph_api:', data);
            
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










// domain_analytics_graph_api
async function domain_analytics_graph_api(api_url, domain_slug_id, start_date, end_date) {
    try {
        const access_token = localStorage.getItem("access_token");

        const query_params = new URLSearchParams({});
        if (domain_slug_id) {
            query_params.append("domain_slug_id", domain_slug_id);
        }
        if (start_date) {
            query_params.append("start_date", start_date);
        }
        if (end_date) {
            query_params.append("end_date", end_date);
        }

        const response = await fetch(`${api_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('domain_analytics_graph_api:', data);
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






// domain_article_graph_api
async function domain_article_graph_api(api_url, domain_slug_id, start_date, end_date) {
    try {
        const access_token = localStorage.getItem("access_token");

        const query_params = new URLSearchParams({});
        if (domain_slug_id) {
            query_params.append("domain_slug_id", domain_slug_id);
        }
        if (start_date) {
            query_params.append("start_date", start_date);
        }
        if (end_date) {
            query_params.append("end_date", end_date);
        }

        
        const response = await fetch(`${api_url}?${query_params.toString()}`, {
        // const response = await fetch(`${a}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('domain_article_graph_api:', data);
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
