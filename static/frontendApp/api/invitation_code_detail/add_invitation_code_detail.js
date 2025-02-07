

function add_invitation_code_detail_api() {

    // Get the form element
    const invitation_code_detail_form = document.querySelector('[name="invitation_code_detail_form"]');

    // Collect form data using the name attributes
    const invitation_code = invitation_code_detail_form.querySelector('[name="invitation_code"]').value;
    const article_limitation = invitation_code_detail_form.querySelector('[name="article_limitation"]').value;
    const domain_limitation = invitation_code_detail_form.querySelector('[name="domain_limitation"]').value;
    const workspace_limitation = invitation_code_detail_form.querySelector('[name="workspace_limitation"]').value;

    const data = new FormData();
    data.append("invitation_code", invitation_code);
    data.append("article_limitation", article_limitation);
    data.append("domain_limitation", domain_limitation);
    data.append("workspace_limitation", workspace_limitation);



    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_invitation_code_detail_url, data, slug_id, list_invitation_code_detail_page_url);
        } else {
            await add_api(add_invitation_code_detail_url, data, list_invitation_code_detail_page_url);
        }
    })()

}


(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_invitation_code_detail_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);


        // Get the form element
        const invitation_code_detail_form = document.querySelector('[name="invitation_code_detail_form"]');

        // Collect form data using the name attributes
        const invitation_code = invitation_code_detail_form.querySelector('[name="invitation_code"]');
        const article_limitation = invitation_code_detail_form.querySelector('[name="article_limitation"]');
        const domain_limitation = invitation_code_detail_form.querySelector('[name="domain_limitation"]');
        const workspace_limitation = invitation_code_detail_form.querySelector('[name="workspace_limitation"]');
    
        if (data_obj && data_obj.invitation_code_details && data_obj.invitation_code_details.length > 0) {
            invitation_code.value = data_obj.invitation_code_details[0].invitation_code;
            article_limitation.value = data_obj.invitation_code_details[0].article_limitation;
            domain_limitation.value = data_obj.invitation_code_details[0].domain_limitation;
            workspace_limitation.value = data_obj.invitation_code_details[0].workspace_limitation;
        } else {
            window.location.href = error_page;
        }
        
    }
})()
     

