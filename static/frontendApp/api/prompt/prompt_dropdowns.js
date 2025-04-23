


// workspace
document.addEventListener('DOMContentLoaded', function () {

    const workspace_div = prompt_form.querySelector('[id="workspace-div"]');

    if(workspace_div){

    
        workspace_data.then((response) => {

            
            const teamMembers = response.data || [];  // Ensure data is loaded
            

            let workspace_ids = [];
            const workspaceInput = document.querySelector('input[name="workspace_id"]'); // Reference to the hidden input


            // set the hidden input value with the workspace_ids as a comma-separated string
            function setWorkspaceInput() {
                workspaceInput.value = workspace_ids.join(',');
            }
            

            const customSelect = document.querySelector('.member_custom_select');
            const selectedItemsContainer = document.querySelector('.member_selected_items');
            const dropdownContainer = document.querySelector('.member_custom_select_dropdown');
            const input = document.querySelector('.member_custom_select input');

            function createTeamMemberElement(member) {
                const div = document.createElement('div');
                div.className = 'px-4 cursor-pointer flex items-center';
                div.innerHTML = `
                    <label class="flex w-full items-center p-2 text-sm rounded-xl mb-1 text-gray-600 bg-white hover:bg-indigo-600/15" id="set_workspace_${member.slug_id}">
                    <input type="checkbox" class="mr-2"> 
                    <img src="${member.logo}" alt="${member.name}" class="w-6 h-6 mr-1 rounded-full">
                    ${member.name}
                    </label>
                    `;
                div.dataset.slug_id = member.slug_id;

                const label = div.querySelector('label');
                const checkbox = div.querySelector('input[type="checkbox"]');

                label.addEventListener('click', function () {
                    if (!checkbox.checked) {
                        checkbox.checked = true;
                        label.classList.add('bg-indigo-600/15');
                        label.classList.remove('bg-white');
                        addMemberToSelectedList(member);
                    } else {
                        checkbox.checked = false;
                        label.classList.remove('bg-indigo-600/15');
                        label.classList.add('bg-white');
                        removeMemberFromSelectedList(member.slug_id);
                    }
                });

                return div;
            }

            function createSelectedItemElement(member) {
                const div = document.createElement('div');
                div.className = 'bg-blue-100 rounded-full relative px-3 py-2 flex items-center text-sm';
                div.innerHTML = `
                    <img src="${member.logo}" alt="${member.name}" class="w-4 h-4 rounded-full mr-1">
                    <span class="mr-1">${member.name}</span>
                    <button class="absolute top-1 -right-0 hover:opacity-90" data-id="${member.slug_id}">
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 0C2.245 0 0 2.245 0 5C0 7.755 2.245 10 5 10C7.755 10 10 7.755 10 5C10 2.245 7.755 0 5 0ZM6.68 6.15C6.825 6.295 6.825 6.535 6.68 6.68C6.605 6.755 6.51 6.79 6.415 6.79C6.32 6.79 6.225 6.755 6.15 6.68L5 5.53L3.85 6.68C3.775 6.755 3.68 6.79 3.585 6.79C3.49 6.79 3.395 6.755 3.32 6.68C3.175 6.535 3.175 6.295 3.32 6.15L4.47 5L3.32 3.85C3.175 3.705 3.175 3.465 3.32 3.32C3.465 3.175 3.705 3.175 3.85 3.32L5 4.47L6.15 3.32C6.295 3.175 6.535 3.175 6.68 3.32C6.825 3.465 6.825 3.705 6.68 3.85L5.53 5L6.68 6.15Z" fill="#DF6137"/>
                    </svg>
                    </button>
                    `;
                return div;
            }


            function addMemberToSelectedList(member) {
                // Check if the member is already added by slug_id
                const isAlreadySelected = [...selectedItemsContainer.children].some(item => {
                    return item.querySelector('button').dataset.id === member.slug_id;
                });
            
                if (!isAlreadySelected) {
                    // If not already selected, create and append the member
                    const selectedItem = createSelectedItemElement(member);
                    selectedItemsContainer.appendChild(selectedItem);
                    input.value = ''; // Clear the input
                    input.focus(); // Refocus the input

                    // set slug_id in list
                    workspace_ids.push(member.slug_id);
                    setWorkspaceInput();


                } else {
                    console.log(`Member with slug_id ${member.slug_id} is already selected.`);
                }
            }
            

            function removeMemberFromSelectedList(slug_id) {
                // Remove from selectedItemsContainer
                const itemToRemove = selectedItemsContainer.querySelector(`button[data-id="${slug_id}"]`);
                if (itemToRemove) {
                    itemToRemove.closest('div').remove();
                    input.focus();

                    // remove slug_id in list
                    workspace_ids = workspace_ids.filter(id => id !== slug_id);
                    setWorkspaceInput();

                }
            
                // Remove from dropdownContainer
                const memberElement = dropdownContainer.querySelector(`[data-slug_id="${slug_id}"]`);
                if (memberElement) {
                    const checkbox = memberElement.querySelector('input[type="checkbox"]');
                    if (checkbox) {
                        checkbox.checked = false;
                    }
            
                    const label = memberElement.querySelector('label');
                    if (label) {
                        label.classList.remove('bg-indigo-600/15');
                        label.classList.add('bg-white');
                    }
                }
            }

            if(dropdownContainer){

                teamMembers.forEach(member => {
                    const memberElement = createTeamMemberElement(member);
                    dropdownContainer.appendChild(memberElement);
                });
            }

            if(customSelect){

                input.addEventListener('focus', () => {
                    customSelect.classList.add('active');
                });
            }

            if(input){

                input.addEventListener('input', () => {
                    const searchTerm = input.value.toLowerCase();
                    Array.from(dropdownContainer.children).forEach(child => {
                        const name = child.querySelector('label').textContent.toLowerCase();
                        child.style.display = name.includes(searchTerm) ? '' : 'none';
                    });
                });
            }

            
            // update time set data
            // setTimeout(() => {
            
            //     if (typeof set_workspace_ids === 'string') {
            //         if (set_workspace_ids.includes(',')) {
            //             // If it's a comma-separated list, split it and trim each item
            //             set_workspace_ids = set_workspace_ids.split(',').map(item => item.trim());
            //         } else {
            //             // If it's a single ID, wrap it in an array
            //             set_workspace_ids = [set_workspace_ids.trim()];
            //         }
            //     }
                
                
            //     // update time set data
            //     if (Array.isArray(set_workspace_ids)) {
            //         set_workspace_ids.forEach(workspaceId => {
            //             console.log(`Workspace ID: ${workspaceId}`);
            //             document.getElementById(`set_workspace_${workspaceId}`).click();

            //         });
            //     } else {
            //         console.error('set_workspace is not an array:', set_workspace_ids);
            //     }
            // }, 100);


            if(input){

                // Add keydown event listener for backspace functionality
                input.addEventListener('keydown', (e) => {
                    if (e.key === 'Backspace' && input.value === '' && selectedItemsContainer.lastChild) {
                        const lastSelectedItem = selectedItemsContainer.lastChild;
                        const id = lastSelectedItem.querySelector('button').dataset.id;
                        console.log(id,'89')
                        removeMemberFromSelectedList(id);
                    }
                });
            }

            if(selectedItemsContainer){

                // Use event delegation for close button clicks
                selectedItemsContainer.addEventListener('click', (e) => {
                    if (e.target.closest('button')) {
                        const id = e.target.closest('button').dataset.id;
                        removeMemberFromSelectedList(id);
                    }
                });
                setWorkspaceInput();
            }

            if(customSelect){

                document.addEventListener('click', (e) => {
                    if (!customSelect.contains(e.target)) {
                        customSelect.classList.remove('active');
                    }
                });
            }



        }) 

    
        .catch((error) => {
            console.error('Error:', error);
        });
    }

});











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
            const variables_api_url = `${list_variables_url}?article_type_slug_id=${selectedSlugId}`;
            get_article_type_field_data(article_type_field_api_url)
            // get_variables_data(variables_api_url)
            createSupportiveVariableButtons(selectedSlugId);
            
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
                get_article_type_field_data(api_url)

                setTimeout(() => {

                    createSupportiveVariableButtons(set_article_type_id);
                }, 500);
                
            }
        }, 100);


    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

});








