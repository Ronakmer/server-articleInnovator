

// article_type_field
document.addEventListener('DOMContentLoaded', function () {
    
    article_type_field_data.then((response) => {
        // Access article_type_fields once the promise is resolved
        const categories = response.article_type_fields || [];  // Ensure data is loaded
        console.log(categories, '0w');

        // const categories = [
        //     { slug_id: 1, name: 'text', count: 15 },
        //     { slug_id: 2, name: 'textarea', count: 10 },
        //     { slug_id: 3, name: 'text', count: 8 },
        //     { slug_id: 4, name: 'Category 4', count: 12 },
        //     { slug_id: 5, name: 'Category 5', count: 20 },
        // ];
        
        const input = document.getElementById('article_type_fields_input');
        const dropdown = document.getElementById('article_type_field_dropdown');
        const selectedContainer = document.getElementById('selected_article_type_fields');
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
                alert(category.slug_id)
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
                selected_article_type_field();

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
            selected_article_type_field()
        }

        // set data for api
        function selected_article_type_field() {
            console.log('Selected Prompt Types:', categories_ids);
            
            const article_type_field_input = document.querySelector("input[name='article_type_field']");
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
            if (!e.target.closest('.article_type_field_search')) {
                dropdown.classList.add('hidden');
            }
        });

        // set data in update time
        setTimeout(() => {

            if(set_article_type_field_slug_id){
                console.log(set_article_type_field_slug_id,'r0')
                const slug_ids = set_article_type_field_slug_id.split(', ');

                console.log(slug_ids,'0.')
                slug_ids.forEach(slug_id => {
                    // Find the category by slug_id and select it
                    const category = categories.find(c => c.slug_id == slug_id);
                    if (category) {
                        toggleCategory(category.slug_id, true);  // Mark as selected

                    }
                });
            }
        }, 100);


    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

});



// color
document.addEventListener('DOMContentLoaded', function () {
    
    color_detail_data.then((response) => {
        const color_data = response.colors || [];  // Ensure data is loaded
        console.log(color_data)
        const selectElement = document.querySelector('[name="color_data"]');

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
        color_data.forEach((color) => {
            const option = document.createElement('option');
            option.value = color.slug_id; // Use appropriate key for the value
            option.textContent = color.bg_color; // Use appropriate key for the label
            selectElement.appendChild(option);
        });

        // set slug_id in add time
        selectElement.addEventListener('change', function () {
            const selectedSlugId = selectElement.value;
            console.log('Selected Slug ID:', selectedSlugId);

            const color_input = document.querySelector("input[name='color']");
            color_input.value = selectedSlugId;

        });

        setTimeout(() => {
            // set slug_id in update time
            if (set_color_slug_id) {

                const options = selectElement.querySelectorAll('option');
                options.forEach(option => {
                    if (option.value === set_color_slug_id) {
                        option.selected = true;
                        // document.getElementById(`set_manager_${managerId}`).click();

                    }
                });

                // Additionally, set the color input field's value
                const color_input = document.querySelector("input[name='color']");
                color_input.value = set_color_slug_id;
            }
        }, 100);


    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

});

