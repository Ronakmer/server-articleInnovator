


let manager_data = '';
let writer_data = '';
let set_manager_ids = '';
let set_writer_ids = '';



function add_domain_api() {

    // Get the form element
    const domain_form = document.querySelector('[name="domain_form"]');

    // Collect form data using the name attributes
    const name = domain_form.querySelector('[name="name"]').value;
    const manager_id = domain_form.querySelector('[name="manager_id"]').value;
    const writer_id = domain_form.querySelector('[name="writer_id"]').value;
    const permalinks = domain_form.querySelector('[name="permalinks"]').value;
    wordpress_username = wp_username 
    wordpress_application_password = wp_password 
    
    // Prepare the data object
    // const data = {
    //     name: name,
    // };
    const data = new FormData();
    data.append("name", name);
    data.append("manager_slug_id", manager_id);
    data.append("writer_slug_id", writer_id);
    data.append("permalinks", permalinks);
    data.append("wordpress_username", wordpress_username);
    data.append("wordpress_application_password", wordpress_application_password);


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            document.getElementById('step2').style.display = 'block';

            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_domain_url, data, slug_id, list_domain_page_url);
        } else {
            // await add_api(add_domain_url, data, list_domain_page_url);

            // const workspace_slug_id = sessionStorage.getItem("workspace_slug_id");
            const workspace_slug_id = '77b4ad49-db8a-4434-aad5-c2351c953cc7';

            const domain_slug_id = sessionStorage.getItem("domain_slug_id");
            
            progress_bar_page_url += `?workspace_slug_id=${workspace_slug_id}&domain_slug_id=${domain_slug_id}`;
            await add_api(add_domain_url, data, progress_bar_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_domain_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const domain_form = document.querySelector('[name="domain_form"]');

        // Collect form data using the name attributes
        const name = domain_form.querySelector('[name="name"]');
        const permalinks = domain_form.querySelector('[name="permalinks"]');
        // wordpress_username = wp_username 
        // wordpress_application_password = wp_password 


        // show step 2 in update time
        document.getElementById('step2').style.display = 'block';


        if (data_obj && data_obj.domains && data_obj.domains.length > 0) {

            name.value = data_obj.domains[0].name;
            permalinks.value = data_obj.domains[0].permalinks;
            wp_username = data_obj.domains[0].wordpress_username;
            wp_password = data_obj.domains[0].wordpress_application_password;

            alert(data_obj.domains[0].manager_id_data[0].slug_id)
            // set_manager_ids = data_obj.domains[0].manager_id_data.map(manager => manager.slug_id);
            set_manager_ids = data_obj.domains[0].manager_id_data[0].slug_id;
            set_writer_ids = data_obj.domains[0].writer_id_data[0].slug_id;

            

        } else {
            // name.value = ''; 
            window.location.href = error_page;
        }
        
    }
})()
     



function get_manager_data(){

    manager_data = get_data_api(list_user_detail_url)
    console.log(manager_data,'000')
}
get_manager_data()


function get_writer_data(){

    writer_data = get_data_api(list_user_detail_url)
    console.log(writer_data,'000')
}
get_writer_data()


