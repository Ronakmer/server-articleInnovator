


// async function populatePromptDropdowns(obj_data) {
//     if (obj_data && obj_data.then) {
//         obj_data = await obj_data.catch((error) => {
//             console.error('Error:', error);
//         });
//     }
//     // await new Promise(resolve => setTimeout(resolve, 2000));        

//     await processDropdownData(obj_data);
// }


// async function processDropdownData(response) {
//     const promptCategories = response.data || [];

//     const containerDiv = document.getElementById('wp_promp_id');
//     if (!containerDiv) {
//         console.error('Container div not found');
//         return;
//     }

//     containerDiv.innerHTML = '';
//     containerDiv.className = 'flex flex-wrap w-full'; // Ensure two-column layout
    

//     for (const item of promptCategories) {
//         const fieldName = `supportive_prompt_${item.name}`;
//         console.log(fieldName, "fieldName");
//         const wrapper = document.createElement('div');
//         // wrapper.className = 'flex flex-col md:flex-row items-start gap-3 mb-4';
//         wrapper.className = 'w-full md:w-1/2 px-2 mb-4'; // Two-column layout

//         wrapper.innerHTML = `
//             <div class="block w-full">
//                 <label for="${fieldName}"
//                     class="mb-2 text-sm font-medium text-gray-600 w-full flex items-center">${item.title}
//                 </label>
//                 <select id="${fieldName}" name="${fieldName}_data" class="!appearance-none bg-white border border-gray-300 text-gray-900 text-sm font-normal rounded-lg block w-full py-2 px-3 pr-10 focus:outline-none focus:ring-2 focus:ring-blue-500">
//                 </select>
//                 <input type="hidden" name="${fieldName}_id" class="flex-grow text-sm outline-none px-2 py-1" placeholder="">
//                 </div>
//             `;

//         containerDiv.appendChild(wrapper);

//         const selectElement = wrapper.querySelector(`select[name="${fieldName}_data"]`);
//         const hiddenInput = wrapper.querySelector(`input[name="${fieldName}_id"]`);

//         const defaultOption = document.createElement('option');
//         defaultOption.value = '';
//         defaultOption.textContent = `Select ${item.title}`;
//         selectElement.appendChild(defaultOption);

//         try {
//             const obj = await get_supportive_prompt_data(item.slug_id);
//             console.log(obj,'objjjjjjjjjjjjjjj')
//             if (obj && obj.data) {
//                 obj.data.forEach(optionItem => {
//                     const option = document.createElement('option');
//                     option.value = optionItem.slug_id;
//                     option.textContent = optionItem.name;
//                     option.dataset.description = optionItem.description;
//                     option.dataset.example = optionItem.example;
//                     option.dataset.variables = optionItem.supportive_variables;
//                     selectElement.appendChild(option);
//                 });
//                 // Set default selection to the first available option
//                 if (selectElement.options.length > 1) {
//                     selectElement.selectedIndex = 1; // Select the first actual option
//                     hiddenInput.value = selectElement.options[1].value; // Update hidden input with selected value
//                 }
//             }
//         } catch (error) {
//             console.error("Error fetching WP prompt data:", error);
//         }


//         selectElement.addEventListener('change', function () {
//             const selectedValue = this.value;
//             hiddenInput.value = selectedValue;


//             const selectedOption = this.options[this.selectedIndex];
//             if (selectedOption && selectedValue) {                       

//                 console.log({
//                     slug_id: selectedValue,

//                     // type: item.name,
//                     // slug_id: selectedValue,  // Printing the slug_id of selected option
//                     // name: selectedOption.textContent,
//                     // description: selectedOption.dataset.description,
//                     // example: selectedOption.dataset.example,
//                     // variables: selectedOption.dataset.variables
        
                    
//                 });

//             }
//         });

//     }
// }

// async function get_supportive_prompt_data(slug_id) {
//     try {
//         const supportive_prompt_data = await get_data_api(list_supportive_prompt_url, '', slug_id);
//         return supportive_prompt_data;
//     } catch (error) {
//         console.error("Error fetching prompt data:", error);
//         return null;
//     }
// }















// // for update time
// async function setPromptDropdownValues(savedData) {
//     // Check if we have saved data to populate
//     if (!savedData) {
//         console.log("No saved data provided");
//         return;
//     }
    
//     // Parse the data if it's a string
//     const promptData = typeof savedData === 'string' ? JSON.parse(savedData) : savedData;
    
//     console.log("Setting values for:", promptData);
    
//     // Ensure all dropdowns are fully rendered by waiting for them to be available
//     const maxAttempts = 10;
//     let attempts = 0;
    
//     while (attempts < maxAttempts) {
//         const allDropdownsReady = Object.keys(promptData)
//             .filter(key => key.startsWith('supportive_prompt_'))
//             .every(key => {
//                 const selectName = key.replace('_id', '_data');
//                 return document.querySelector(`select[name="${selectName}"]`);
//             });
        
