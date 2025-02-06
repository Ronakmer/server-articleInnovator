

async function add_country_api() {

    // Get the form element
    const country_form = document.querySelector('[name="country_form"]');

    // Collect form data using the name attributes
    const name = country_form.querySelector('[name="name"]').value;
    const country_flag = country_form.querySelector('[name="country_flag"]');

    // // Prepare the data object
    // const data = {
    //     name: name,
    //     country_flag: base64Image,
    // };

    const data = new FormData();
    data.append("name", name);
    if (country_flag && country_flag.files && country_flag.files[0]) {
        data.append('country_flag', country_flag.files[0]);
    }
    // data.append("country_flag", country_flag);


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_country_url, data, slug_id, list_country_page_url);
        } else {
            await add_api(add_country_url, data, list_country_page_url);
        }
    })()

}



(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_country_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const country_form = document.querySelector('[name="country_form"]');

        // Collect form data using the name attributes
        const name = country_form.querySelector('[name="name"]');
        
        if (data_obj && data_obj.countries && data_obj.countries.length > 0) {
            name.value = data_obj.countries[0].name;
            // country_flag.src = data_obj.countries[0].country_flag.files[0];
            // country_flag.src = "https://127.0.0.1:8000/media/country_flag/image_fAaUOyd.png";
        } else {
            // name.value = ''; 
            // window.location.href = error_page;
        }
        
    }
})()
     