// // api_model
// document.addEventListener('DOMContentLoaded', function () {
    
//     ai_configuration_data.then((response) => {
//         // Access api_models once the promise is resolved
//         const categories = response.data || [];  // Ensure data is loaded

        
//         const input = document.getElementById('api_models_input');
//         const dropdown = document.getElementById('api_model_dropdown');
//         const selectedContainer = document.getElementById('selected_api_models');
//         var categories_ids = [];

//         function createCategoryElement(category) {
//             const div = document.createElement('div');
//             div.className = 'p-2 hover:bg-gray-100 cursor-pointer';
//             div.innerHTML = `
//             <label class="flex items-center justify-between">
//                 <span class="flex items-center">
//                     <input type="checkbox" class="mr-2" data-id="${category.api_model}">
//                     ${category.api_model}
//                 </span>
//                 <span class="hidden bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">${category.count}</span>
//             </label>
//         `;
//             return div;
//         }

//         function createSelectedCategory(category) {
//             const span = document.createElement('span');
//             span.className = 'relative rounded-lg border border-solid border-gray-200 mr-2 pl-2 pr-4 py-1 flex items-center mb-2';
//             span.dataset.api_model = category.api_model;
//             span.innerHTML = `
//                 ${category.api_model}
//                 <!-- Close button -->
//                 <button class="ml-1.5 text-blue-800 hover:text-blue-900 absolute top-0 right-0 transform -translate-y-1/2 translate-x-1/2 p-1 hover:opacity-90" data-id="${category.api_model}">
//                 <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
//                 <path d="M5 0C2.245 0 0 2.245 0 5C0 7.755 2.245 10 5 10C7.755 10 10 7.755 10 5C10 2.245 7.755 0 5 0ZM6.68 6.15C6.825 6.295 6.825 6.535 6.68 6.68C6.605 6.755 6.51 6.79 6.415 6.79C6.32 6.79 6.225 6.755 6.15 6.68L5 5.53L3.85 6.68C3.775 6.755 3.68 6.79 3.585 6.79C3.49 6.79 3.395 6.755 3.32 6.68C3.175 6.535 3.175 6.295 3.32 6.15L4.47 5L3.32 3.85C3.175 3.705 3.175 3.465 3.32 3.32C3.465 3.175 3.705 3.175 3.85 3.32L5 4.47L6.15 3.32C6.295 3.175 6.535 3.175 6.68 3.32C6.825 3.465 6.825 3.705 6.68 3.85L5.53 5L6.68 6.15Z" fill="#DF6137"></path>
//                 </svg>
//                 </button>
//                 `;

