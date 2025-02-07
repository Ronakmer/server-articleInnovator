

function add_motivation_api() {

    // Get the form element
    const motivation_form = document.querySelector('[name="motivation_form"]');

    // Collect form data using the name attributes
    const quote = motivation_form.querySelector('[name="quote"]').value;
    const quote_author = motivation_form.querySelector('[name="quote_author"]').value;
    const start_date = motivation_form.querySelector('[name="start_date"]').value;
    const end_date = motivation_form.querySelector('[name="end_date"]').value;
    const workspace_slug_id = sessionStorage.getItem("workspace_slug_id");


    const data = new FormData();
    data.append("quote", quote);
    data.append("quote_author", quote_author);
    data.append("start_date", start_date);
    data.append("end_date", end_date);
    data.append("workspace_slug_id", workspace_slug_id);


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_motivation_url, data, slug_id, list_motivation_page_url);
        } else {
            await add_api(add_motivation_url, data, list_motivation_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_motivation_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const motivation_form = document.querySelector('[name="motivation_form"]');

        // Collect form data using the name attributes
        const quote = motivation_form.querySelector('[name="quote"]');
        const quote_author = motivation_form.querySelector('[name="quote_author"]');
        const start_date = motivation_form.querySelector('[name="start_date"]');
        const end_date = motivation_form.querySelector('[name="end_date"]');

        if (data_obj && data_obj.motivations && data_obj.motivations.length > 0) {
            quote.value = data_obj.motivations[0].quote;
            quote_author.value = data_obj.motivations[0].quote_author;
            start_date.value = data_obj.motivations[0].start_date;
            end_date.value = data_obj.motivations[0].end_date;
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     

