// // Function to handle tab selection and field visibility
// function handleTabSelection(tab) {
//     if (!tab) return; // Prevent errors if the tab is null

//     // Reset all tabs' styles
//     const tabs = document.querySelectorAll('.tab');
//     tabs.forEach((t) => {
//         t.style.backgroundColor = ''; // Reset to default background color
//         const spanElement = t.querySelector('span');
//         if (spanElement) {
//             spanElement.style.color = ''; // Reset text color
//         }
//     });

//     // Get selected tab attributes
//     const color = tab.getAttribute('data-color');
//     const tabName = tab.querySelector('span')?.textContent.trim(); // Safe access with optional chaining

//     if (!tabName) return; // Avoid errors if tabName is undefined

//     // Apply styles to the selected tab
//     tab.style.backgroundColor = color;
//     const spanElement = tab.querySelector('span');
//     if (spanElement) {
//         spanElement.style.color = '#fff';
//     }

//     // List of field IDs to hide/show
//     const fieldIds = [
//         'key_id', 'model_id', 'version_id', 'url_id',
//         'email_id', 'type_id', 'button_id'
//     ];

//     // Hide all fields
//     fieldIds.forEach(id => {
//         const field = document.getElementById(id);
//         if (field) {
//             field.style.display = "none";
//         }
//     });

//     // Show fields based on the selected tab
//     const showFields = {
//         'OpenAI': ['key_id', 'model_id', 'button_id', 'email_id'],
//         'Azure': ['version_id', 'url_id', 'type_id', 'email_id', 'model_id', 'key_id', 'button_id'],
//         'Claude': ['key_id', 'email_id', 'model_id', 'button_id']
//     };

//     if (showFields[tabName]) {
//         showFields[tabName].forEach(id => {
//             const field = document.getElementById(id);
//             if (field) {
//                 field.style.display = "block";
//             }
//         });
//     }

//     // set hidden input field if it exists
//     const apiProviderInput = document.getElementById('api_provider');

//     if (apiProviderInput) {
//         apiProviderInput.value = tabName;
//     }


// }

// // Function to initialize the tabs on page load
// function initializeTabs() {
//     const tabs = document.querySelectorAll('.tab');

//     tabs.forEach((tab) => {
//         tab.addEventListener('click', () => handleTabSelection(tab));
//     });

    

//     setTimeout(() => {
//         const apiProviderInput = document.getElementById('api_provider');
//         let preselectedProvider = apiProviderInput ? apiProviderInput.value : '';

//         // Find the preselected tab
//         let preselectedTab = Array.from(tabs).find((tab) => {
//             return tab.querySelector('span')?.textContent.trim() === preselectedProvider;
//         });

//         // If no preselected provider, default to "Azure"
//         if (!preselectedTab) {
//             preselectedTab = Array.from(tabs).find(tab => 
//                 tab.querySelector('span')?.textContent.trim() === 'Azure'
//             );
//         }

//         // Apply selection to the default or preselected tab
//         if (preselectedTab) {
//             handleTabSelection(preselectedTab);
//         }
//     }, 200);
// }

// // Ensure the script runs after DOM is fully loaded
// document.addEventListener('DOMContentLoaded', initializeTabs);





