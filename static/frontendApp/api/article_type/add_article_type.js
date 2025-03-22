
let article_type_field_data = '';
let color_detail_data = '';
let set_color_slug_id = '';
let set_article_type_field_slug_id = '';


function add_article_type_api() {

    // Get the form element
    const article_type_form = document.querySelector('[name="article_type_form"]');

    // Collect form data using the name attributes
    const article_category = article_type_form.querySelector('[name="article_category"]').value;
    const category = article_type_form.querySelector('[name="category"]').value;
    const article_type_field_slug_id = article_type_form.querySelector('[name="article_type_field"]').value;
    const color_detail_slug_id = article_type_form.querySelector('[name="color"]').value;
    const title = article_type_form.querySelector('[name="title"]').value;
    const description = article_type_form.querySelector('[name="description"]').value;
    const article_type_image = article_type_form.querySelector('[name="article_type_image"]');

    console.log(category,'120')
    const data = new FormData();
    data.append("article_category", article_category);
    data.append("category", category);
    data.append("article_type_field_slug_id", article_type_field_slug_id);
    data.append("color_detail_slug_id", color_detail_slug_id);
    data.append("title", title);
    data.append("description", description);

    if (article_type_image && article_type_image.files && article_type_image.files[0]) {
        data.append('article_type_image', article_type_image.files[0]);
    }



    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_article_type_url, data, slug_id, list_article_type_page_url);
        } else {
            await add_api(add_article_type_url, data, list_article_type_page_url);
        }
    })()

}



(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_article_type_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const article_type_form = document.querySelector('[name="article_type_form"]');

        // Collect form data using the name attributes
        const article_category = article_type_form.querySelector('[name="article_category"]');
        const category = article_type_form.querySelector('[name="category"]');
        const article_type_field_slug_id = article_type_form.querySelector('[name="article_type_field"]');
        const color_slug_id = article_type_form.querySelector('[name="color"]');
        const title = article_type_form.querySelector('[name="title"]');
        const description = article_type_form.querySelector('[name="description"]');
        const article_type_image = article_type_form.querySelector('[name="article_type_image"]');
    
        
        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            article_category.value = data_obj.data[0].article_category;
            category.value = data_obj.data[0].category;
            title.value  = data_obj.data[0].title;
            description.value  = data_obj.data[0].description;            
            set_color_slug_id = data_obj.data[0].color_detail_id_data.slug_id
            set_article_type_field_slug_id = data_obj.data[0].article_type_field_id_data.map(field => field.slug_id).join(', ')
            
        } else {
            // name.value = ''; 
            window.location.href = error_page;
        }
        
    }
})()
     

function get_article_type_field_data(){

    article_type_field_data = get_data_api(list_article_type_field_url)
}
get_article_type_field_data()



function get_color_detail_data(){
    
    color_detail_data = get_data_api(list_color_detail_url)
}
get_color_detail_data()
