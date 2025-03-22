


// user_workspace_data_api api
async function user_workspace_data_api() {
    try {

        const access_token = localStorage.getItem("access_token");        
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");

        const temp_url = new URL(window.location.href);
        const pathname = temp_url.pathname; 
        const slug_id = pathname.split('/').pop();
        
        const query_params = new URLSearchParams();

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }

        if (slug_id) {
            query_params.append("slug_id", slug_id);
        }
    
        const response = await fetch(`${list_user_detail_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('successfully:', data);

            const user_data = data.data;

            set_user_workspace_data(user_data);

        } else {
            const error_data = await response.json();
            console.error('Failed to fetch roles:', error_data);

            const errorMessage = error_data.error || "Something went wrong";
            show_toast("error", `Error: ${errorMessage}`);
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later.");
    }
}

user_workspace_data_api()





function set_user_workspace_data(user_data){
    console.log(user_data,'user_data')
    const user_image = document.querySelector('[id="user_image"]');
    const user_full_name = document.querySelector('[id="user_full_name"]');
    const user_email = document.querySelector('[id="user_email"]');
    
    user_image.src = user_data[0].profile_image;
    user_full_name.textContent = user_data[0].full_name;
    user_email.textContent = user_data[0].user_id.email;
    

    // set user workspace in table 
    const user_workspace = document.querySelector('[id="user_workspace"]');

    user_workspace.innerHTML = ''; 

    user_data.forEach((obj) => {
        const workspaces = obj.workspace_id;
        
        // Loop through each workspace
        workspaces.forEach((obj, index) => {
            const tr = document.createElement('tr');
            tr.classList.add('border-t', 'border-gray-100');

            tr.innerHTML = `
                <td class="py-3.5 pl-4 ">${index + 1}</td>
                <td class="py-3 px-4">${obj.name}</td>
                <td class="py-3 px-4">
                    <button type="button" data-permission="revoke_workspace_from_user"  onclick="user_workspace_revoke_api('${obj.slug_id}')" class="bg-red-100 hidden h-10 w-full text-red-700 px-3 py-1.5 rounded-xl text-xs font-medium flex items-center justify-center">Revoke</button>
                </td>
            `;

            // Append the row to the workspace table
            user_workspace.appendChild(tr);
        });
    });
    

}

