


// Listen for Enter key on the form
document.addEventListener("DOMContentLoaded", () => {
    const integrationForm = document.getElementById("integration_form");

    integrationForm.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // prevent actual form submission
            add_integration_api(); // trigger your existing function
        }
    });
});


function add_integration_api() {

    // Get the form element
    const integration_form = document.querySelector('[name="integration_form"]');

    // Collect form data using the name attributes
    const integration_type = integration_form.querySelector('[name="integration_type"]').value;
    const description = integration_form.querySelector('[name="description"]').value;

    const data = new FormData();
    data.append("integration_type", integration_type);
    data.append("description", description);

    // Collect additional dynamic field data
    const fields = integration_form.querySelectorAll('[name^="integration_"]');
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
            await update_api(update_integration_url, data, slug_id, list_integration_page_url);
        } else {
            await add_api(add_integration_url, data, list_integration_page_url);
        }
    })()

}



(async () => {
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 

        const temp_api_url = `${list_integration_url}?slug_id=${slug_id}`;
        const data_obj = await set_data_api(temp_api_url, slug_id);

        const integration_form = document.querySelector('[name="integration_form"]');
        const integration_type_select = integration_form.querySelector('[name="integration_type"]');
        const description = integration_form.querySelector('[name="description"]');

        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            const configData = data_obj.data[0];

            description.value = configData.description;

            // Step 1: Get integration field definitions and setup listeners
            await getIntegrationFieldsFromBackend();

            // Wait for the field definitions to be loaded
            const populateFields = () => {
                // Step 2: Set integration type dropdown value
                const integrationTypeName = configData.integration_type_id_data.name;
                integration_type_select.value = integrationTypeName;

                // Step 3: Trigger change event to render config fields
                const changeEvent = new Event('change');
                integration_type_select.dispatchEvent(changeEvent);

                // Step 4: Create a promise to wait for fields to be rendered
                return new Promise(resolve => {
                    // Give the DOM time to update after the change event
                    setTimeout(() => {
                        // Fix: Use integration_json_data instead of config
                        if (configData.integration_json_data) {
                            Object.entries(configData.integration_json_data).forEach(([key, value]) => {
                                const field = integration_form.querySelector(`[name="integration_${key}"]`);
                                if (field) {
                                    field.value = value;
                                } else {
                                    console.warn(`Field for ${key} not found in the form`);
                                }
                            });
                        }
                        resolve();
                    }, 300);
                });
            };
            
            await populateFields();
        } else {
            window.location.href = error_page;
        }
    }
})();

