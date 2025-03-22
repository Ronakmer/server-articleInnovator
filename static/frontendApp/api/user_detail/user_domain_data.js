
let slug_id = '';

// user_domain_data_api api
async function user_domain_data_api() {
    try {

        const access_token = localStorage.getItem("access_token");        
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");

        const temp_url = new URL(window.location.href);
        const pathname = temp_url.pathname; 
        slug_id = pathname.split('/').pop();
        
        const query_params = new URLSearchParams();

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }
        if (slug_id) {
            query_params.append("slug_id", slug_id);
        }
        
        const api_url = `${user_domain_revoke_list_url}${slug_id}`
    
        const response = await fetch(`${api_url}?${query_params.toString()}`, {
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

            const domain_data = data.data;

            set_user_domain_data(domain_data);

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

user_domain_data_api()


function set_user_domain_data(domain_data){
    console.log(domain_data,'domain_data')

    // set user workspace in table 
    const user_domain = document.querySelector('[id="user_domain"]');
   


    user_domain.innerHTML = ''; 

    domain_data.forEach((obj, index) => {

        let role_html = '';
        obj.manager_id_data.forEach(manager => {
            if (manager.slug_id === slug_id) {
                role_html += '<span class="px-2 py-1 rounded text-sm bg-purple-100 text-purple-800">Manager</span> ';
            }
        });
    
        obj.writer_id_data.forEach(writer => {
            if (writer.slug_id === slug_id) {
                role_html += '<span class="px-2 py-1 rounded text-sm bg-blue-100 text-blue-800">Writer</span> ';
            }
        });

        
        let role_action = '';
        obj.manager_id_data.forEach(manager => {
            console.log(obj.slug_id,'obj.slug_id')
            if (manager.slug_id === slug_id) {
                role_action += `<button type="button" data-permission="revoke_domain_from_user" onclick="user_domain_revoke_api('${obj.slug_id}', 'manager')" class="bg-red-100 hidden h-10 w-full text-red-700 px-3 py-1.5 rounded-xl text-xs font-medium flex items-center justify-center">Revoke Manager</button>`;
            }
        });
        obj.writer_id_data.forEach(writer => {
            if (writer.slug_id === slug_id) {
                role_action += `<button type="button" data-permission="revoke_domain_from_user" onclick="user_domain_revoke_api('${obj.slug_id}', 'writer')" class="bg-red-100 hidden h-10 w-full text-red-700 px-3 py-1.5 rounded-xl text-xs font-medium flex items-center justify-center">Revoke Writer</button> `;
            }
        });

        const tr = document.createElement('tr');
        tr.classList.add('border-t', 'border-gray-100');

        tr.innerHTML = `
            <td class="py-3.5 pl-4 ">${index + 1}</td>
            <td class="py-3 px-4">${obj.name}</td>
            <td class="py-3 px-4">${obj.workspace_id_data.name}</td>
            <td class="py-3 px-4 text-gray-500">
                <div class="flex gap-3">${role_html}</div>
            </td>
            <td class="py-3 px-4 hidden" data-permission="revoke_domain_from_user">
                <div class="flex gap-3 " >${role_action}</div>
            </td>
        `;

        // Append the row to the workspace table
        user_domain.appendChild(tr);
    
    });
    

}


