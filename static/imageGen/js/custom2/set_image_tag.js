



// get dropdown value api
async function get_image_tag_api() {
    try {

        const access_token = localStorage.getItem("access_token");
        
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");

        const query_params = new URLSearchParams();

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }

        const response = await fetch(`${list_image_tag_url}?${query_params.toString()}`, {
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
                
            set_image_tag_api(data)


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

// call 
get_image_tag_api()




// Function to populate the dropdown
function set_image_tag_api(data) {
    const selectElement = document.getElementById("palleon-image-tags");

    if (!selectElement) {
        console.error("Dropdown element not found.");
        return;
    }

    selectElement.innerHTML = ``;

    data.data.forEach(obj => {
        const option = document.createElement("option");
        option.value = obj.slug_id; // Assuming each obj has an 'id' field
        option.textContent = obj.name; // Assuming each obj has a 'obj_name' field
        selectElement.appendChild(option);
    });
    
}
