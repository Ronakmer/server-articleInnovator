

// add api 
async function add_api(api_url, data, redirect_url) {

    const access_token = localStorage.getItem("access_token");

    const workspace_slug_id = localStorage.getItem("workspace_slug_id");

    if (!data.has("workspace_slug_id")) {
        // data.append("workspace_slug_id", workspace_slug_id);   
        if(workspace_slug_id){
            data.append("workspace_slug_id", workspace_slug_id);
        }
    }


    try {
        // Perform the API call
        const response = await fetch(api_url, {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,

            },
            // body: JSON.stringify(data),
            body: data,
        });
        

        const responseData = await response.json();

        check_authentication_error(responseData)

        
        if (response.ok) {
            // Handle successful response
            const data = responseData;

            
            console.log(data)
            show_toast("success", `${data.message}`);

            // Redirect or show a success message (for domain only)
            if(api_url === add_domain_url) {
                progress_bar_page_url += `?workspace_slug_id=${workspace_slug_id}&domain_slug_id=${data.data.slug_id}`;
                window.location.href = progress_bar_page_url
            }

            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    window.location.href = redirect_url;
                }, 1000);
            }

        } else {
            
            const error_data = responseData;

            console.log(error_data)
            // Show api error
            var error_message = error_message_data(error_data);
            

            // Show the toast
            show_toast("error", `Error: ${error_message}`);
        
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("Network error. Please try again later");
    }
}


