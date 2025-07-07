



// set_domain_dropdown
function set_domain_dropdown(domain_data){
    domain_data.then((response) => {
        const domain_data = response.data || [];  // Ensure data is loaded
        console.log(domain_data)
        const selectElement = document.querySelector('[name="ai_domain_data"]');
        
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
            const selectedSlugId = selectElement.value;
            console.log('Selected Slug ID:', selectedSlugId);
            const domain_input = document.querySelector("input[name='ai_domain_slug_id']");
            domain_input.value = selectedSlugId;

            get_author_data_ai(selectedSlugId)
            get_category_data_ai(selectedSlugId)
            get_tag_data_ai(selectedSlugId)

        });

     

    }) 

};




function get_author_data_ai(domain_slug_id){

    const author_data = get_data_api(list_author_url, domain_slug_id)    
    //set_author_dropdown
    set_author_dropdown_ai(author_data)
}

function get_category_data_ai(domain_slug_id){

    const category_data = get_data_api(list_category_url, domain_slug_id)    
    //set_category_dropdown
    set_category_dropdown_ai(category_data)
}

function get_tag_data_ai(domain_slug_id){

    const tag_data = get_data_api(list_tag_url, domain_slug_id)    
    //set_tag_dropdown
    set_tag_dropdown_ai(tag_data)
}





