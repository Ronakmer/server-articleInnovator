
// get_variables_data api
async function get_variables_data(api_url) {
    try {

        const access_token = localStorage.getItem("access_token");
        

        const response = await fetch(api_url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });
        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('00000xxxx:', data);
            // const fields = data.data_field; // Extract fields from response
            const selectedSlugId = data.slug_id;
            // generateDynamicButton(fields)
            createSupportiveVariableButtons(selectedSlugId);


            // show_toast("success", "Roles fetched successfully");
        } else {
            const error_data = responseData;
            console.error('Failed to fetch roles:', error_data);

            const errorMessage = error_data.error || "Something went wrong";
            show_toast("error", `Error: ${errorMessage}`);
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later.");
    }
}






let supportive_variables_data;

// Function to create buttons from supportive variables
function createSupportiveVariableButtons(selectedSlugId) {

    console.log(selectedSlugId, 'selectedSlugId');
    const temp_supportive_variables_api_url = `${list_variables_url}?article_type_slug_id=${selectedSlugId}`;

    const supportive_variables_api_data = set_data_api(temp_supportive_variables_api_url);
    
    console.log(supportive_variables_api_data, 'supportive_variables_api_data');

    supportive_variables_api_data.then((response) => {
        supportive_variables_data = response.data || [];  // Ensure data is loaded
        console.log(supportive_variables_data, 'supportive_variables_data');
        
        // Process the supportive variables data and create buttons
        const buttonsContainer = document.getElementById('variables_btn');
        buttonsContainer.innerHTML = '';  // Clear any existing buttons
       
        supportive_variables_data.forEach(item => {
            const buttonLabel = item.name || ''; // Display name on button
            const variableValue = item.value || ''; // Copy this value instead
        
            // Create button for supportive variables
            const button = document.createElement('button');
            button.textContent = buttonLabel;
            button.type = 'button';
            button.className = 'bottom-2 mr-3 mt-3 px-2 py-1 mt-1 bg-indigo-500 text-white text-xs rounded-lg';
      

            button.dataset.copyValue = variableValue;  // for preview and clipboard
            button.dataset.insertName = buttonLabel;   // for textarea
            

            button.addEventListener('click', function() {
                const insertName = this.dataset.insertName;
                const valueForPreview = this.dataset.copyValue;
                
                // Use the "name" from the item instead of "supportive_prompt_type_id_data.name"
                const supportiveVariables = `[[${item.name}]]` || ''; // Get the "name" value from the data

                // updatePreview();

                // Store the supportive variable name for insertion
                button.dataset.variable = supportiveVariables;


                // Add click event to copy and insert the variable into the editor or textarea
                button.addEventListener('click', function() {
                    // Copy to clipboard
                    navigator.clipboard.writeText(this.dataset.variable)
                        .then(() => {
                            console.log('Variable copied to clipboard');
                            show_toast("success", `Copied to clipboard`);
                            
                            
                            // Visual feedback that copy worked
                            const originalBackground = this.style.backgroundColor;
                            this.style.backgroundColor = '#000000'; 
                            setTimeout(() => {
                                this.style.backgroundColor = originalBackground;
                            }, 300);
                        })
                        .catch(err => {
                            console.error('Failed to copy: ', err);
                        });
                });


            });
            
            
        
            buttonsContainer.appendChild(button);
        });
        



    }).catch((error) => {
        console.error('Error:', error);
    });
}

// Function to clear all buttons
function clearSupportiveVariableButtons() {
    const buttonsContainer = document.getElementById('supportive_variables_btn');
    buttonsContainer.innerHTML = '';
}
