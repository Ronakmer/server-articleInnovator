


async function add_admin_detail_api() {

    // Get the form element
    const admin_detail_form = document.querySelector('[name="admin_detail_form"]');

    let temp_avatar_image_id = '';
    if (avatar_image_id){
        temp_avatar_image_id = avatar_image_id.replace('/media/', '');
    }

    // Collect form data using the name attributes
    const full_name = admin_detail_form.querySelector('[name="full_name"]').value;
    const email = admin_detail_form.querySelector('[name="email"]').value;
    const password = admin_detail_form.querySelector('[name="password"]').value;
    const article_limitation = admin_detail_form.querySelector('[name="article_limitation"]').value;
    const domain_limitation = admin_detail_form.querySelector('[name="domain_limitation"]').value;
    const workspace_limitation = admin_detail_form.querySelector('[name="workspace_limitation"]').value;
    const profile_image = admin_detail_form.querySelector('[name="profile_image"]');


    const data = new FormData();
    data.append("full_name", full_name);
    data.append("email", email);
    data.append("password", password);
    data.append("article_limitation", article_limitation);
    data.append("domain_limitation", domain_limitation);
    data.append("workspace_limitation", workspace_limitation);

    if (profile_image && profile_image.files && profile_image.files[0]) {
        data.append('profile_image', profile_image.files[0]);
    }

    if(temp_avatar_image_id){

        data.append("avatar_image_path", temp_avatar_image_id);
    }


    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_admin_detail_url, data, slug_id, list_admin_detail_page_url);
        } else {
            await add_api(add_admin_detail_url, data, list_admin_detail_page_url);
        }
    })()

}



(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_admin_detail_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const admin_detail_form = document.querySelector('[name="admin_detail_form"]');

        // Collect form data using the name attributes
        const full_name = admin_detail_form.querySelector('[name="full_name"]');
        const email = admin_detail_form.querySelector('[name="email"]');
        const password = admin_detail_form.querySelector('[name="password"]');
        const workspace_id = admin_detail_form.querySelector('[name="workspace_id"]');
        const article_limitation = admin_detail_form.querySelector('[name="article_limitation"]');
        const domain_limitation = admin_detail_form.querySelector('[name="domain_limitation"]');
        const workspace_limitation = admin_detail_form.querySelector('[name="workspace_limitation"]');
            
        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            full_name.value = data_obj.data[0].full_name;
            email.value = data_obj.data[0].user_id.email;
            password.value = data_obj.data[0].password;
            article_limitation.value = data_obj.data[0].article_limitation;
            domain_limitation.value = data_obj.data[0].domain_limitation;
            workspace_limitation.value = data_obj.data[0].workspace_limitation;


        } else {
            window.location.href = error_page;
        }
        
    }
})()
     

