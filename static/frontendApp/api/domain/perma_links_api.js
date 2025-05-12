
async function perma_links_api(){

    try {

        const access_token = localStorage.getItem("access_token");
        
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");

        // Get the current URL
        const urlParams = new URLSearchParams(window.location.search);

        // Extract parameters
        const siteUrl = urlParams.get("site_url");
        const wordpress_username = urlParams.get("user_login");
        const wordpress_application_password = urlParams.get("password");

        // Extract domain name from site_url
        const domain_name = siteUrl ? new URL(siteUrl).hostname : "";
                
        const data = new FormData();
        data.append("name", domain_name);
        data.append("wordpress_username", wordpress_username);
        data.append("wordpress_application_password", wordpress_application_password);
        

        const response = await fetch(`${list_perma_links_url}`, {
            method: 'POST',
            headers: {
                // 'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
            body: data,
        });

        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('fetched successfully:', data);

            perma_links(data.data.current_structure)
                

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


// perma_links_api()
// Extract parameters from URL
// const urlParams = new URLSearchParams(window.location.search);
// const siteUrl = urlParams.get("site_url");
// const wordpress_username = urlParams.get("user_login");
// const wordpress_application_password = urlParams.get("password");

// Call API only if all required values are present
if (siteUrl) {
    perma_links_api();
}
