
// document.addEventListener('DOMContentLoaded', function () {
//     // Run this after the DOM has fully loaded
//     temp_set_manual_data();
// });


function temp_set_manual_data() {
    const temp_article_type_slug_id = localStorage.getItem("article_type_slug_id");
    const temp_article_type_title = localStorage.getItem("article_type_title");

    // Query the element by ID or name, make sure it's an input element
    const set_manual_article_type_slug_id = document.querySelector('[name="manual_article_type_slug_id"]'); 
    const set_manual_article_type_title = document.querySelector('[name="manual_article_type_title"]'); 

    if(temp_article_type_slug_id){

        // Check if the element exists before accessing its value
        set_manual_article_type_slug_id.value = temp_article_type_slug_id;  
        set_manual_article_type_title.textContent = temp_article_type_title;  
    }
   
}




function add_ai_article_api() {

    let slug_data = [
        $('#category_permalink').val(),
        $('#year_permalink').val(),
        $('#month_permalink').val(),
        $('#day_permalink').val(),
        $('#hour_permalink').val(),
        $('#minute_permalink').val(),
        $('#second_permalink').val(),
        $('#author_permalink').val(),
        $('#wp_slug_data').val()
    ].filter(Boolean).join('/'); 
    console.log(slug_data, 'slug_data'); 

    // const wp_slug_id = document.querySelector('[name="wp_slug"]');
    // wp_slug_id.value = slug_data;

    
    // Get the form element
    const manual_article_form = document.querySelector('[name="manual_article_form"]');
    
    // Collect form data using the name attributes
    const manual_domain_slug_id = manual_article_form.querySelector('[name="manual_domain_slug_id"]').value;
   
    const wp_slug = manual_article_form.querySelector('[name="wp_slug"]').value;
    const wp_title = manual_article_form.querySelector('[name="wp_title"]').value;
    // const wp_status = manual_article_form.querySelector('[name="wp_status"]').value;
    const wp_content_data = manual_article_form.querySelector('[name="wp_content_data"]').value;

    const wp_excerpt = manual_article_form.querySelector('[name="wp_excerpt"]').value;
    const manual_article_type_slug_id = manual_article_form.querySelector('[name="manual_article_type_slug_id"]').value;
    const author_slug_id = manual_article_form.querySelector('input[name="author_slug_id"]').value;
    const category_slug_id = manual_article_form.querySelector('input[name="category_slug_id"]').value;
    const tag_slug_id = manual_article_form.querySelector('input[name="tag_slug_id"]').value;
    const wp_featured_image = manual_article_form.querySelector('input[name="wp_featured_image"]');
    
    // const wp_status_manual = manual_article_form.querySelector('input[name="wp_status_manual"]:checked').value;
    const selectedRadio = manual_article_form.querySelector('input[name="wp_status_manual"]:checked');
    const wp_status_manual = selectedRadio ? selectedRadio.value : null;

    let formatted_date_time = ''

    if(wp_status_manual == 'scheduled'){

        const manual_date = document.querySelector("#manual_date_time_fields input[type='date']");
        const manual_time = document.querySelector("#manual_date_time_fields input[type='time']");
        
        const date_value = manual_date.value;
        const time_value = manual_time.value;
        
        if (date_value && time_value) {
            formatted_date_time = `${date_value}T${time_value}:00Z`;      
            alert(formatted_date_time)
        }
        
    }


    const data = new FormData();
    data.append("domain_slug_id", manual_domain_slug_id);
    // data.append("wp_slug", wp_slug);
    data.append("wp_slug", slug_data);
    data.append("wp_title", wp_title);
    data.append("wp_content", wp_content_data);
    data.append("wp_excerpt", wp_excerpt);
    data.append("article_type_slug_id", manual_article_type_slug_id);
    data.append("wp_status", wp_status_manual);
    data.append("author_slug_id", author_slug_id);
    data.append("category_slug_id", category_slug_id);
    data.append("tag_slug_id", tag_slug_id);
    data.append("temp_article_type", 'manual');
    

    if(formatted_date_time){
        data.append("wp_schedule_time", formatted_date_time);
    }


    if (wp_featured_image && wp_featured_image.files && wp_featured_image.files[0]) {
        data.append('wp_featured_image', wp_featured_image.files[0]);
    }

    console.log('ronadata:', Object.fromEntries(data.entries()));
    (async ()=>{     
        await add_api(add_article_url, data, list_article_page_url);
        
    })()

}




function get_domain_data(){

    const domain_data = get_data_api(list_domain_url)    
    //set_domain_dropdown
    set_domain_dropdown(domain_data)
}
get_domain_data()




function get_author_data(domain_slug_id){

    const author_data = get_data_api(list_author_url, domain_slug_id)    
    //set_author_dropdown
    set_author_dropdown(author_data)
}

function get_category_data(domain_slug_id){

    const category_data = get_data_api(list_category_url, domain_slug_id)    
    //set_category_dropdown
    set_category_dropdown(category_data)
}

function get_tag_data(domain_slug_id){

    const tag_data = get_data_api(list_tag_url, domain_slug_id)    
    //set_tag_dropdown
    set_tag_dropdown(tag_data)
}



