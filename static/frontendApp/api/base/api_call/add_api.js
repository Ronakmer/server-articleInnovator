async function add_api(api_url, data, redirect_url) {
    const access_token = localStorage.getItem("access_token");
    const workspace_slug_id = localStorage.getItem("workspace_slug_id");
    console.log(workspace_slug_id, 'workspace_slug_id');

    if (!data.has("workspace_slug_id") && workspace_slug_id) {
        data.append("workspace_slug_id", workspace_slug_id);
    }

    try {
        const response = await fetch(api_url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${access_token}`,
            },
            body: data,
        });

        const responseData = await response.json();
        check_authentication_error(responseData);

        if (response.ok) {
            console.log(responseData);
            show_toast("success", `${responseData.message}`);

            // Special handling for domain
            if (api_url === add_domain_url) {
                progress_bar_page_url += `?workspace_slug_id=${workspace_slug_id}&domain_slug_id=${responseData.data.slug_id}`;
                window.location.href = progress_bar_page_url;
                return; // stop here
            }

            if (redirect_url) {
                setTimeout(() => {
                    window.location.href = redirect_url;
                }, 1000);
            }

            // Always return the parsed response
            return responseData;

        } else {
            const error_message = error_message_data(responseData);
            show_toast("error", `Error: ${error_message}`);
            return responseData;  // also return the error response
        }

    } catch (error) {
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later");
        return { success: false, message: "Network error" };  // consistent return
    }
}
