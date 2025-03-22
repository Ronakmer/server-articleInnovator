

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

            const workspace_input = document.querySelector("input[name='workspace_id']");
            workspace_input.value = selectedSlugId;


        });

        // set slug_id in update time
        if (set_workspace_id) {

            const options = selectElement.querySelectorAll('option');
            options.forEach(option => {
                if (option.value === set_workspace_id) {
                    option.selected = true;
                }
            });

            // Additionally, set the workspace input field's value
            const workspace_input = document.querySelector("input[name='workspace_id']");
            workspace_input.value = set_workspace_id;
        }


    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

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
            const api_url = `${get_article_type_fields}${selectedSlugId}` 
            get_article_type_field_data(api_url)

            
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
                
            }
        }, 100);


    }) 
    .catch((error) => {
        console.error('Error:', error);
    });

});



