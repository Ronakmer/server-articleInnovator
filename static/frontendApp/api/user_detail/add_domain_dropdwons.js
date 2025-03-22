


// workspace
document.addEventListener('DOMContentLoaded', function () {
    
    workspace_data.then((response) => {
        // Access article_type_fields once the promise is resolved
        const workspace_data = response.data || [];  // Ensure data is loaded
        console.log(workspace_data, '0w');


        const selectElement = document.querySelector('[name="workspace_data"]');

        // Clear existing options
        selectElement.innerHTML = '';

        // Add a default "Select" option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select';
        defaultOption.selected = true;
        defaultOption.disabled = true;
        selectElement.appendChild(defaultOption);

        // Populate the dropdown with the workspace_data
        workspace_data.forEach((workspace) => {
            const option = document.createElement('option');
            option.value = workspace.slug_id; // Use appropriate key for the value
            option.textContent = workspace.name; // Use appropriate key for the label
            selectElement.appendChild(option);
        });

        // set slug_id in add time
        selectElement.addEventListener('change', function () {
            const selectedSlugId = selectElement.value;
            console.log('Selected Slug ID:', selectedSlugId);

            const workspace_input = document.querySelector("input[name='new_workspace_id']");
            workspace_input.value = selectedSlugId;


        });

    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

});





// domain
document.addEventListener('DOMContentLoaded', function () {
    
    domain_data.then((response) => {
        // Access article_type_fields once the promise is resolved
        const domain_data = response.data || [];  // Ensure data is loaded
        console.log(domain_data, '0w');


        const selectElement = document.querySelector('[name="domain_data"]');

        // Clear existing options
        selectElement.innerHTML = '';

        // Add a default "Select" option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select';
        defaultOption.selected = true;
        defaultOption.disabled = true;
        selectElement.appendChild(defaultOption);

        // Populate the dropdown with the domain_data
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

            const domain_input = document.querySelector("input[name='new_domain_id']");
            domain_input.value = selectedSlugId;

        });

    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

});




