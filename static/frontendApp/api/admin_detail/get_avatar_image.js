

let avatar_image_id = '';


// get_avatar_image_api
async function get_avatar_image_api() {
    try {

        const access_token = localStorage.getItem("access_token");

        const query_params = new URLSearchParams();

        if (query_params) {
            query_params.append("avatar_type", 'profile');
        }
    

        const response = await fetch(`${list_dynamic_avatar_image_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('list_dynamic_avatar_image_url:', data);
            
            set_avatar_image_data(data)

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
get_avatar_image_api()















function set_avatar_image_data(data) {
    // Get the container where the images will be inserted
    const container = document.getElementById('avatar-images-container');

    // Clear any existing content in the container
    container.innerHTML = '';

    // Iterate over the dynamic_avatar_images array and create the HTML elements
    data.dynamic_avatar_images.forEach((obj, index) => {
        const div = document.createElement('div');
        div.classList.add('p-2', 'w-full', 'rounded-lg');
        div.id = `dynamic_avatar_image_div_${index + 1}`;

        const img = document.createElement('img');
        img.classList.add('rounded-lg', 'w-full', 'h-16', 'object-cover', 'avatar-image');
        img.alt = 'Featured Image';

        if (obj.avatar_image) {
            img.src = obj.avatar_image;
            img.setAttribute('data-image-path', obj.avatar_image);
        } else {
            img.src = ''; // Placeholder or default image
        }

        // Add a click event listener to toggle selection
        img.addEventListener('click', function() {
            // Check if the clicked image is already selected
            const isSelected = div.classList.contains('bg-indigo-600');

            // Reset background color for all images
            const allDivs = document.querySelectorAll('.p-2');
            allDivs.forEach(d => {
                d.classList.remove('bg-indigo-600');
            });

            // If the clicked image was not selected, select it
            if (!isSelected) {
                div.classList.add('bg-indigo-600');
                console.log(`Selected image slug_id: ${obj.slug_id}`);
                avatar_image_id = obj.avatar_image;
            } else {
                console.log('Deselected image');
                avatar_image_id = null; // Clear the selection
            }
        });

        div.appendChild(img);
        container.appendChild(div);
    });
}

