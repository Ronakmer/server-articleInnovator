



// Delete author API
function delete_author_api(slug_id, new_author_json) {
    const new_author = JSON.parse(new_author_json.replace(/&quot;/g, '"'));
    console.log(new_author, '///////////////////');

    const api_url = `${delete_author_url}${slug_id}`;
    const current_page_url = window.location.href;
    const domain_slug_id = current_page_url.split('/').pop();

    author_delete_toast(api_url, slug_id, new_author, domain_slug_id);
}

// Function to show the delete confirmation toast
function author_delete_toast(api_url, slug_id, new_author, domain_slug_id) {
    let inputOptions = {};
    let defaultInputValue = "";

    if (Array.isArray(new_author) && new_author.length > 0) {
        console.log(new_author, 'new_author');
        inputOptions = new_author.reduce((options, item) => {
            options[item.username] = item.username;
            return options;
        }, {});

        defaultInputValue = new_author[0].username;
    }

    Swal.fire({
        title: "Are you sure?",
        text: `You won't be able to revert this! Deleting author with ID: ${slug_id}.`,
        input: 'select',
        inputOptions: inputOptions,
        inputValue: defaultInputValue,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
    }).then((result) => {
        if (result.isConfirmed) {
            const selected_author = result.value; // Get selected author name from dropdown

            if (selected_author) {
                author_delete_api(api_url, slug_id, domain_slug_id, selected_author);
            } else {
                Swal.fire("Error", "Please select an author before proceeding.", "error");
            }
        }
    });
}










// author delete api
async function author_delete_api(api_url, slug_id, domain_slug_id=NaN, selected_author) {
    try {

        const access_token = localStorage.getItem("access_token");
        
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");
        const query_params = new URLSearchParams();

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }
        if (domain_slug_id) {
            query_params.append("domain_slug_id", domain_slug_id);
        }
        if (selected_author) {
            query_params.append("new_author", selected_author);
        }

        // Perform the GET API call
        const response = await fetch(`${api_url}?${query_params.toString()}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
                'slug_id': `${slug_id}`,
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('Roles fetched successfully:', data);

            show_toast("success", `${data.message}`);
            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    window.location.reload(); 
                }, 1000);
            }

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