//             // Event listener to remove category when close button is clicked
//             span.querySelector('button').addEventListener('click', function () {
//                 alert(category.api_model)
//                 toggleCategory(category.api_model, false); // Uncheck in dropdown
//                 // selectedContainer.removeChild(span); // Remove from selected list
                
//                 // update list Remove the slug_id from categories_ids list
//                 const index = categories_ids.indexOf(category.api_model);
//                 if (index !== -1) {
//                     categories_ids.splice(index, 1); // Remove slug_id from categories_ids array
//                 }

//                 // Check if the span is still in the selectedContainer before removing
//                 if (selectedContainer.contains(span)) {
//                     selectedContainer.remove(span); // Remove the span from selectedContainer
//                 }
//                 selected_api_model();

//             });

//             selectedContainer.appendChild(span);
//         }


//         function toggleCategory(categoryId, selected) {
//             const checkbox = dropdown.querySelector(`input[data-id="${categoryId}"]`);
//             if (checkbox) {
//                 checkbox.checked = selected;
//             }
            
//             if (selected) {
//                 const category = categories.find(c => c.api_model == categoryId);

//                 if (category && !selectedContainer.querySelector(`[data-id="${categoryId}"]`)) {
//                     createSelectedCategory(category);
//                     console.log(categoryId);
//                     categories_ids.push(categoryId);
//                 }
//             } else {
//                 const selectedCategory = selectedContainer.querySelector(`button[data-id="${categoryId}"]`);
//                 if (selectedCategory) {
//                     selectedCategory.closest('span').remove();
//                 }
//             }
//             selected_api_model()
//         }

//         // set data for api
//         function selected_api_model() {
//             console.log('Selected Prompt Types:', categories_ids);
            
//             const api_model_input = document.querySelector("input[name='api_model']");
//             api_model_input.value = categories_ids;
//         }

//         categories.forEach(category => {
            
//             const categoryElement = createCategoryElement(category);
//             dropdown.appendChild(categoryElement);

//             const checkbox = categoryElement.querySelector('input[type="checkbox"]');
//             checkbox.addEventListener('change', (e) => {
//                 toggleCategory(category.api_model, e.target.checked);
//             });
//         });

//         input.addEventListener('focus', () => {
//             dropdown.classList.remove('hidden');
//         });

//         input.addEventListener('input', () => {
//             const searchTerm = input.value.toLowerCase();
//             Array.from(dropdown.children).forEach(child => {
//                 const name = child.textContent.toLowerCase();
//                 child.style.display = name.includes(searchTerm) ? '' : 'none';
//             });
//         });

//         selectedContainer.addEventListener('click', (e) => {
//             if (e.target.tagName === 'BUTTON') {
//                 const categoryId = e.target.getAttribute('data-id');
//                 toggleCategory(categoryId, false);
//             }
//         });

//         document.addEventListener('click', (e) => {
//             if (!e.target.closest('.api_model_search')) {
//                 dropdown.classList.add('hidden');
//             }
//         });

//         // // set data in update time
//         // setTimeout(() => {

//         //     if(set_api_model_slug_id){
//         //         console.log(set_api_model_slug_id,'r0')
//         //         const slug_ids = set_api_model_slug_id.split(', ');

//         //         console.log(slug_ids,'0.')
//         //         slug_ids.forEach(slug_id => {
//         //             // Find the category by slug_id and select it
//         //             const category = categories.find(c => c.api_model == slug_id);
//         //             if (category) {
//         //                 toggleCategory(category.api_model, true);  // Mark as selected