// article_type
document.addEventListener('DOMContentLoaded', function () {
    
    article_type_data.then((response) => {
        const article_type_data = response.data || [];  // Ensure data is loaded
        console.log(article_type_data)
        const selectElement = document.querySelector('[name="article_type_data"]');

        const inputs = selectElement.querySelectorAll("input, textarea, select"); // Capture all input types

        // Clear existing options
        selectElement.innerHTML = '';

        // Add a default "Select" option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select';
        defaultOption.selected = true;
        defaultOption.disabled = true;
        selectElement.appendChild(defaultOption);

        // Populate the dropdown with the article_type
        article_type_data.forEach((article_type) => {
            const option = document.createElement('option');
            option.value = article_type.slug_id; // Use appropriate key for the value
            option.textContent = article_type.title; // Use appropriate key for the label
            selectElement.appendChild(option);
        });

        // set slug_id in add time
        selectElement.addEventListener('change', function () {
            const selectedSlugId = selectElement.value;
            console.log('Selected Slug ID:', selectedSlugId);

            const article_type_input = document.querySelector("input[name='article_type_id']");
            article_type_input.value = selectedSlugId;

            // get article type fields
            const article_type_field_api_url = `${get_article_type_fields}${selectedSlugId}` 
            // get_article_type_field_data(article_type_field_api_url)
            // createSupportiveVariableButtons(selectedSlugId);
            get_prompt_data(selectedSlugId)
            
        });


        setTimeout(() => {
            // set slug_id in update time
            if (set_article_type_id) {

                const options = selectElement.querySelectorAll('option');
                options.forEach(option => {
                    if (option.value === set_article_type_id) {
                        option.selected = true;
                    }
                });

                // Additionally, set the input field's value
                const article_type_input = document.querySelector("input[name='article_type_id']");
                article_type_input.value = set_article_type_id;

                // get article type fields
                const api_url = `${get_article_type_fields}${set_article_type_id}` 
                // get_article_type_field_data(api_url)

                setTimeout(() => {
                    get_prompt_data(selectedSlugId)

                    // createSupportiveVariableButtons(set_article_type_id);
                }, 500);
                
            }
        }, 100);


    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

});



function get_prompt_data(article_type_slug_id){
    // const urlParams = new URLSearchParams(window.location.search);
    // const article_type_slug_id = urlParams.get("article_type_slug_id");
    const searchParams = article_type_slug_id;

    const prompt_data = get_data_api(list_prompt_url, null, searchParams)    
    // const prompt_data = get_data_api(list_prompt_url)    
    set_prompt_dropdown(prompt_data)
}


// set_prompt_dropdown
function set_prompt_dropdown(prompt_data){
    prompt_data.then((response) => {
        const prompt_data = response.data || [];  // Ensure data is loaded
        console.log(prompt_data)
        const selectElement = document.querySelector('[name="prompt_data"]');

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
        prompt_data.forEach((prompt) => {
            const option = document.createElement('option');
            option.value = prompt.slug_id; // Use appropriate key for the value
            option.textContent = prompt.name; // Use appropriate key for the label
            selectElement.appendChild(option);
        });



        function setAIControlledCheckboxes(supportivePromptJsonData) {
            alert('000')
            const wrapper = document.getElementById("ai-checkbox-wrapper");
            wrapper.innerHTML = "";  // Clear previous content
            alert(wrapper)
            const relatedDivMap = {
                "is_wp_authors_selected_by_ai": "author_div_id",
                "is_wp_categories_selected_by_ai": "category_div_id",
                "is_wp_tags_selected_by_ai": "tag_div_id"
            };

            const fields = Object.entries(supportivePromptJsonData)
                .filter(([key]) => key.startsWith("supportive_prompt_") && key.endsWith("_id"))
                .map(([key, value]) => {
                    const shortKey = key.replace("supportive_prompt_", "").replace("_id", "");
                    const labelText = shortKey.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
                    return {
                        id: `is_${shortKey}`,
                        label: labelText,
                        checked: !!value,
                        name: `is_${shortKey}`
                    };
                });

            for (let i = 0; i < fields.length; i += 2) {
                const rowDiv = document.createElement("div");
                rowDiv.className = "flex flex-col md:flex-row items-start gap-3";

                [fields[i], fields[i + 1]].forEach(field => {
                    if (!field) return;

                    const fieldDiv = document.createElement("div");
                    fieldDiv.className = "flex flex-col md:flex-row w-full items-start gap-3 p-[10px] border border-gray-300 rounded-lg";

                    const checkbox = document.createElement("input");
                    checkbox.type = "checkbox";
                    checkbox.id = field.id;
                    checkbox.name = field.name;
                    checkbox.checked = field.checked;
                    checkbox.disabled = !field.checked;

                    checkbox.className = "w-4 h-4 border border-gray-300 rounded-sm hover:border-indigo-500 hover:bg-indigo-100 checked:bg-no-repeat checked:bg-center checked:border-indigo-500 checked:bg-indigo-900";

                    const label = document.createElement("label");
                    label.htmlFor = field.id;
                    label.className = "text-sm font-medium text-gray-900 w-full flex items-center";
                    label.textContent = field.label;

                    // Handle show/hide on checkbox change
                    checkbox.addEventListener("change", () => {
                        const targetDivId = relatedDivMap[checkbox.id];
                        if (targetDivId) {
                            const relatedDiv = document.getElementById(targetDivId);
                            if (relatedDiv) {
                                relatedDiv.classList.toggle("hidden", checkbox.checked);
                            }
                        }
                    });

                    // Initial show/hide setup
                    const initDivId = relatedDivMap[checkbox.id];
                    if (initDivId) {
                        const relatedDiv = document.getElementById(initDivId);
                        if (relatedDiv) {
                            relatedDiv.classList.toggle("hidden", checkbox.checked);
                        }
                    }

                    fieldDiv.appendChild(checkbox);
                    fieldDiv.appendChild(label);
                    rowDiv.appendChild(fieldDiv);
                });

                wrapper.appendChild(rowDiv);
            }
        }



        // set slug_id in add time
        selectElement.addEventListener('change', function () {
            const selectedSlugId = selectElement.value;
            console.log('Selected Slug ID:', selectedSlugId);
            const prompt_input = document.querySelector("input[name='prompt_slug_id']");
            prompt_input.value = selectedSlugId;


            // Find full prompt data from prompt_data array
            const selectedPrompt = prompt_data.find(p => p.slug_id === selectedSlugId);
            console.log('Selected Prompt Object:', selectedPrompt);


            // Example: access supportive_prompt_json_data if it exists
            if (selectedPrompt && selectedPrompt.supportive_prompt_json_data) {
                console.log('Supportive Prompt JSON Data:', selectedPrompt.supportive_prompt_json_data);

                // create a dropdwon
                setAIControlledCheckboxes(selectedPrompt.supportive_prompt_json_data)
            }



        });



    }) 

};










// set_author_dropdown_ai
function set_author_dropdown_ai(author_data){
    author_data.then((response) => {
        const author_data = response.data || [];  // Ensure data is loaded
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

            const author_input = document.querySelector("input[name='author_slug_id_ai']");
            author_input.value = selectedSlugId;

        });



    }) 

};




// category
function set_category_dropdown_ai(category_data) {
    
    category_data.then((response) => {
        // Access article_type_fields once the promise is resolved
        const categories = response.data || [];  // Ensure data is loaded
        
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
                selected_category_ai();

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
            selected_category_ai()
        }

        // set data for api
        function selected_category_ai() {
            console.log('Selected cat Types:', categories_ids);
            alert(categories_ids)

            const article_type_field_input = document.querySelector("input[name='category_slug_id_ai']");
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
function set_tag_dropdown_ai(tag_data) {
    
    tag_data.then((response) => {
        // Access article_type_fields once the promise is resolved
        const categories = response.data || [];  // Ensure data is loaded
        console.log(categories, '0w');
        
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
                selected_category_ai();

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
            selected_category_ai()
        }

        // set data for api
        function selected_category_ai() {
            console.log('Selected cat Types:', categories_ids);
            
            const article_type_field_input = document.querySelector("input[name='tag_slug_id_ai']");
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
