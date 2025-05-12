


// Listen for Enter key on the form
document.addEventListener("DOMContentLoaded", () => {
    const configuration_settingsForm = document.getElementById("configuration_settings_form");

    configuration_settingsForm.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // prevent actual form submission
            add_configuration_settings_api(); // trigger your existing function
        }
    });
});


function add_configuration_settings_api() {

    // Get the form element
    const configuration_settings_form = document.querySelector('[name="configuration_settings_form"]');

    // Collect form data using the name attributes
    const name = configuration_settings_form.querySelector('[name="name"]').value;
    const description = configuration_settings_form.querySelector('[name="description"]').value;

    const data = new FormData();
    data.append("name", name);
    data.append("description", description);

    // Collect additional dynamic field data
    const fields = configuration_settings_form.querySelectorAll('[name^="config_"]');
    fields.forEach(field => {
        const fieldValue = field.value;
        data.append(field.name, fieldValue);
    });


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_configuration_settings_url, data, slug_id, list_configuration_settings_page_url);
        } else {
            await add_api(add_configuration_settings_url, data, list_configuration_settings_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_configuration_settings_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const configuration_settings_form = document.querySelector('[name="configuration_settings_form"]');

        // Collect form data using the name attributes
        const name = configuration_settings_form.querySelector('[name="name"]');
        const description = configuration_settings_form.querySelector('[name="description"]');

        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            name.value = data_obj.data[0].name;
            description.value = data_obj.data[0].description;

            const configData=data_obj.data[0];
            // Set dynamic config fields
            if (configData.config) {
                // Wait for the config fields to be created
                await get_config_field();
                
                // Trigger the change event to create fields based on selected config type
                const nameSelect = document.getElementById('name');
                if (nameSelect) {
                    nameSelect.value = configData.name;
                    // Create a new change event
                    const event = new Event('change');
                    nameSelect.dispatchEvent(event);
                    
                    // After fields are created, populate them with values from the API
                    setTimeout(() => {
                        Object.entries(configData.config).forEach(([key, value]) => {
                            const field = configuration_settings_form.querySelector(`[name="config_${key}"]`);
                            if (field) {
                                field.value = value;
                            }
                        });
                    }, 300); // Small delay to ensure fields are created
                }
            }
                
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     

