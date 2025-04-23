


// Listen for Enter key on the form
document.addEventListener("DOMContentLoaded", () => {
    const roleForm = document.getElementById("role_form");

    roleForm.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            event.preventDefault(); // prevent actual form submission
            add_role_api(); // trigger your existing function
        }
    });
});


function add_role_api() {

    // Get the form element
    const role_form = document.querySelector('[name="role_form"]');

    // Collect form data using the name attributes
    const name = role_form.querySelector('[name="name"]').value;

    const data = new FormData();
    data.append("name", name);



    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_role_url, data, slug_id, list_role_page_url);
        } else {
            await add_api(add_role_url, data, list_role_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_role_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const role_form = document.querySelector('[name="role_form"]');

        // Collect form data using the name attributes
        const name = role_form.querySelector('[name="name"]');

        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            name.value = data_obj.data[0].name;
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     