//         if (allDropdownsReady) break;
        
//         await new Promise(resolve => setTimeout(resolve, 500));
//         attempts++;
//         console.log(`Waiting for dropdowns, attempt ${attempts}/${maxAttempts}`);
//     }
    
//     // Loop through each field in the saved data
//     Object.entries(promptData).forEach(([key, value]) => {
//         if (!key.startsWith('supportive_prompt_') || !value) return;
        
//         const selectName = key.replace('_id', '_data');
//         const selectElement = document.querySelector(`select[name="${selectName}"]`);
//         const hiddenInput = document.querySelector(`input[name="${key}"]`);
        
//         if (selectElement && hiddenInput) {
//             // Set the dropdown value
//             selectElement.value = value;
            
//             // Set the hidden input value
//             hiddenInput.value = value;
            
//             // Trigger change event
//             const changeEvent = new Event('change', { bubbles: true });
//             selectElement.dispatchEvent(changeEvent);
            
//             console.log(`Successfully set value for ${key} to ${value}`);
//         } else {
//             console.log(`Failed to set value for ${key}: elements not found`);
//         }
//     });
// }










// Function to populate dropdowns from API data
async function populatePromptDropdowns(obj_data) {
    if (!obj_data || !obj_data.data || !Array.isArray(obj_data.data)) {
        console.error("Invalid prompt category data format:", obj_data);
        return;
    }
    
    const promptCategories = obj_data.data;
    console.log(`Processing ${promptCategories.length} prompt categories`);
    
    // Debug: List all categories
    promptCategories.forEach(cat => console.log(`Category: ${cat.name} - ${cat.title}`));
    
    const containerDiv = document.getElementById('supportive_prompt_id');
    if (!containerDiv) {
        console.error('Container div not found');
        return;
    }
    
    // Clear the container first
    containerDiv.innerHTML = '';
    containerDiv.className = 'flex flex-wrap w-full';
    
    // Create all dropdowns first (synchronously)
    for (const item of promptCategories) {
        const fieldName = `supportive_prompt_${item.name}`;
        console.log(`Creating dropdown for: ${fieldName}`);
        
        const wrapper = document.createElement('div');
        wrapper.className = 'w-full md:w-1/2 px-2 mb-4';
        wrapper.setAttribute('data-field-name', fieldName);
        
        wrapper.innerHTML = `
            <div class="block w-full">
                <label for="${fieldName}"
                    class="mb-2 text-sm font-medium text-gray-600 w-full flex items-center">${item.title}
                </label>
                <select id="${fieldName}" name="${fieldName}_data" class="!appearance-none bg-white border border-gray-300 text-gray-900 text-sm font-normal rounded-lg block w-full py-2 px-3 pr-10 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">Select ${item.title}</option>
                </select>
                <input type="hidden" name="${fieldName}_id" value="">
            </div>
        `;
        
        containerDiv.appendChild(wrapper);
        
        // Verify that the dropdown was added to the DOM
        const added = document.querySelector(`[data-field-name="${fieldName}"]`);
        if (!added) {
            console.error(`Failed to add ${fieldName} to the DOM`);
        } else {
            console.log(`Successfully added ${fieldName} to the DOM`);
        }
    }
    
    // Now populate each dropdown with options (asynchronously)
    const populationPromises = promptCategories.map(async (item) => {
        const fieldName = `supportive_prompt_${item.name}`;
        const selectElement = document.querySelector(`select[name="${fieldName}_data"]`);
        const hiddenInput = document.querySelector(`input[name="${fieldName}_id"]`);
        
        if (!selectElement || !hiddenInput) {
            console.error(`Elements for ${fieldName} not found in DOM`);
            return;
        }
        
        // Add event listener
        selectElement.addEventListener('change', function() {
            const selectedValue = this.value;
            hiddenInput.value = selectedValue;
            
            if (selectedValue) {
                console.log({ slug_id: selectedValue });
            }
        });
        
        try {
            const obj = await get_supportive_prompt_data(item.slug_id);
            console.log(`Fetched ${obj?.data?.length || 0} options for ${fieldName}`);
            
            if (obj && obj.data && Array.isArray(obj.data)) {
                obj.data.forEach(optionItem => {
                    const option = document.createElement('option');
                    option.value = optionItem.slug_id;
                    option.textContent = optionItem.name;
                    option.dataset.description = optionItem.description || '';
                    option.dataset.example = optionItem.example || '';
                    option.dataset.variables = optionItem.supportive_variables || '';
                    selectElement.appendChild(option);
                });
                // Set default selection to the first available option
                // if (selectElement.options.length > 1) {
                //     selectElement.selectedIndex = 1; // Select the first actual option
                //     hiddenInput.value = selectElement.options[1].value; // Update hidden input with selected value
                // }
            }
        } catch (error) {
            console.error(`Error fetching options for ${fieldName}:`, error);
        }
    });
    
    // Wait for all dropdowns to be populated
    await Promise.all(populationPromises);
    console.log(`Created and populated ${promptCategories.length} dropdown elements`);
    
    // Return true to indicate successful completion
    return true;
}

