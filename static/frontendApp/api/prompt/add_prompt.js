

let article_type_data = '';
let workspace_data = '';
let set_article_type_id = '';
let set_workspace_id = '';



function add_prompt_api() {

    // Get the form element
    const prompt_form = document.querySelector('[name="prompt_form"]');

    // Collect form data using the name attributes
    const name = prompt_form.querySelector('[name="name"]').value;
    const article_type_slug_id = prompt_form.querySelector('[name="article_type_id"]').value;
    const workspace_slug_id = prompt_form.querySelector('[name="workspace_id"]').value;
    const prompt_data = prompt_form.querySelector('[name="prompt_data"]').value;

    const data = new FormData();
    data.append("name", name);
    data.append("article_type_slug_id", article_type_slug_id);
    data.append("workspace_slug_id", workspace_slug_id);
    data.append("prompt_data", prompt_data);



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
        const article_type_slug_id = prompt_form.querySelector('[name="article_type_id"]');
        const workspace_slug_id = prompt_form.querySelector('[name="workspace_id"]');
        const prompt_data = prompt_form.querySelector('[name="prompt_data"]');
    

        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            name.value = data_obj.data[0].name;
            prompt_data.value = JSON.stringify(data_obj.data[0].prompt_data);
            // article_type_slug_id.value = data_obj.data[0].article_type_slug_id;
            // workspace_slug_id.value = data_obj.data[0].workspace_slug_id;

            set_article_type_id = data_obj.data[0].article_type_id_data.slug_id;
            set_workspace_id = data_obj.data[0].workspace_id_data.slug_id;

            
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