// Function to handle tab selection and field visibility
function handleTabSelection(tab) {
    if (!tab) return; // Prevent errors if the tab is null

    // Reset all tabs' styles
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach((t) => {
        t.style.backgroundColor = ''; // Reset to default background color
        const spanElement = t.querySelector('span');
        if (spanElement) {
            spanElement.style.color = ''; // Reset text color
        }
    });

    // Get selected tab attributes
    const color = tab.getAttribute('data-color');
    const tabName = tab.querySelector('span')?.textContent.trim(); // Safe access with optional chaining

    if (!tabName) return; // Avoid errors if tabName is undefined

    // Apply styles to the selected tab
    tab.style.backgroundColor = color;
    const spanElement = tab.querySelector('span');
    if (spanElement) {
        spanElement.style.color = '#fff';
    }

    // List of field IDs to hide/show
    const fieldIds = [
        'key_id', 'model_id', 'version_id', 'url_id',
        'email_id', 'type_id', 'button_id'
    ];

    // Hide all fields
    fieldIds.forEach(id => {
        const field = document.getElementById(id);
        if (field) {
            field.style.display = "none";
        }
    });

    // Show fields based on the selected tab
    const showFields = {
        'OpenAI': ['key_id', 'model_id', 'button_id', 'email_id'],
        'Azure': ['version_id', 'url_id', 'type_id', 'email_id', 'model_id', 'key_id', 'button_id'],
        'Claude': ['key_id', 'email_id', 'model_id', 'button_id'],
        'Novita': ['url_id', 'type_id', 'email_id', 'model_id', 'key_id', 'button_id'],
    };

    if (showFields[tabName]) {
        showFields[tabName].forEach(id => {
            const field = document.getElementById(id);
            if (field) {
                field.style.display = "block";
            }
        });
    }

    // Set hidden input field if it exists
    const apiProviderInput = document.getElementById('api_provider');
    // alert(apiProviderInput.value)
    if (apiProviderInput) {
        apiProviderInput.value = tabName;
    }
}

// Function to initialize the tabs on page load
function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');
    const apiProviderInput = document.getElementById('api_provider');

    tabs.forEach((tab) => {
        tab.addEventListener('click', () => handleTabSelection(tab));
    });

    setTimeout(() => {
        let preselectedProvider = apiProviderInput ? apiProviderInput.value.trim() : '';

        console.log("Preselected Provider:", preselectedProvider); // Debugging

        // Find the preselected tab
        let preselectedTab = Array.from(tabs).find(tab =>
            tab.querySelector('span')?.textContent.trim() === preselectedProvider
        );

        // If no preselected provider, default to "Azure"
        if (!preselectedTab) {
            console.log("No preselected provider found, defaulting to Azure.");
            preselectedTab = Array.from(tabs).find(tab =>
                tab.querySelector('span')?.textContent.trim() === 'Azure'
            );
        }

        // Apply selection to the default or preselected tab
        if (preselectedTab) {
            console.log("Selecting Tab:", preselectedTab.querySelector('span')?.textContent.trim());
            handleTabSelection(preselectedTab);
        } else {
            console.log("No tab found to select.");
        }
    }, 200);
}

// Ensure the script runs after DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializeTabs);



















// // for model

// document.addEventListener('DOMContentLoaded', function() {
//     const modelsWrapper = document.getElementById('models-wrapper');
//     const newModalBtn = document.getElementById('new_modal_btn');
//     const apiModelInput = document.getElementById('api_model');

//     // Function to update hidden input with comma-separated model names
//     function updateApiModelInput() {
//         const modelInputs = document.querySelectorAll('input[name="model_name[]"]');
//         const modelNames = Array.from(modelInputs)
//             .map(input => input.value.trim())
//             .filter(value => value !== '');
//         apiModelInput.value = modelNames.join(',');
//     }

//     // Add new model input
//     newModalBtn.addEventListener('click', function() {
//         const newModelGroup = document.createElement('div');
//         newModelGroup.className = 'model-input-group mb-2 flex items-center';
        
//         newModelGroup.innerHTML = `
//             <input type="text" name="model_name[]" 
//                 class="block w-full px-3 py-1.5 pr-8 text-sm font-normal shadow-xs text-gray-900 bg-transparent border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none leading-relaxed"
//                 placeholder="API Model">
//             <button class="remove-model flex items-center gap-1.5 px-4 py-2  text-sm font-medium text-white bg-custom-black border border-black-600 rounded-lg hover:bg-indigo-700 ">✕</button>
//         `;

//         modelsWrapper.appendChild(newModelGroup);

//         // Add remove functionality to the new input group
//         const removeBtn = newModelGroup.querySelector('.remove-model');
//         removeBtn.addEventListener('click', function() {
//             modelsWrapper.removeChild(newModelGroup);
//             updateApiModelInput();
//         });

//         // Update hidden input whenever a new input is added
//         newModelGroup.querySelector('input').addEventListener('input', updateApiModelInput);
//     });

