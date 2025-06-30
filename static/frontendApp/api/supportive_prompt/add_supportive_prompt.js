
let supportive_prompt_type_data = '';
let set_supportive_prompt_type_slug_id = '';

let workspace_data = '';
let set_workspace_id = '';

let ai_configuration_data = '';
let set_ai_model = '';


function add_supportive_prompt_api() {

    // Get the form element
    const supportive_prompt_form = document.querySelector('[name="supportive_prompt_form"]');

    // Collect form data using the name attributes
    const name = supportive_prompt_form.querySelector('[name="name"]').value;
    const description = supportive_prompt_form.querySelector('[name="description"]').value;
    const supportive_prompt_type_id = supportive_prompt_form.querySelector('[name="supportive_prompt_type"]').value;
    const supportive_prompt_data = supportive_prompt_form.querySelector('[name="supportive_prompt_data"]').value;

    const ai_model = supportive_prompt_form.querySelector('[name="api_model"]').value;

    let workspace_slug_id = '';
    workspace_element = supportive_prompt_form.querySelector('[name="workspace_id"]');
    if(workspace_element){
        workspace_slug_id = workspace_element.value;
    }

    const data = new FormData();
    data.append("name", name);
    data.append("description", description);
    data.append("supportive_prompt_type_slug_id", supportive_prompt_type_id);
    data.append("supportive_prompt_data", supportive_prompt_data);
    data.append("ai_model", ai_model);
    data.append("workspace_slug_id", workspace_slug_id);




    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_supportive_prompt_url, data, slug_id, list_supportive_prompt_page_url);
        } else {
            await add_api(add_supportive_prompt_url, data, list_supportive_prompt_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_supportive_prompt_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const supportive_prompt_form = document.querySelector('[name="supportive_prompt_form"]');

        // Collect form data using the name attributes
        const name = supportive_prompt_form.querySelector('[name="name"]');
        const description = supportive_prompt_form.querySelector('[name="description"]');
        const supportive_prompt_data = supportive_prompt_form.querySelector('[name="supportive_prompt_data"]');


        const workspace_div = supportive_prompt_form.querySelector('[id="workspace-div"]');

        workspace_div?.remove();


        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            name.value = data_obj.data[0].name;
            description.value = data_obj.data[0].description;
            supportive_prompt_data.value = data_obj.data[0].supportive_prompt_data;
            set_supportive_prompt_type_slug_id = data_obj.data[0].supportive_prompt_type_id_data.slug_id;   
            
            set_ai_model = data_obj.data[0].ai_model;


            updateTimeout = setTimeout(() => {
                updatePreview();  // Your actual update logic
            }, 5000); // Delay in milliseconds (adjust as needed)
        
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     




function get_supportive_prompt_type_data(){
    
    supportive_prompt_type_data = get_data_api(list_supportive_prompt_type_url)
}
get_supportive_prompt_type_data()



function get_workspace_data(){

    workspace_data = get_data_api(list_workspace_url)
    console.log(workspace_data,'000')
}
get_workspace_data()



function get_ai_configuration_data(){

    ai_configuration_data = get_data_api(list_ai_configuration_url)
}
get_ai_configuration_data()






// // Function to update preview text dynamically
// function updatePreview() {
//     console.log(supportive_variables_data,'4444444444444')   
//     const wpPrompt = document.getElementById('supportive_prompt_data_id').value; // Get the textarea value
//     const preview = document.getElementById('preview'); // The element to display the text
//     preview.textContent = wpPrompt; // Update the preview text  

// }

function updatePreview() {
    const wpPrompt = document.getElementById('supportive_prompt_data_id').value;
    const preview = document.getElementById('preview');
    // Clone the original prompt text
    let finalText = wpPrompt;

    // Replace each variable like {{test-1.2.1}} with its value
    supportive_variables_data.forEach(variable => {
        const name = variable.name;
        const value = variable.example_value;

        // Create regex for placeholder (e.g., {{test-1.2.1}})
        // const regex = new RegExp(`{{\\s*${escapeRegExp(name)}\\s*}}`, 'g');
        const regex = new RegExp(`\\[\\[\\s*${escapeRegExp(name)}\\s*\\]\\]`, 'g');

        finalText = finalText.replace(regex, value);
    });

    // Set the result to the preview element
    preview.textContent = finalText;
}

// Utility to escape special characters in variable names for RegExp
function escapeRegExp(string) {
    // return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

}


// document.getElementById('supportive_prompt_data_id').addEventListener('input', updatePreview);
