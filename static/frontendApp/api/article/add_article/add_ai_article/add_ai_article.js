
// // show category, tag and author dropdwon
// document.addEventListener("DOMContentLoaded", function () {
//     const toggleVisibility = (checkboxId, divId) => {
//         const checkbox = document.getElementById(checkboxId);
//         const div = document.getElementById(divId);

//         const updateDisplay = () => {
//             if (checkbox.checked) {
//                 div.classList.add("hidden");
//             } else {
//                 div.classList.remove("hidden");
//             }
//         };

//         // Initial setup
//         updateDisplay();

//         // Listen for changes
//         checkbox.addEventListener("change", updateDisplay);
//     };

//     toggleVisibility("is_author_selected_by_ai", "author_div_id");
//     toggleVisibility("is_category_selected_by_ai", "category_div_id");
//     toggleVisibility("is_tag_selected_by_ai", "tag_div_id");
// });






// // toggleVisibility function
// const toggleVisibility = (checkboxId, divId) => {
//     const checkbox = document.getElementById(checkboxId);
//     const div = document.getElementById(divId);

//     if (!checkbox || !div) {
//         console.warn(`Element not found for checkboxId: ${checkboxId} or divId: ${divId}`);
//         return;
//     }

//     const updateDisplay = () => {
//         if (checkbox.checked) {
//             div.classList.add("hidden");
//         } else {
//             div.classList.remove("hidden");
//         }
//     };

//     // Initial setup
//     updateDisplay();

//     // Listen for changes
//     checkbox.addEventListener("change", updateDisplay);
// };


function temp_set_ai_data() {
    // const temp_article_type_slug_id = localStorage.getItem("article_type_slug_id");
    // const temp_article_type_title = localStorage.getItem("article_type_title");

    const urlParams = new URLSearchParams(window.location.search);
    const stored_article_type_slug_id = urlParams.get("article_type_slug_id");

    // // Query the element by ID or name, make sure it's an input element
    // const set_ai_article_type_slug_id = document.querySelector('[name="ai_article_type_slug_id"]'); // using name or you can use id instead of name
    const set_article_type_title = document.querySelector('[name="article_type_title"]'); // using name or you can use id instead of name
    const set_keyword_section = document.getElementById("ai_keyword"); // using name or you can use id instead of name
    const set_url_section = document.getElementById("ai_url"); // using name or you can use id instead of name


    const stored_article_type_title = article_type_list.data.find(obj => obj.slug_id === stored_article_type_slug_id)?.title;
    const stored_article_type_category = article_type_list.data.find(obj => obj.slug_id === stored_article_type_slug_id)?.category;

    
    if(stored_article_type_title){
        // Check if the element exists before accessing its value
        // set_ai_article_type_slug_id.value = stored_article_type_slug_id;  // Set the value of the input field
        set_article_type_title.textContent = stored_article_type_title;  // Set the value of the input field
    } 


    // Hide both sections first
    if (set_keyword_section) set_keyword_section.classList.add("hidden");
    if (set_url_section) set_url_section.classList.add("hidden");

    // Then show only the correct one
    if (stored_article_type_category === 'keyword' && set_keyword_section) {
        set_keyword_section.classList.remove("hidden");
    } else if (stored_article_type_category === 'url' && set_url_section) {
        set_url_section.classList.remove("hidden");
    }

    get_prompt_data();
   
}

function collectAICheckboxesState() {
    const wrapper = document.getElementById("ai-checkbox-wrapper");
    const checkboxes = wrapper.querySelectorAll('input[type="checkbox"]');
    const result = {};

    checkboxes.forEach(checkbox => {
        // Use the checkbox name as the key, e.g., is_author_selected_by_ai
        result[checkbox.name] = checkbox.checked;
    });

    return result;
}