//         //             }
//         //         });
//         //     }
//         // }, 100);


//     }) 
//     .catch((error) => {
//         console.error('Error:', error);
//     });

// });





document.addEventListener('DOMContentLoaded', function () {
    
    ai_configuration_data.then((response) => {
        const categories = response.data || []; // Ensure data is loaded

        const input = document.getElementById('api_models_input');
        const dropdown = document.getElementById('api_model_dropdown');
        const selectedContainer = document.getElementById('selected_api_models');
        let selectedCategoryId = null; // Store only one selected category

        function createCategoryElement(category) {
            const div = document.createElement('div');
            div.className = 'p-2 hover:bg-gray-100 cursor-pointer';
            div.innerHTML = `
            <label class="flex items-center justify-between">
                <span class="flex items-center">
                    <input type="radio" name="api_model_radio" class="mr-2" data-id="${category.api_model}">
                    ${category.api_model}
                </span>
                <span class="hidden bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded-full">${category.count}</span>
            </label>
            `;
            return div;
        }

        function createSelectedCategory(category) {
            selectedContainer.innerHTML = ''; // Clear any previously selected category
            
            const span = document.createElement('span');
            span.className = 'relative rounded-lg border border-solid border-gray-200 mr-2 pl-2 pr-4 py-1 flex items-center mb-2';
            span.dataset.api_model = category.api_model;
            span.innerHTML = `
                ${category.api_model}
                <button class="ml-1.5 text-blue-800 hover:text-blue-900 absolute top-0 right-0 transform -translate-y-1/2 translate-x-1/2 p-1 hover:opacity-90" data-id="${category.api_model}">
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M5 0C2.245 0 0 2.245 0 5C0 7.755 2.245 10 5 10C7.755 10 10 7.755 10 5C10 2.245 7.755 0 5 0ZM6.68 6.15C6.825 6.295 6.825 6.535 6.68 6.68C6.605 6.755 6.51 6.79 6.415 6.79C6.32 6.79 6.225 6.755 6.15 6.68L5 5.53L3.85 6.68C3.775 6.755 3.68 6.79 3.585 6.79C3.49 6.79 3.395 6.755 3.32 6.68C3.175 6.535 3.175 6.295 3.32 6.15L4.47 5L3.32 3.85C3.175 3.705 3.175 3.465 3.32 3.32C3.465 3.175 3.705 3.175 3.85 3.32L5 4.47L6.15 3.32C6.295 3.175 6.535 3.175 6.68 3.32C6.825 3.465 6.825 3.705 6.68 3.85L5.53 5L6.68 6.15Z" fill="#DF6137"></path>
                    </svg>
                </button>
            `;

            span.querySelector('button').addEventListener('click', function () {
                toggleCategory(null); // Unselect radio button
            });

            selectedContainer.appendChild(span);
        }

        function toggleCategory(categoryId) {
            const radios = dropdown.querySelectorAll('input[type="radio"]');
            radios.forEach(radio => radio.checked = false);

            selectedCategoryId = categoryId; // Update selected category
            const api_model_input = document.querySelector("input[name='api_model']");
            api_model_input.value = categoryId || '';

            selectedContainer.innerHTML = ''; // Clear previous selections
            if (categoryId) {
                const category = categories.find(c => c.api_model == categoryId);
                if (category) {
                    createSelectedCategory(category);
                }
            }
        }

        categories.forEach(category => {
            const categoryElement = createCategoryElement(category);
            dropdown.appendChild(categoryElement);

            const radio = categoryElement.querySelector('input[type="radio"]');
            radio.addEventListener('change', (e) => {
                toggleCategory(category.api_model);
            });
        });

        input.addEventListener('focus', () => {
            dropdown.classList.remove('hidden');
        });


        //  set data in update time
        setTimeout(() => {

            if(set_ai_rate_model){
                console.log(set_ai_rate_model,'r0')
                const slug_ids = set_ai_rate_model.split(', ');

                console.log(slug_ids,'0.')
                slug_ids.forEach(slug_id => {
                    // Find the category by slug_id and select it
                    const category = categories.find(c => c.api_model == slug_id);
                    if (category) {
                        toggleCategory(category.api_model, true);  // Mark as selected

                    }
                });
            }
        }, 100);

        input.addEventListener('input', () => {
            const searchTerm = input.value.toLowerCase();
            Array.from(dropdown.children).forEach(child => {
                const name = child.textContent.toLowerCase();
                child.style.display = name.includes(searchTerm) ? '' : 'none';
            });
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.api_model_search')) {
                dropdown.classList.add('hidden');
            }
        });

    }).catch((error) => {
        console.error('Error:', error);
    });

});


