

let article_type_data = '';
let workspace_data = '';
let set_article_type_id = '';
let set_workspace_id = '';

let ai_configuration_data = '';
let set_ai_rate_model = '';


// wp prompt

let wp_prompt_category_type_data = '';
let set_wp_prompt_category_type_id = '';






function add_prompt_api() {

    // Get the form element
    const prompt_form = document.querySelector('[name="prompt_form"]');

    // Collect form data using the name attributes
    const name = prompt_form.querySelector('[name="name"]').value;
    const article_type_slug_id = prompt_form.querySelector('[name="article_type_id"]').value;
    // const workspace_slug_id = prompt_form.querySelector('[name="workspace_id"]').value;
    const prompt_data = prompt_form.querySelector('[name="prompt_data"]').value;
    const ai_rate_model = prompt_form.querySelector('[name="api_model"]').value;

    let workspace_slug_id = '';
    workspace_element = prompt_form.querySelector('[name="workspace_id"]');
    if(workspace_element){
        workspace_slug_id = workspace_element.value;
    }

    const data = new FormData();
    data.append("name", name);
    data.append("article_type_slug_id", article_type_slug_id);
    data.append("workspace_slug_id", workspace_slug_id);
    data.append("prompt_data", prompt_data);
    data.append("ai_rate_model", ai_rate_model);


    const hiddenInputs = prompt_form.querySelectorAll('input[type="hidden"][name$="_id"]');
    alert(hiddenInputs)
    hiddenInputs.forEach(hiddenInput => {
        const fieldName = hiddenInput.name; // e.g., wp_prompt_somefield_id
        const fieldValue = hiddenInput.value;
        if (fieldName !== 'article_type_id' && fieldName !== 'workspace_id') {
            console.log(`Adding hidden input: ${fieldName} = ${fieldValue}`);
            data.append(fieldName, fieldValue);
        }        
    });





    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_prompt_url, data, slug_id, list_prompt_page_url);
        } else {
            await add_api(add_prompt_url, data, list_prompt_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_prompt_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const prompt_form = document.querySelector('[name="prompt_form"]');

        // Collect form data using the name attributes
        const name = prompt_form.querySelector('[name="name"]');
        const prompt_data = prompt_form.querySelector('[name="prompt_data"]');
    

        const workspace_div = prompt_form.querySelector('[id="workspace-div"]');

        workspace_div?.remove();


        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            name.value = data_obj.data[0].name;
            prompt_data.value = JSON.stringify(data_obj.data[0].prompt_data);
            // article_type_slug_id.value = data_obj.data[0].article_type_slug_id;
            // workspace_slug_id.value = data_obj.data[0].workspace_slug_id;

            set_article_type_id = data_obj.data[0].article_type_id_data.slug_id;
            // set_workspace_id = data_obj.data[0].workspace_id_data.slug_id;
            // set_ai_rate_model = data_obj.data[0].ai_configuration_id_data.api_model;
            set_ai_rate_model = data_obj.data[0].ai_rate_model;


            console.log(data_obj.data[0].wordpress_prompt_json_data,'//////////////')
            const obj_data = JSON.stringify(data_obj.data[0].wordpress_prompt_json_data);
            // const parsed_obj_data = JSON.parse(obj_data);


            // // setTimeout(() => {
            // populatePromptDropdowns(obj_data).then(() => {
            //     // Then set the saved values
            //     setPromptDropdownValues(obj_data);
                
            // });
            // // }, 5000);

            setTimeout(() => {
                setPromptDropdownValues(obj_data);
            }, 2000);
            
            
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     

function get_article_type_data(){

    article_type_data = get_data_api(list_article_type_url)
    console.log(article_type_data,'000')
}
get_article_type_data()


function get_workspace_data(){

    workspace_data = get_data_api(list_workspace_url)
    console.log(workspace_data,'000')
}
get_workspace_data()



function get_ai_configuration_data(){

    ai_configuration_data = get_data_api(list_ai_configuration_url)
}
get_ai_configuration_data()






// wp propmt 
function get_supportive_prompt_type_data() {
    get_data_api(list_supportive_prompt_type_url)
        .then((supportive_prompt_type_data) => {
            console.log(supportive_prompt_type_data, 'xxxxxxxxxxxxxxxxxxxxxx');
            populatePromptDropdowns(supportive_prompt_type_data);
        })
        .catch((error) => {
            console.error("Error fetching prompt data:", error);
        });
}

get_supportive_prompt_type_data();