function add_ai_article_api() {

    const current_page_url = window.location.href;
    
    // Get the form element
    const ai_article_form = document.querySelector('[name="ai_article_form"]');
    
    // Collect form data using the name attributes
    // const ai_article_type_slug_id = ai_article_form.querySelector('[name="ai_article_type_slug_id"]').value;
    const domain_slug_id = ai_article_form.querySelector('[name="ai_domain_slug_id"]').value;
    const prompt_slug_id = ai_article_form.querySelector('[name="prompt_slug_id"]').value;
    // const wp_status = ai_article_form.querySelector('[name="wp_status_ai"]').value;
    const url = ai_article_form.querySelector('[name="url"]').value;
    const keyword = ai_article_form.querySelector('[name="keyword"]').value;
    // const is_category_selected_by_ai = ai_article_form.querySelector('[name="is_category_selected_by_ai"]').checked;
    // const is_category_generated_by_ai = ai_article_form.querySelector('[name="is_category_generated_by_ai"]').checked;
    // const is_tag_selected_by_ai = ai_article_form.querySelector('[name="is_tag_selected_by_ai"]').checked;
    // const is_tag_generated_by_ai = ai_article_form.querySelector('[name="is_tag_generated_by_ai"]').checked;
    // const is_author_selected_by_ai = ai_article_form.querySelector('[name="is_author_selected_by_ai"]').checked;
    // const is_meta_description_generated_by_ai = ai_article_form.querySelector('[name="is_meta_description_generated_by_ai"]').checked;
    // const is_meta_keyword_generated_by_ai = ai_article_form.querySelector('[name="is_meta_keyword_generated_by_ai"]').checked;
    // const is_meta_title_generated_by_ai = ai_article_form.querySelector('[name="is_meta_title_generated_by_ai"]').checked;
    // const is_internal_links_generated_by_ai = ai_article_form.querySelector('[name="is_internal_links_generated_by_ai"]').checked;
    // const is_external_links_generated_by_ai = ai_article_form.querySelector('[name="is_external_links_generated_by_ai"]').checked;

    const author_slug_id_ai = ai_article_form.querySelector('input[name="author_slug_id_ai"]').value;
    const category_slug_id_ai = ai_article_form.querySelector('input[name="category_slug_id_ai"]').value;
    const tag_slug_id_ai = ai_article_form.querySelector('input[name="tag_slug_id_ai"]').value;


    const selectedRadio = ai_article_form.querySelector('input[name="wp_status_ai"]:checked');
    const wp_status_ai = selectedRadio ? selectedRadio.value : null;

    let formatted_date_time = ''

    if(wp_status_ai == 'future'){

        const ai_date = document.querySelector("#ai_date_time_fields input[type='date']");
        const ai_time = document.querySelector("#ai_date_time_fields input[type='time']");
        
        const date_value = ai_date.value;
        const time_value = ai_time.value;
        
        if (date_value && time_value) {
            formatted_date_time = `${date_value}T${time_value}:00Z`;      
        }    
    }

    const aiCheckboxStateJson = collectAICheckboxesState();
    alert(aiCheckboxStateJson)


    const urlParams = new URLSearchParams(window.location.search);
    const ai_article_type_slug_id = urlParams.get("article_type_slug_id");
    const data = new FormData();
    data.append("article_type_slug_id", ai_article_type_slug_id);
    data.append("domain_slug_id", domain_slug_id);
    data.append("prompt_slug_id", prompt_slug_id);
    data.append("wp_status", wp_status_ai);
    data.append("url", url);
    data.append("keyword", keyword);
    data.append("ai_content_flags", JSON.stringify(aiCheckboxStateJson));

    // data.append("is_category_selected_by_ai", is_category_selected_by_ai);
    // data.append("is_category_generated_by_ai", is_category_generated_by_ai);
    // data.append("is_tag_selected_by_ai", is_tag_selected_by_ai);
    // data.append("is_tag_generated_by_ai", is_tag_generated_by_ai);
    // data.append("is_author_selected_by_ai", is_author_selected_by_ai);
    // data.append("is_meta_description_generated_by_ai", is_meta_description_generated_by_ai);
    // data.append("is_meta_keyword_generated_by_ai", is_meta_keyword_generated_by_ai);
    // data.append("is_meta_title_generated_by_ai", is_meta_title_generated_by_ai);
    // data.append("is_internal_links_generated_by_ai", is_internal_links_generated_by_ai);
    // data.append("is_external_links_generated_by_ai", is_external_links_generated_by_ai);
    data.append("author_slug_id", author_slug_id_ai);
    data.append("category_slug_id", category_slug_id_ai);
    data.append("tag_slug_id", tag_slug_id_ai);


    
    (async ()=>{     
        try {
            await add_api(add_article_url, data, list_article_page_url);
        } catch (err) {
            console.error("Error in add_api:", err);
        }        
    })()

}




function get_domain_data(){
    const domain_data = get_data_api(list_domain_url)    
    set_domain_dropdown(domain_data)
}
get_domain_data()




function get_prompt_data(){
    const urlParams = new URLSearchParams(window.location.search);
    const article_type_slug_id = urlParams.get("article_type_slug_id");
    const searchParams = article_type_slug_id;

    const prompt_data = get_data_api(list_prompt_url, null, searchParams)    
    // const prompt_data = get_data_api(list_prompt_url)    
    set_prompt_dropdown(prompt_data)
}
// get_prompt_data();\




function get_author_data_ai(domain_slug_id){

    const author_data = get_data_api(list_author_url, domain_slug_id)    
    //set_author_dropdown
    set_author_dropdown_ai(author_data)
}

function get_category_data_ai(domain_slug_id){

    const category_data = get_data_api(list_category_url, domain_slug_id)    
    //set_category_dropdown
    set_category_dropdown_ai(category_data)
}

function get_tag_data_ai(domain_slug_id){

    const tag_data = get_data_api(list_tag_url, domain_slug_id)    
    //set_tag_dropdown
    set_tag_dropdown_ai(tag_data)
}