//     // Update hidden input for existing inputs
//     document.querySelectorAll('input[name="model_name[]"]').forEach(input => {
//         input.addEventListener('input', updateApiModelInput);
//     });
// });










document.addEventListener('DOMContentLoaded', function() {
    const modelsWrapper = document.getElementById('models-wrapper');
    const newModalBtn = document.getElementById('new_modal_btn');
    const apiModelInput = document.getElementById('api_model');

    // Function to update hidden input with comma-separated model names
    function updateApiModelInput() {
        const modelInputs = document.querySelectorAll('input[name="model_name[]"]');
        const modelNames = Array.from(modelInputs)
            .map(input => input.value.trim())
            .filter(value => value !== '');
        apiModelInput.value = modelNames.join(',');
    }

    // Function to pre-populate model inputs from api_model
    function prePopulateModelInputs() {
        // Clear existing model input groups (except the first one)
        const existingGroups = document.querySelectorAll('.model-input-group');
        for (let i = 1; i < existingGroups.length; i++) {
            modelsWrapper.removeChild(existingGroups[i]);
        }

        // Get models from api_model input
        const models = apiModelInput.value.split(',').map(model => model.trim()).filter(model => model !== '');

        // Populate the first input field with the first model
        if (models.length > 0) {
            document.querySelector('input[name="model_name[]"]').value = models[0];
        }

        // Add additional input groups for remaining models
        for (let i = 1; i < models.length; i++) {
            const newModelGroup = document.createElement('div');
            newModelGroup.className = 'model-input-group mb-2 flex items-center';
            
            newModelGroup.innerHTML = `
                <input type="text" name="model_name[]" 
                    class="block w-full px-3 py-1.5 pr-8 text-sm font-normal shadow-xs text-gray-900 bg-transparent border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none leading-relaxed"
                    placeholder="API Model"
                    value="${models[i]}">
                <button class="remove-model flex items-center gap-1.5 px-4 py-2  text-sm font-medium text-white bg-custom-black border border-black-600 rounded-lg hover:bg-indigo-700 ">✕</button>
            `;

            modelsWrapper.appendChild(newModelGroup);

            // Add remove functionality to the new input group
            const removeBtn = newModelGroup.querySelector('.remove-model');
            removeBtn.addEventListener('click', function() {
                modelsWrapper.removeChild(newModelGroup);
                updateApiModelInput();
            });

            // Update hidden input whenever an input is modified
            newModelGroup.querySelector('input').addEventListener('input', updateApiModelInput);
        }

        // Update the hidden input
        updateApiModelInput();
    }

    // Add new model input
    newModalBtn.addEventListener('click', function() {
        const newModelGroup = document.createElement('div');
        newModelGroup.className = 'model-input-group mb-2 flex items-center';
        
        newModelGroup.innerHTML = `
            <input type="text" name="model_name[]" 
                class="block w-full px-3 py-1.5 pr-8 text-sm font-normal shadow-xs text-gray-900 bg-transparent border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none leading-relaxed"
                placeholder="API Model">
            <button class="remove-model flex items-center gap-1.5 px-4 py-2  text-sm font-medium text-white bg-custom-black border border-black-600 rounded-lg hover:bg-indigo-700 ">✕</button>
        `;

        modelsWrapper.appendChild(newModelGroup);

        // Add remove functionality to the new input group
        const removeBtn = newModelGroup.querySelector('.remove-model');
        removeBtn.addEventListener('click', function() {
            modelsWrapper.removeChild(newModelGroup);
            updateApiModelInput();
        });

        // Update hidden input whenever a new input is added
        newModelGroup.querySelector('input').addEventListener('input', updateApiModelInput);
    });

    setTimeout(() => {
        // Update hidden input for existing inputs
        document.querySelectorAll('input[name="model_name[]"]').forEach(input => {
            input.addEventListener('input', updateApiModelInput);
        });
    }, 500);

    // Pre-populate model inputs when the page loads
    prePopulateModelInputs();

    // Add event listener to pre-populate when api_model changes
    apiModelInput.addEventListener('change', prePopulateModelInputs);
});





