

// get dropdown value api
async function get_image_template_api(slug_id=NaN) {
    try {

        const access_token = localStorage.getItem("access_token");
        
        const searchInput = document.getElementById('palleon-template-search-keyword-tag');

        const filters = {
            search: searchInput ? searchInput.value : '',
        
        };


        if (!access_token) {
            console.error("Missing access token.");
            show_toast("error", "Authentication required. Please log in again.");
            return;
        }

        const workspace_slug_id = localStorage.getItem("workspace_slug_id");

        const query_params = new URLSearchParams({
            ...filters,
        });

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }
        if (slug_id) {
            query_params.append("slug_id", slug_id);
        }

        const response = await fetch(`${list_image_template_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('fetched successfully image_template :', data);
            
            console.log(data,'xx')
            set_image_template_api(data)
            set_template_grid(data)


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




// Event listener for the search button
document.getElementById("palleon-template-search").addEventListener("click", function() {
    const selectElement = document.getElementById("palleon-templates-menu");
    const selectedSlugId = selectElement ? selectElement.value : null;

    get_image_template_api(selectedSlugId);
});



// Function to populate the dropdown
function set_image_template_api(data) {
    const selectElement = document.getElementById("palleon-templates-menu");

    if (!selectElement) {
        console.error("Dropdown element not found.");
        return;
    }

    selectElement.innerHTML = `<option value="" disabled selected>Select</option>`;

    data.data.forEach(obj => {
        const option = document.createElement("option");
        option.value = obj.slug_id; // Assuming each obj has an 'id' field
        option.textContent = obj.name; // Assuming each obj has a 'obj_name' field
        selectElement.appendChild(option);
    });
    
}





// Function to populate the templates grid
function set_template_grid(responseData) {
    const gridContainer = document.getElementById("palleon-templates-grid");
    const noImageElement = document.getElementById("palleon-all-templates-noimg");

    if (!gridContainer) {
        console.error("Grid container not found.");
        return;
    }

    // If no data found, show the "Nothing found" message
    if (!responseData || responseData.image_templates.length === 0) {
        noImageElement.classList.remove('d-none');
        gridContainer.innerHTML = '';
        return;
    } else {
        noImageElement.classList.add('d-none');
    }

    // Clear previous content before adding new templates
    gridContainer.innerHTML = '';

    // Loop through the image_templates data and populate the grid
    responseData.data.forEach(obj => {
        const gridItem = document.createElement("div");
        gridItem.classList.add("grid-item");
        gridItem.setAttribute("data-keyword", obj.name);
        gridItem.setAttribute("data-category", obj.image_template_category_id_data.join(', '));

        const favoriteBtn = document.createElement("div");
        favoriteBtn.classList.add("template-favorite");
        favoriteBtn.innerHTML = `
            <button type="button" class="palleon-btn-simple star" data-templateid="${obj.slug_id}">
                <span class="material-icons">star_border</span>
            </button>
        `;

        const masonryItemInner = document.createElement("div");
        masonryItemInner.classList.add("palleon-masonry-item-inner", "palleon-select-template");
        masonryItemInner.setAttribute("data-json", `${list_image_template_url}?slug_id=${obj.slug_id}`);
        masonryItemInner.setAttribute("data-title", obj.name);
        masonryItemInner.setAttribute("data-image_tags", obj.image_tag_id_data.join(', '));

        const imgWrap = document.createElement("div");
        imgWrap.classList.add("palleon-img-wrap");

        // Loader effect
        const imgLoader = document.createElement("div");
        imgLoader.classList.add("palleon-img-loader");
        imgWrap.appendChild(imgLoader);

        const img = document.createElement("img");
        img.classList.add("lazy");
        img.setAttribute("data-src", obj.template_image_path);
        img.setAttribute("src", obj.template_image_path);
        img.setAttribute("title", obj.name);
        img.style.opacity = "0"; // Initially hide the image

        // Show loader until the image fully loads
        img.onload = function () {
            imgLoader.style.display = "none"; // Hide loader
            img.style.opacity = "1"; // Show image with fade-in effect
            img.style.transition = "opacity 0.3s ease-in-out"; // Smooth transition
        };

        // Handle broken images
        img.onerror = function () {
            imgLoader.style.display = "none"; // Hide loader
            img.src = "default-placeholder.png"; // Set a placeholder image if loading fails
        };

        imgWrap.appendChild(img);

        const masonryItemDesc = document.createElement("div");
        masonryItemDesc.classList.add("palleon-masonry-item-desc");
        masonryItemDesc.textContent = obj.name;

        masonryItemInner.appendChild(imgWrap);
        masonryItemInner.appendChild(masonryItemDesc);

        gridItem.appendChild(favoriteBtn);
        gridItem.appendChild(masonryItemInner);

        gridContainer.appendChild(gridItem);
    });
}



// call 
get_image_template_api()











