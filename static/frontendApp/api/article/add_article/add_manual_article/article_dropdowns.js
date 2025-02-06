
let temp_domain_slug_id = '';

// set_domain_dropdown
function set_domain_dropdown(domain_data){
    console.log(domain_data,'***')
    domain_data.then((response) => {
        const domain_data = response.domains || [];  // Ensure data is loaded
        console.log(domain_data)
        const selectElement = document.querySelector('[name="manual_domain_data"]');
        if(!selectElement){
            alert(0)
        }
        // Clear existing options
        selectElement.innerHTML = '';

        // Add a default "Select" option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select';
        defaultOption.selected = true;
        defaultOption.disabled = true;
        selectElement.appendChild(defaultOption);

        // Populate the dropdown with the colors
        domain_data.forEach((domain) => {
            const option = document.createElement('option');
            option.value = domain.slug_id; // Use appropriate key for the value
            option.textContent = domain.name; // Use appropriate key for the label
            selectElement.appendChild(option);
        });

        // set slug_id in add time
        selectElement.addEventListener('change', function () {
            temp_domain_slug_id = selectElement.value;
            console.log('Selected Slug ID:', temp_domain_slug_id);

            const domain_input = document.querySelector("input[name='manual_domain_slug_id']");
            domain_input.value = temp_domain_slug_id;

        });

        // // set slug_id in update time
        // if (set_color_slug_id) {

        //     const options = selectElement.querySelectorAll('option');
        //     options.forEach(option => {
        //         if (option.value === set_color_slug_id) {
        //             option.selected = true;
        //             // document.getElementById(`set_manager_${managerId}`).click();

        //         }
        //     });

        //     // Additionally, set the color input field's value
        //     const color_input = document.querySelector("input[name='color']");
        //     color_input.value = set_color_slug_id;
        // }


    }) 

};









// set_author_dropdown
function set_author_dropdown(author_data){
    author_data.then((response) => {
        const author_data = response.authors || [];  // Ensure data is loaded
        console.log(author_data)
        const selectElement = document.querySelector('[name="author_data"]');

        // Clear existing options
        selectElement.innerHTML = '';

        // Add a default "Select" option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select';
        defaultOption.selected = true;
        defaultOption.disabled = true;
        selectElement.appendChild(defaultOption);

        // Populate the dropdown with the colors
        author_data.forEach((author) => {
            const option = document.createElement('option');
            option.value = author.slug_id; // Use appropriate key for the value
            option.textContent = author.username; // Use appropriate key for the label
            selectElement.appendChild(option);
        });

        // set slug_id in add time
        selectElement.addEventListener('change', function () {
            const selectedSlugId = selectElement.value;
            console.log('Selected Slug ID:', selectedSlugId);

            const author_input = document.querySelector("input[name='author_slug_id']");
            author_input.value = selectedSlugId;

        });

        // // set slug_id in update time
        // if (set_color_slug_id) {

        //     const options = selectElement.querySelectorAll('option');
        //     options.forEach(option => {
        //         if (option.value === set_color_slug_id) {
        //             option.selected = true;
        //             // document.getElementById(`set_manager_${managerId}`).click();

        //         }
        //     });

        //     // Additionally, set the color input field's value
        //     const color_input = document.querySelector("input[name='color']");
        //     color_input.value = set_color_slug_id;
        // }


    }) 

};








