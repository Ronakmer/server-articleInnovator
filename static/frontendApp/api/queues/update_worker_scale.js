// update_worker_scale API
async function update_worker_scale(queue_name) {
    const access_token = localStorage.getItem("access_token");
    const workspace_slug_id = localStorage.getItem("workspace_slug_id");

    const worker_scale_id = document.getElementById('worker_scale_id'); 
    const formData = new FormData();  // Changed variable name to formData

    // Make sure workspace_slug_id is appended to FormData
    if (workspace_slug_id) {
        formData.append("workspace_slug_id", workspace_slug_id);
    }

    // Append queue_name and worker_scale_id if both exist
    if (queue_name && worker_scale_id) {
        formData.append("queue_name", queue_name);
        formData.append("worker_count", worker_scale_id.value);
    }

    try {
        // Perform the API call
        const response = await fetch(update_worker_scale_url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${access_token}`,
            },
            body: formData,  // Use formData directly
        });

        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            const data = responseData;  // Get the response data

            console.log(data);
            show_toast("success", `${data.message}`);

            // Reload page after 1 second
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            const error_data = responseData;  // Get error data

            console.log(error_data);
            // Show API error
            var error_message = error_message_data(error_data);

            // Show the toast with error message
            show_toast("error", `Error: ${error_message}`);
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later.");
    }
}
