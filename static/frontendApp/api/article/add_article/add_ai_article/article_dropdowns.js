



// set_domain_dropdown
function set_domain_dropdown(domain_data){
    console.log(domain_data,'***')
    domain_data.then((response) => {
        const domain_data = response.domains || [];  // Ensure data is loaded
        console.log(domain_data)
        const selectElement = document.querySelector('[name="ai_domain_data"]');
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
            const selectedSlugId = selectElement.value;
            console.log('Selected Slug ID:', selectedSlugId);

            const domain_input = document.querySelector("input[name='ai_domain_slug_id']");
            domain_input.value = selectedSlugId;

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









// set_prompt_dropdown
function set_prompt_dropdown(prompt_data){
    console.log(prompt_data,'2030')
    prompt_data.then((response) => {
        const prompt_data = response.prompts || [];  // Ensure data is loaded
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

        // set slug_id in add time
        selectElement.addEventListener('change', function () {
            const selectedSlugId = selectElement.value;
            console.log('Selected Slug ID:', selectedSlugId);

            const prompt_input = document.querySelector("input[name='prompt_slug_id']");
            prompt_input.value = selectedSlugId;

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