// Function to get WP prompt data for a specific category
async function get_supportive_prompt_data(slug_id) {
    try {
        const supportive_prompt_data = await get_data_api(list_supportive_prompt_url, '', slug_id);
        return supportive_prompt_data;
    } catch (error) {
        console.error("Error fetching prompt data:", error);
        return null;
    }
}


// Function to set values for all dropdowns update time
async function setPromptDropdownValues(savedData) {
    if (!savedData) {
        console.log("No saved data provided");
        return;
    }
    
    // Parse the data if it's a string
    let promptData;
    try {
        promptData = typeof savedData === 'string' ? JSON.parse(savedData) : savedData;
    } catch (error) {
        console.error("Error parsing saved data:", error, savedData);
        return;
    }
    
    console.log("Setting values for:", promptData);
    
    // Find fields that need to be set
    const fieldsToSet = Object.keys(promptData).filter(key => key.startsWith('supportive_prompt_'));
    console.log(`Need to set values for ${fieldsToSet.length} fields:`, fieldsToSet);
    
    // Debug: check if all needed elements exist in the DOM
    fieldsToSet.forEach(key => {
        const selectName = key.replace('_id', '_data');
        const selectExists = !!document.querySelector(`select[name="${selectName}"]`);
        const inputExists = !!document.querySelector(`input[name="${key}"]`);
        
        console.log(`Field ${key}: Select exists: ${selectExists}, Input exists: ${inputExists}`);
        
        // If elements don't exist, try to recreate them
        if (!selectExists || !inputExists) {
            // Extract the field base name (e.g., supportive_prompt_wp_meta_descriptions_id -> wp_meta_descriptions)
            const baseName = key.replace('supportive_prompt_', '').replace('_id', '');
            
            // Look for the parent div that should contain this field
            const parentDiv = document.querySelector(`[data-field-name="supportive_prompt_${baseName}"]`);
            
            if (!parentDiv) {
                console.error(`Missing parent div for ${baseName}, will create it`);
                
                // If parent div doesn't exist, create the entire structure
                const containerDiv = document.getElementById('supportive_prompt_id');
                if (containerDiv) {
                    const wrapper = document.createElement('div');
                    wrapper.className = 'w-full md:w-1/2 px-2 mb-4';
                    wrapper.setAttribute('data-field-name', `supportive_prompt_${baseName}`);
                    
                    wrapper.innerHTML = `
                        <div class="block w-full">
                            <label for="supportive_prompt_${baseName}"
                                class="mb-2 text-sm font-medium text-gray-600 w-full flex items-center">${baseName.replace('wp_', '').replace('_', ' ').toUpperCase()}
                            </label>
                            <select id="supportive_prompt_${baseName}" name="supportive_prompt_${baseName}_data" class="!appearance-none bg-white border border-gray-300 text-gray-900 text-sm font-normal rounded-lg block w-full py-2 px-3 pr-10 focus:outline-none focus:ring-2 focus:ring-blue-500">
                                <option value="">Select ${baseName}</option>
                                <option value="${promptData[key]}">${promptData[key]}</option>
                            </select>
                            <input type="hidden" name="${key}" value="${promptData[key]}">
                        </div>
                    `;
                    
                    containerDiv.appendChild(wrapper);
                    console.log(`Created missing dropdown for ${baseName}`);
                }
            }
        }
    });
    
    // Now try to set values for all fields
    fieldsToSet.forEach(key => {
        if (!promptData[key]) return;
        
        const selectName = key.replace('_id', '_data');
        const selectElement = document.querySelector(`select[name="${selectName}"]`);
        const hiddenInput = document.querySelector(`input[name="${key}"]`);
        
        if (selectElement && hiddenInput) {
            // Check if the option exists
            let optionExists = false;
            for (let i = 0; i < selectElement.options.length; i++) {
                if (selectElement.options[i].value === promptData[key]) {
                    optionExists = true;
                    break;
                }
            }
            
            // If option doesn't exist, add it
            if (!optionExists && promptData[key]) {
                const option = document.createElement('option');
                option.value = promptData[key];
                option.textContent = promptData[key];
                selectElement.appendChild(option);
            }
            
            // Set the dropdown value
            selectElement.value = promptData[key];
            
            // Set the hidden input value
            hiddenInput.value = promptData[key];
            
            // Trigger change event
            const changeEvent = new Event('change', { bubbles: true });
            selectElement.dispatchEvent(changeEvent);
            
            console.log(`Successfully set value for ${key} to ${promptData[key]}`);
        } else {
            console.error(`Failed to set value for ${key}: elements not found. Select: ${!!selectElement}, Input: ${!!hiddenInput}`);
        }
    });
}
