


let selectedCategory = [];
let selectedTag = [];

// find google image api
async function find_google_image_api() {
    try {

        const access_token = localStorage.getItem("access_token");
        
        // const query_params = new URLSearchParams();

        // const api_key = 'D92B03D0EC80405C8DE89B94F9887C8C';
        // const search_type = 'images';
        const query = document.querySelector('.search-keyword').value;
        
        // query_params.append("api_key", api_key);
        // query_params.append("search_type", search_type);
        // query_params.append("q", query);

        const response = await fetch(fetch_google_images_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
            body: JSON.stringify({ query }) // Send query in body
        });

        const responseData = await response.json();

        check_authentication_error(responseData)

        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('fetched successfully:', data);

            // set_google_image_data(data.image_results);
            set_google_image_data(data.data);
                
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








// find_template_category_api
async function find_template_category_api() {
    try {

        const access_token = localStorage.getItem("access_token");
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");
        

        let current_page = 1; // Initialize current page
        const limit = 100; // Number of items per page
        const offset = (current_page - 1) * limit; // Calculate offset based on current page

        const query_params = new URLSearchParams({
            offset,
            limit,
        });

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }

        const response = await fetch(`${list_image_template_category_url}?${query_params.toString()}`, {
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

            
            // Get the select element
            const categorySelect = document.querySelector(".template-category");

            // Clear existing options
            categorySelect.innerHTML = "";

            // Create and add the default disabled option
            const defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.textContent = "Category";
            defaultOption.disabled = true;
            defaultOption.selected = true;
            categorySelect.appendChild(defaultOption);

            // Populate the dropdown with categories
            data.data.forEach(category => {
                const option = document.createElement("option");
                option.value = category.name;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });

            // Add event listener for category selection
            // categorySelect.addEventListener("change", function () {
            //     selectedCategory = categorySelect.value;
            //     if (selectedCategory) {
            //         find_template_by_category_and_tag_api(selectedCategory);
            //     }
            // });
    
            categorySelect.addEventListener("change", function () {
                selectedCategory = categorySelect.value ? [categorySelect.value] : []; // Ensure it’s always an array
                if (selectedCategory.length > 0) {
                    find_template_by_category_and_tag_api(selectedCategory);
                }
            });
            
            
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

find_template_category_api()











// find_template_tag_api
async function find_template_tag_api() {
    try {

        const access_token = localStorage.getItem("access_token");
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");
        

        let current_page = 1; // Initialize current page
        const limit = 100; // Number of items per page
        const offset = (current_page - 1) * limit; // Calculate offset based on current page

        const query_params = new URLSearchParams({
            offset,
            limit,
        });

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

            
            // Get the select element
            const tagSelect = document.querySelector(".template-tag");

            // Clear existing options
            tagSelect.innerHTML = "";

            // Create and add the default disabled option
            const defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.textContent = "tag";
            defaultOption.disabled = true;
            defaultOption.selected = true;
            tagSelect.appendChild(defaultOption);

            // Populate the dropdown with categories
            data.data.forEach(tag => {
                const option = document.createElement("option");
                option.value = tag.name;
                option.textContent = tag.name;
                tagSelect.appendChild(option);
            });

            // Add event listener for tag selection
            // tagSelect.addEventListener("change", function () {
            //     selectedTag = tagSelect.value;
            //     if (selectedTag) {
            //         find_template_by_category_and_tag_api(selectedTag);
            //     }
            // });
    
            tagSelect.addEventListener("change", function () {
                selectedTag = tagSelect.value ? [tagSelect.value] : []; // Ensure it’s always an array
                if (selectedTag.length > 0) {
                    find_template_by_tag_and_tag_api(selectedTag);
                }
            });
            
    
            
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

find_template_tag_api()








// find_template_by_categoryand_tag_api
async function find_template_by_category_and_tag_api(name) {
    try {

        const access_token = localStorage.getItem("access_token");
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");
        


        let current_page = 1; // Initialize current page
        const limit = 100; // Number of items per page
        const offset = (current_page - 1) * limit; // Calculate offset based on current page
    
        const filters = {
            search: name,
        };

        const query_params = new URLSearchParams({
            offset,
            limit,
            ...filters
        });

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }

        const response = await fetch(`${list_image_template_url}?${query_params.toString()}`, {
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
            set_image_template_data(data);
                
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











// generate_single_image_api
async function generate_single_image_api() {

    const access_token = localStorage.getItem("access_token");
    const workspace_slug_id = localStorage.getItem("workspace_slug_id");


   alert(selectedCategory)

    
    if (selectedImages.length === 0) {  
        show_toast("error", "Please select at least one image.");  
        return;  
    }  


    const query = document.querySelector('.search-keyword').value;


    const no_of_images = document.querySelector('.no_of_images').value;
    const data = {
        workspace_slug_id: workspace_slug_id || null,
        categories: JSON.stringify(selectedCategory) || null,
        tags: JSON.stringify(selectedTag) || null,
        image_urls: JSON.stringify(selectedImages),
        no_of_images: parseInt(no_of_images) || 1,
        search_query:query || null,
    };
    

    try {
        // Perform the API call
        const response = await fetch(generate_single_image_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,

            },
            body: JSON.stringify(data),
            // body: data,
        });
        
        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
           
            console.log(data)
            set_generated_images(data)

            show_toast("success", `${data.message}`);


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


