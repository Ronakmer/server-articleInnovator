

function add_supportive_prompt_type_api() {

    // Get the form element
    const supportive_prompt_type_form = document.querySelector('[name="supportive_prompt_type_form"]');

    // Collect form data using the name attributes
    const name = supportive_prompt_type_form.querySelector('[name="name"]').value;
    const description = supportive_prompt_type_form.querySelector('[name="description"]').value;
    const example = supportive_prompt_type_form.querySelector('[name="example"]').value;
    // const supportive_variables = supportive_prompt_type_form.querySelector('[name="supportive_variables"]').value;
    const title = supportive_prompt_type_form.querySelector('[name="title"]').value;

    const supportive_variables_data = create_variables_json()

    const data = new FormData();
    data.append("name", name);
    data.append("description", description);
    data.append("example", example);
    // data.append("supportive_variables", supportive_variables);
    data.append("supportive_variables_data", supportive_variables_data);
    data.append("title", title);



    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 

        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_supportive_prompt_type_url, data, slug_id, list_supportive_prompt_type_page_url);
        } else {
            await add_api(add_supportive_prompt_type_url, data, list_supportive_prompt_type_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_supportive_prompt_type_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);
        
        const temp_variables_api_url = `${list_variables_url}?supportive_prompt_type_slug_id=${slug_id}`;
        var variables_data_obj = await set_data_api(temp_variables_api_url, '');
        console.log(variables_data_obj,'variables_data_obj')

        // Get the form element
        const supportive_prompt_type_form = document.querySelector('[name="supportive_prompt_type_form"]');

        // Collect form data using the name attributes
        const name = supportive_prompt_type_form.querySelector('[name="name"]');
        const description = supportive_prompt_type_form.querySelector('[name="description"]');
        const example = supportive_prompt_type_form.querySelector('[name="example"]');
        // const supportive_variables = supportive_prompt_type_form.querySelector('[name="supportive_variables"]');
        const title = supportive_prompt_type_form.querySelector('[name="title"]');

        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            name.value = data_obj.data[0].name;
            description.value = data_obj.data[0].description;
            example.value = data_obj.data[0].example;
            title.value = data_obj.data[0].title;
            // supportive_variables.value = data_obj.data[0].supportive_variables;


            await populateSupportiveVariables(variables_data_obj);
            
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     



// function create_variables_json(){

//     // Build variables array
//     const nameValueGroups = document.querySelectorAll('.name-value-group');
//     const variables = [];

//     nameValueGroups.forEach(group => {
//         const nameInput = group.querySelector('input[name="name[]"]');
//         const valueInput = group.querySelector('textarea[name="value[]"]');
//         const requiredCheckbox = group.querySelector('input[name="required[]"]');

//         const nameVal = nameInput.value.trim();
//         const valueVal = valueInput.value.trim();
//         const requiredVal = requiredCheckbox?.checked || false;

//         if (nameVal && valueVal) {
//             variables.push({
//                 name: nameVal,
//                 value: valueVal,
//                 required: requiredVal
//             });
//         }
//     });

//     console.log(variables);
//     return JSON.stringify(variables);

//     // // Append the supportive variables JSON
//     // data.append("variables", JSON.stringify(variables));


// }


// async function populateSupportiveVariables(variables_data_obj) {
//     if (variables_data_obj && variables_data_obj.data.length > 0) {
//         const addButton = document.getElementById('add-name-value-btn');
//         const requiredLength = variables_data_obj.data.length;
//         let currentLength = document.querySelectorAll('.name-value-group').length;

//         // Function to wait for DOM update
//         const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

//         // Click the add button until enough groups are added
//         while (currentLength < requiredLength) {
//             addButton.click();
//             await wait(100);  // Wait a bit for DOM to update
//             currentLength = document.querySelectorAll('.name-value-group').length;
//         }

//         // Now populate the values
//         variables_data_obj.data.forEach((supportiveVar, index) => {
//             const group = document.querySelector(`.name-value-group[data-index="${index}"]`);

//             if (group) {
//                 const nameInput = group.querySelector('input[name="name[]"]');
//                 const valueInput = group.querySelector('textarea[name="value[]"]');
//                 const requiredCheckbox = group.querySelector('input[name="required[]"]');
//                 nameInput.value = supportiveVar.name || '';
//                 valueInput.value = supportiveVar.value || '';
//                 requiredCheckbox.checked = supportiveVar.required || false;
//             }
//         });
      
        
//     }
    
// }





// Function to create a new name-value group
function addNameValueGroup() {
    const container = document.getElementById('name-value-wrapper');
    const groups = container.querySelectorAll('.name-value-group');
    const newIndex = groups.length;
    
    // Clone the first group
    const newGroup = groups[0].cloneNode(true);
    
    // Clear input values
    newGroup.querySelector('input[name="name[]"]').value = '';
    newGroup.querySelector('textarea[name="value[]"]').value = '';
    newGroup.querySelector('input[name="required[]"]').checked = false;
    
    // Add data-index attribute
    newGroup.setAttribute('data-index', newIndex);
    
    // Show remove button for added groups
    const removeBtn = newGroup.querySelector('.remove-name-value-btn');
    if (removeBtn) {
        removeBtn.classList.remove('hidden');
    }
    
    // Add the new group to the container
    container.appendChild(newGroup);
    
    // Add event listener to remove button
    if (removeBtn) {
        removeBtn.addEventListener('click', function() {
            container.removeChild(newGroup);
            // Reindex remaining groups
            updateGroupIndices();
        });
    }
    
    return newGroup;
}

// Function to update data-index attributes after removal
function updateGroupIndices() {
    const container = document.getElementById('name-value-wrapper');
    const groups = container.querySelectorAll('.name-value-group');
    groups.forEach((group, index) => {
        group.setAttribute('data-index', index);
    });
}

// Function to create JSON from form fields
function create_variables_json() {
    const nameValueGroups = document.querySelectorAll('.name-value-group');
    const variables = [];

    nameValueGroups.forEach(group => {
        const nameInput = group.querySelector('input[name="name[]"]');
        const valueInput = group.querySelector('textarea[name="value[]"]');
        const requiredCheckbox = group.querySelector('input[name="required[]"]');
        const slugIdInput = group.querySelector('input[name="variables_slug_id[]"]');  // Get hidden slug_id

        const nameVal = nameInput.value.trim();
        const valueVal = valueInput.value.trim();
        const requiredVal = requiredCheckbox?.checked || false;
        const slugIdVal = slugIdInput ? slugIdInput.value.trim() : '';


        // if (nameVal && valueVal) {
        //     variables.push({
        //         name: nameVal,
        //         value: valueVal,
        //         required: requiredVal
        //     });
        // }
        if (nameVal && valueVal) {
            const entry = {
                name: nameVal,
                value: valueVal,
                required: requiredVal
            };
            if (slugIdVal) {
                entry.slug_id = slugIdVal;
            }
            variables.push(entry);
        }
    });

    console.log(variables);
    return JSON.stringify(variables);
}

// Function to populate supportive variables from API data
async function populateSupportiveVariables(variables_data_obj) {
    if (!variables_data_obj || !variables_data_obj.data || 
        !Array.isArray(variables_data_obj.data) || 
        variables_data_obj.data.length === 0) {
        console.log("No supportive variables data to populate");
        return;
    }
    
    console.log("Populating supportive variables:", variables_data_obj.data);
    
    const container = document.getElementById('name-value-wrapper');
    
    // Make sure we have the first group as template
    let firstGroup = container.querySelector('.name-value-group');
    if (!firstGroup) {
        console.error("Cannot find name-value-group template");
        return;
    }
    
    // Clear existing groups except the first one (template)
    const existingGroups = container.querySelectorAll('.name-value-group');
    for (let i = 1; i < existingGroups.length; i++) {
        container.removeChild(existingGroups[i]);
    }
    
    // Reset the first group
    firstGroup.setAttribute('data-index', '0');
    
    // Populate first group if we have data
    if (variables_data_obj.data.length > 0) {
        const firstVar = variables_data_obj.data[0];
        const nameInput = firstGroup.querySelector('input[name="name[]"]');
        const valueInput = firstGroup.querySelector('textarea[name="value[]"]');
        const requiredCheckbox = firstGroup.querySelector('input[name="required[]"]');
        const slugIdInput = firstGroup.querySelector('input[name="variables_slug_id[]"]'); // ✅ added here

        nameInput.value = firstVar.name || '';
        valueInput.value = firstVar.value || '';
        requiredCheckbox.checked = firstVar.required || false;
        if (slugIdInput) {
            slugIdInput.value = firstVar.slug_id || '';
        }

    }
    
    // Create and populate additional groups for remaining data, but manually instead of using the button
    for (let i = 1; i < variables_data_obj.data.length; i++) {
        const newGroup = addNameValueGroup();
        
        if (newGroup) {
            const supportiveVar = variables_data_obj.data[i];
            const nameInput = newGroup.querySelector('input[name="name[]"]');
            const valueInput = newGroup.querySelector('textarea[name="value[]"]');
            const requiredCheckbox = newGroup.querySelector('input[name="required[]"]');
            
            const slugIdInput = newGroup.querySelector('input[name="variables_slug_id[]"]'); // ✅ added here
            if (slugIdInput) {
                slugIdInput.value = supportiveVar.slug_id || '';
            }


            nameInput.value = supportiveVar.name || '';
            valueInput.value = supportiveVar.value || '';
            requiredCheckbox.checked = supportiveVar.required || false;
        }
    }
    
    console.log("Finished populating supportive variables");
}

// Initialize add button event listener
// document.addEventListener('DOMContentLoaded', function() {
//     const addButton = document.getElementById('add-name-value-btn');
//     if (addButton) {
//         addButton.addEventListener('click', addNameValueGroup);
//     }
// });