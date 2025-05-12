






// articleconsole_graph_api 
async function article_console_graph_api(api_url, wp_slug, start_date, end_date) {
    try {
        const access_token = localStorage.getItem("access_token");

        const query_params = new URLSearchParams({});
        if (wp_slug) {
            query_params.append("wp_slug", wp_slug);
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

        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('article_console_graph_api:', data);
            
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










// article_analytics_graph_api
async function article_analytics_graph_api(api_url, wp_slug, start_date, end_date) {
    try {
        const access_token = localStorage.getItem("access_token");

        const query_params = new URLSearchParams({});
        if (wp_slug) {
            query_params.append("wp_slug", wp_slug);
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

        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('article_analytics_graph_api:', data);
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






// article_article_graph_api
async function article_article_graph_api(api_url, wp_slug, start_date, end_date) {
    try {
        const access_token = localStorage.getItem("access_token");

        const query_params = new URLSearchParams({});
        if (wp_slug) {
            query_params.append("wp_slug", wp_slug);
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

        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('article_article_graph_api:', data);
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
