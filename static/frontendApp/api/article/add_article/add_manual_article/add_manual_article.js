
// document.addEventListener('DOMContentLoaded', function () {
//     // Run this after the DOM has fully loaded
//     // temp_set_manual_data();
//     setTimeout(() => {
//         temp_set_manual_data();
//     }, 500); 

// });


function temp_set_manual_data() {
    // const temp_article_type_slug_id = localStorage.getItem("article_type_slug_id");
    // const temp_article_type_title = localStorage.getItem("article_type_title");

    const urlParams = new URLSearchParams(window.location.search);
    const stored_article_type_slug_id = urlParams.get("article_type_slug_id");

    // Query the element by ID or name, make sure it's an input element
    // const set_manual_article_type_slug_id = document.querySelector('[name="manual_article_type_slug_id"]'); 
    const set_manual_article_type_title = document.querySelector('[name="manual_article_type_title"]'); 

    const stored_article_type_title = article_type_list.data.find(obj => obj.slug_id === stored_article_type_slug_id)?.title;
    // alert(stored_article_type_title)


    if(stored_article_type_title){

        // Check if the element exists before accessing its value
        // set_manual_article_type_slug_id.value = temp_article_type_slug_id;  
        set_manual_article_type_title.textContent = stored_article_type_title;  
    } 
   
}





function add_manual_article_api() {

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
    const wp_content = manual_article_form.querySelector('#editor').value;

    const wp_slug = manual_article_form.querySelector('[name="wp_slug"]').value;
    const wp_title = manual_article_form.querySelector('[name="wp_title"]').value;
    // const wp_status = manual_article_form.querySelector('[name="wp_status"]').value;
    const wp_content_data = manual_article_form.querySelector('[name="wp_content_data"]').value;

    const wp_excerpt = manual_article_form.querySelector('[name="wp_excerpt"]').value;
    // const manual_article_type_slug_id = manual_article_form.querySelector('[name="manual_article_type_slug_id"]').value;
    const author_slug_id = manual_article_form.querySelector('input[name="author_slug_id"]').value;
    const category_slug_id = manual_article_form.querySelector('input[name="category_slug_id"]').value;
    const tag_slug_id = manual_article_form.querySelector('input[name="tag_slug_id"]').value;
    const wp_featured_image = manual_article_form.querySelector('input[name="wp_featured_image"]').value;
    
    // const wp_status_manual = manual_article_form.querySelector('input[name="wp_status_manual"]:checked').value;
    const selectedRadio = manual_article_form.querySelector('input[name="wp_status_manual"]:checked');
    const wp_status_manual = selectedRadio ? selectedRadio.value : null;
    
    let formatted_date_time = ''

    if(wp_status_manual == 'future'){

        const manual_date = document.querySelector("#manual_date_time_fields input[type='date']");
        const manual_time = document.querySelector("#manual_date_time_fields input[type='time']");
        
        const date_value = manual_date.value;
        const time_value = manual_time.value;
        
        if (date_value && time_value) {
            formatted_date_time = `${date_value}T${time_value}:00Z`;      
        }
        
    }

    const urlParams = new URLSearchParams(window.location.search);
    const manual_article_type_slug_id = urlParams.get("article_type_slug_id");
    



    // const bas64_image = image_to_sting(wp_featured_image)
    // alert(bas64_image)


    // image_to_string(wp_featured_image.files[0], function(base64) {
    //     console.log("Base64 String:", base64);
    // });
    


    console.log("manual_domain_slug_id:", manual_domain_slug_id);
    console.log("wp_slug:", wp_slug);
    console.log("wp_title:", wp_title);
    console.log("wp_content_data:", wp_content_data);
    console.log("wp_excerpt:", wp_excerpt);
    console.log("manual_article_type_slug_id:", manual_article_type_slug_id);
    console.log("author_slug_id:", author_slug_id);
    console.log("category_slug_id:", category_slug_id);
    console.log("tag_slug_id:", tag_slug_id);
    // console.log("wp_featured_image:", wp_featured_image ? wp_featured_image.value : "No image selected");
    console.log("wp_status_manual:", wp_status_manual);


    const data = new FormData();
    data.append("domain_slug_id", manual_domain_slug_id);
    // data.append("wp_slug", wp_slug);
    data.append("wp_slug", slug_data);
    data.append("wp_title", wp_title);
    data.append("wp_content", wp_content_data);
    data.append("wp_excerpt", wp_excerpt);
    data.append("article_type_slug_id", manual_article_type_slug_id);
    data.append("wp_status", wp_status_manual);
    data.append("article_status", 'success');
    data.append("author_slug_id", author_slug_id);
    data.append("category_slug_id", category_slug_id);
    data.append("tag_slug_id", tag_slug_id);
    data.append("wp_featured_image", wp_featured_image);
    

    if(formatted_date_time){
        data.append("wp_schedule_time", formatted_date_time);
    }


    // if (wp_featured_image && wp_featured_image.files && wp_featured_image.files[0]) {
    //     data.append('wp_featured_image', wp_featured_image.files[0]);
    // }

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






// image to string

function image_to_string(image_file, callback) {
    if (image_file) {
        const reader = new FileReader();
        reader.readAsDataURL(image_file);
        reader.onload = function () {
            let base64String = reader.result.split(",")[1];
            callback(base64String); // Pass Base64 string to callback
        };
        reader.onerror = function (error) {
            console.error("Error: ", error);
        };
    }
}



function handleFileUpload(event) {
    let file = event.target.files[0]; // Get the selected file
    if (file) {
        image_to_string(file, function(base64) {
            console.log("Base64 String:", base64);
            alert(base64)
            document.getElementById("image-url").value = base64; 
        });
    }
}