// category
function set_category_dropdown(category_data) {
    
    category_data.then((response) => {
        // Access article_type_fields once the promise is resolved
        const categories = response.categories || [];  // Ensure data is loaded
        console.log(categories, '0w');

        // const categories = [
        //     { slug_id: 1, name: 'text', count: 15 },
        //     { slug_id: 2, name: 'textarea', count: 10 },
        //     { slug_id: 3, name: 'text', count: 8 },
        //     { slug_id: 4, name: 'Category 4', count: 12 },
        //     { slug_id: 5, name: 'Category 5', count: 20 },
        // ];
        
        const input = document.getElementById('category-input');
        const dropdown = document.getElementById('category-dropdown');
        const selectedContainer = document.getElementById('selected-categories');

        var categories_ids = [];

        function createCategoryElement(category) {
            const div = document.createElement('div');
            div.className = 'p-2 hover:bg-gray-100 cursor-pointer';
            div.innerHTML = `
            <label class="flex items-center justify-between">
                <span class="flex items-center">
                    <input type="checkbox" class="mr-2" data-id="${category.slug_id}">
                    ${category.name}
                </span>
                <span class="hidden bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">${category.count}</span>
            </label>
        `;
            return div;
        }

        function createSelectedCategory(category) {
            const span = document.createElement('span');
            span.className = 'relative rounded-lg border border-solid border-gray-200 mr-2 pl-2 pr-4 py-1 flex items-center mb-2';
            span.dataset.slug_id = category.slug_id;
            span.innerHTML = `
                ${category.name}
                    <!-- Close button -->
                    <button class="ml-1.5 text-blue-800 hover:text-blue-900 absolute top-0 right-0 transform -translate-y-1/2 translate-x-1/2 p-1 hover:opacity-90" data-id="${category.slug_id}">
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 0C2.245 0 0 2.245 0 5C0 7.755 2.245 10 5 10C7.755 10 10 7.755 10 5C10 2.245 7.755 0 5 0ZM6.68 6.15C6.825 6.295 6.825 6.535 6.68 6.68C6.605 6.755 6.51 6.79 6.415 6.79C6.32 6.79 6.225 6.755 6.15 6.68L5 5.53L3.85 6.68C3.775 6.755 3.68 6.79 3.585 6.79C3.49 6.79 3.395 6.755 3.32 6.68C3.175 6.535 3.175 6.295 3.32 6.15L4.47 5L3.32 3.85C3.175 3.705 3.175 3.465 3.32 3.32C3.465 3.175 3.705 3.175 3.85 3.32L5 4.47L6.15 3.32C6.295 3.175 6.535 3.175 6.68 3.32C6.825 3.465 6.825 3.705 6.68 3.85L5.53 5L6.68 6.15Z" fill="#DF6137"></path>
                    </svg>
                    </button>
                `;

            // Event listener to remove category when close button is clicked
            span.querySelector('button').addEventListener('click', function () {
                toggleCategory(category.slug_id, false); // Uncheck in dropdown
                // selectedContainer.removeChild(span); // Remove from selected list
                
                // update list Remove the slug_id from categories_ids list
                const index = categories_ids.indexOf(category.slug_id);
                if (index !== -1) {
                    categories_ids.splice(index, 1); // Remove slug_id from categories_ids array
                }

                // Check if the span is still in the selectedContainer before removing
                if (selectedContainer.contains(span)) {
                    selectedContainer.remove(span); // Remove the span from selectedContainer
                }
                selected_category();

            });

            selectedContainer.appendChild(span);
        }


        function toggleCategory(categoryId, selected) {
            const checkbox = dropdown.querySelector(`input[data-id="${categoryId}"]`);
            if (checkbox) {
                checkbox.checked = selected;
            }
            
            if (selected) {
                const category = categories.find(c => c.slug_id == categoryId);

                if (category && !selectedContainer.querySelector(`[data-id="${categoryId}"]`)) {
                    createSelectedCategory(category);
                    console.log(categoryId);
                    categories_ids.push(categoryId);
                }
            } else {
                const selectedCategory = selectedContainer.querySelector(`button[data-id="${categoryId}"]`);
                if (selectedCategory) {
                    selectedCategory.closest('span').remove();
                }
            }
            selected_category()
        }

        // set data for api
        function selected_category() {
            console.log('Selected cat Types:', categories_ids);
            
            const article_type_field_input = document.querySelector("input[name='category_slug_id']");
            article_type_field_input.value = categories_ids;
        }

        categories.forEach(category => {
            
            const categoryElement = createCategoryElement(category);
            dropdown.appendChild(categoryElement);

            const checkbox = categoryElement.querySelector('input[type="checkbox"]');
            checkbox.addEventListener('change', (e) => {
                toggleCategory(category.slug_id, e.target.checked);
            });
        });

        input.addEventListener('focus', () => {
            dropdown.classList.remove('hidden');
        });

        input.addEventListener('input', () => {
            const searchTerm = input.value.toLowerCase();
            Array.from(dropdown.children).forEach(child => {
                const name = child.textContent.toLowerCase();
                child.style.display = name.includes(searchTerm) ? '' : 'none';
            });
        });

        selectedContainer.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON') {
                const categoryId = e.target.getAttribute('data-id');
                toggleCategory(categoryId, false);
            }
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.category-search')) {
                dropdown.classList.add('hidden');
            }
        });

      

    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

};












