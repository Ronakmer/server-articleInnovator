


function open_progress_page(){
 
    const workspace_slug_id = localStorage.getItem("workspace_slug_id");
    
    const domain_slug_id = window.location.pathname.split("/")[2];
    // console.log("UUID:", uuid);


    progress_bar_page_url += `?workspace_slug_id=${workspace_slug_id}&domain_slug_id=${domain_slug_id}`;
    window.location.href = progress_bar_page_url

}