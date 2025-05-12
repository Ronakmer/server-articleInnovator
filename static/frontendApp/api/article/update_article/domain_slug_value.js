

async function domain_slug_value(){

    setTimeout(async () => {
        try {
            const set_manual_domain_slug_id = document.querySelector('[name="manual_domain_slug_id"]');

            const temp_id = set_manual_domain_slug_id.value.trim();

            const access_token = localStorage.getItem("access_token");
            if (!access_token) {
                console.error("Access token not found. Please log in again.");
                return;
            }
            
            // const workspace_slug_id = localStorage.getItem("workspace_slug_id");
            const workspace_slug_id = "77b4ad49-db8a-4434-aad5-c2351c953cc7"; // Hardcoded workspace ID

            const query_params = new URLSearchParams();
            query_params.append("workspace_slug_id", workspace_slug_id);
            query_params.append("slug_id", temp_id);

            const api_url = `${list_domain_url}?${query_params.toString()}`;

            // Fetch data
            const response = await fetch(api_url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${access_token}`,
                },
            });

            const responseData = await response.json();

            check_authentication_error(responseData)
    

            if (response.ok) {
                const data = responseData;
                // console.log("API Response:", data);
                console.log("API Response:", data.data[0].permalinks);
                const slug_data = data.data[0].permalinks
                const slug_id = data.data[0].slug_id

                set_slug_data(slug_data)
                get_author_data(slug_id)
                get_category_data(slug_id)
                get_tag_data(slug_id)
                
            }else {
                const error_data = responseData;
                console.error('Failed to fetch roles:', error_data);
    
                const errorMessage = error_data.error || "Something went wrong";
                show_toast("error", `Error: ${errorMessage}`);
            }

        } catch (error) {
            console.error("Error in domain_slug_value:", error);
        }
    }, 500); // Delay execution by 500ms
}







function set_slug_data(slug_data){

    console.log(slug_data,'1')

    const permalink_pattern = slug_data
    // Hide all the permalink dropdowns initially
    const dropdown_ids = [
        'minute_permalink', 'hour_permalink', 'day_permalink',
        'month_permalink', 'year_permalink', 'category_permalink',
        'second_permalink', 'author_permalink'
    ];
    dropdown_ids.forEach(id => {
        document.getElementById(id).style.display = 'none';
    });

    // Show the relevant dropdowns based on the permalink pattern
    if (permalink_pattern.includes('minute')) {
        document.getElementById('minute_permalink').style.display = 'block';
    }
    if (permalink_pattern.includes('hour')) {
        document.getElementById('hour_permalink').style.display = 'block';
    }
    if (permalink_pattern.includes('day')) {
        document.getElementById('day_permalink').style.display = 'block';
    }
    if (permalink_pattern.includes('monthnum')) {
        document.getElementById('month_permalink').style.display = 'block';
    }
    if (permalink_pattern.includes('year')) {
        document.getElementById('year_permalink').style.display = 'block';
    }
    if (permalink_pattern.includes('category')) {
        document.getElementById('category_permalink').style.display = 'block';
    }
    if (permalink_pattern.includes('second')) {
        document.getElementById('second_permalink').style.display = 'block';
    }
    if (permalink_pattern.includes('author')) {
        document.getElementById('author_permalink').style.display = 'block';
    }
}