// tag
function set_tag_dropdown(tag_data) {
    
    tag_data.then((response) => {
        // Access article_type_fields once the promise is resolved
        const categories = response.tags || [];  // Ensure data is loaded
        console.log(categories, '0w');

        // const categories = [
        //     { slug_id: 1, name: 'text', count: 15 },
        //     { slug_id: 2, name: 'textarea', count: 10 },
        //     { slug_id: 3, name: 'text', count: 8 },
        //     { slug_id: 4, name: 'Category 4', count: 12 },
        //     { slug_id: 5, name: 'Category 5', count: 20 },
        // ];
        
        const input = document.getElementById('tag-input');
        const dropdown = document.getElementById('tag-dropdown');
        const selectedContainer = document.getElementById('selected-tag');

        var categories_ids = [];

        function createCategoryElement(category) {
            const div = document.createElement('div');
            div.className = 'p-2 hover:bg-gray-100 cursor-pointer';
            div.innerHTML = `
            <label class="flex items-center justify-between">
                <span class="flex items-center">
                    <input type="checkbox" class="mr-2" data-id="${category.slug_id}">
                    ${category.name}
                </span>
                <span class="hidden bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">${category.count}</span>
            </label>
        `;
            return div;
        }

        function createSelectedCategory(category) {
            const span = document.createElement('span');
            span.className = 'relative rounded-lg border border-solid border-gray-200 mr-2 pl-2 pr-4 py-1 flex items-center mb-2';
            span.dataset.slug_id = category.slug_id;
            span.innerHTML = `
                ${category.name}
                    <!-- Close button -->
                    <button class="ml-1.5 text-blue-800 hover:text-blue-900 absolute top-0 right-0 transform -translate-y-1/2 translate-x-1/2 p-1 hover:opacity-90" data-id="${category.slug_id}">
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 0C2.245 0 0 2.245 0 5C0 7.755 2.245 10 5 10C7.755 10 10 7.755 10 5C10 2.245 7.755 0 5 0ZM6.68 6.15C6.825 6.295 6.825 6.535 6.68 6.68C6.605 6.755 6.51 6.79 6.415 6.79C6.32 6.79 6.225 6.755 6.15 6.68L5 5.53L3.85 6.68C3.775 6.755 3.68 6.79 3.585 6.79C3.49 6.79 3.395 6.755 3.32 6.68C3.175 6.535 3.175 6.295 3.32 6.15L4.47 5L3.32 3.85C3.175 3.705 3.175 3.465 3.32 3.32C3.465 3.175 3.705 3.175 3.85 3.32L5 4.47L6.15 3.32C6.295 3.175 6.535 3.175 6.68 3.32C6.825 3.465 6.825 3.705 6.68 3.85L5.53 5L6.68 6.15Z" fill="#DF6137"></path>
                    </svg>
                    </button>
                `;

            // Event listener to remove category when close button is clicked
            span.querySelector('button').addEventListener('click', function () {
                toggleCategory(category.slug_id, false); // Uncheck in dropdown
                // selectedContainer.removeChild(span); // Remove from selected list
                
                // update list Remove the slug_id from categories_ids list
                const index = categories_ids.indexOf(category.slug_id);
                if (index !== -1) {
                    categories_ids.splice(index, 1); // Remove slug_id from categories_ids array
                }

                // Check if the span is still in the selectedContainer before removing
                if (selectedContainer.contains(span)) {
                    selectedContainer.remove(span); // Remove the span from selectedContainer
                }
                selected_category();

            });

            selectedContainer.appendChild(span);
        }


        function toggleCategory(categoryId, selected) {
            const checkbox = dropdown.querySelector(`input[data-id="${categoryId}"]`);
            if (checkbox) {
                checkbox.checked = selected;
            }
            
            if (selected) {
                const category = categories.find(c => c.slug_id == categoryId);

                if (category && !selectedContainer.querySelector(`[data-id="${categoryId}"]`)) {
                    createSelectedCategory(category);
                    console.log(categoryId);
                    categories_ids.push(categoryId);
                }
            } else {
                const selectedCategory = selectedContainer.querySelector(`button[data-id="${categoryId}"]`);
                if (selectedCategory) {
                    selectedCategory.closest('span').remove();
                }
            }
            selected_category()
        }

        // set data for api
        function selected_category() {
            console.log('Selected cat Types:', categories_ids);
            
            const article_type_field_input = document.querySelector("input[name='tag_slug_id']");
            article_type_field_input.value = categories_ids;
        }

        categories.forEach(category => {
            
            const categoryElement = createCategoryElement(category);
            dropdown.appendChild(categoryElement);

            const checkbox = categoryElement.querySelector('input[type="checkbox"]');
            checkbox.addEventListener('change', (e) => {
                toggleCategory(category.slug_id, e.target.checked);
            });
        });

        input.addEventListener('focus', () => {
            dropdown.classList.remove('hidden');
        });

        input.addEventListener('input', () => {
            const searchTerm = input.value.toLowerCase();
            Array.from(dropdown.children).forEach(child => {
                const name = child.textContent.toLowerCase();
                child.style.display = name.includes(searchTerm) ? '' : 'none';
            });
        });

        selectedContainer.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON') {
                const categoryId = e.target.getAttribute('data-id');
                toggleCategory(categoryId, false);
            }
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.tag-search')) {
                dropdown.classList.add('hidden');
            }
        });

    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

};
