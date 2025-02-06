
// document.addEventListener('DOMContentLoaded', function () {
//     // Run this after the DOM has fully loaded
//     temp_set_ai_data();
// });


function temp_set_ai_data() {
    const temp_article_type_slug_id = sessionStorage.getItem("article_type_slug_id");
    const temp_article_type_title = sessionStorage.getItem("article_type_title");

    // Query the element by ID or name, make sure it's an input element
    const set_ai_article_type_slug_id = document.querySelector('[name="ai_article_type_slug_id"]'); // using name or you can use id instead of name
    const set_article_type_title = document.querySelector('[name="article_type_title"]'); // using name or you can use id instead of name

    if(temp_article_type_slug_id){

        // Check if the element exists before accessing its value
        set_ai_article_type_slug_id.value = temp_article_type_slug_id;  // Set the value of the input field
        set_article_type_title.textContent = temp_article_type_title;  // Set the value of the input field
    }
   
}




function add_ai_article_api() {

    const current_page_url = window.location.href;
    
    
    // Get the form element
    const ai_article_form = document.querySelector('[name="ai_article_form"]');
    
    // Collect form data using the name attributes
    const ai_article_type_slug_id = ai_article_form.querySelector('[name="ai_article_type_slug_id"]').value;
    const domain_slug_id = ai_article_form.querySelector('[name="ai_domain_slug_id"]').value;
    const prompt_slug_id = ai_article_form.querySelector('[name="prompt_slug_id"]').value;
    const wp_status = ai_article_form.querySelector('[name="wp_status"]').value;
    const url = ai_article_form.querySelector('[name="url"]').value;
    const keyword = ai_article_form.querySelector('[name="keyword"]').value;

    
    const data = new FormData();
    data.append("article_type_slug_id", ai_article_type_slug_id);
    data.append("domain_slug_id", domain_slug_id);
    data.append("prompt_slug_id", prompt_slug_id);
    data.append("wp_status", wp_status);
    data.append("url", url);
    data.append("keyword", keyword);
    data.append("temp_article_type", 'ai');

    
    (async ()=>{     
        await add_api(add_article_url, data, list_article_page_url);
        
    })()

}




function get_domain_data(){

    domain_data = get_data_api(list_domain_url)    
    //set_domain_dropdown
    set_domain_dropdown(domain_data)
}
get_domain_data()




function get_prompt_data(){

    prompt_data = get_data_api(list_prompt_url)    
    //set_prompt_dropdown
    set_prompt_dropdown(prompt_data)
}
get_prompt_data()
