

function add_color_detail_api() {

    // Get the form element
    const color_detail_form = document.querySelector('[name="color_detail_form"]');

    // Collect form data using the name attributes
    const bg_color = color_detail_form.querySelector('[name="bg_color"]').value;
    const text_color = color_detail_form.querySelector('[name="text_color"]').value;

    const data = new FormData();
    data.append("bg_color", bg_color);
    data.append("text_color", text_color);



    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_color_detail_url, data, slug_id, list_color_detail_page_url);
        } else {
            await add_api(add_color_detail_url, data, list_color_detail_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_color_detail_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const color_detail_form = document.querySelector('[name="color_detail_form"]');

        // Collect form data using the name attributes
        const bg_color = color_detail_form.querySelector('[name="bg_color"]');
        const text_color = color_detail_form.querySelector('[name="text_color"]');
    
        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            bg_color.value = data_obj.data[0].bg_color;
            text_color.value = data_obj.data[0].text_color;
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     

