



// // list api
// async function role_has_permissions_list_api() {
//     try {

//         const access_token = sessionStorage.getItem("access_token");
    

//         const response = await fetch(`${api_url}?${query_params.toString()}`, {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Authorization': `Bearer ${access_token}`
//             },
//         });

//         if (response.ok) {
//             // Handle successful response
//             const data = await response.json();
//             console.log('Roles has permission :', data);
//             return data;
                

//             // show_toast("success", "Roles fetched successfully");
//         } else {
//             const error_data = await response.json();
//             console.error('Failed to fetch roles:', error_data);

//             const errorMessage = error_data.error || "Something went wrong";
//             show_toast("error", `Error: ${errorMessage}`);
//         }
//     } catch (error) {
//         // Handle network or other errors
//         console.error('Network error:', error);
//         show_toast("error", "Network error. Please try again later.");
//     }
// }


// role_has_permissions_list_api()













// const responseData = {
//     "status": "success",
//     "data": {
//         "roles": [
//             {
//                 "name": "admin",
//                 "slug_id": "dde0dc0b-8df8-46fe-bc0d-3d4a611765cc",
//                 "permissions": [
//                     {
//                         "name": "list_workspace",
//                         "slug_id": "4a66d788-469b-44cc-a99c-29b33d4f9e31",
//                         "status": true
//                     },
//                     {
//                         "name": "add_workspace",
//                         "slug_id": "46e9f4b9-ec32-41a8-a891-31ec567c011b",
//                         "status": true
//                     },
//                     {
//                         "name": "update_workspace",
//                         "slug_id": "f5d918c9-933c-420f-99d5-070b85f426ea",
//                         "status": true
//                     }
//                 ]
//             },
//             {
//                 "name": "manager",
//                 "slug_id": "030f008a-3043-43b5-9b59-55f93eb7a1c1",
//                 "permissions": [
//                     {
//                         "name": "list_tag",
//                         "slug_id": "95edd8a0-c37c-43c5-8899-fbee8fa4f71a",
//                         "status": true
//                     },
//                     {
//                         "name": "add_tag",
//                         "slug_id": "ebb31f36-3d2d-46d5-b597-6e1ad56db6e5",
//                         "status": true
//                     }
//                 ]
//             }
//         ],
//         "grouped_permissions": {
//             "jwt": [
//                 {
//                     "slug_id": "61700c72-2bde-4cd7-b09f-08f46fee311c",
//                     "name": "TokenObtainPairView"
//                 },
//                 {
//                     "slug_id": "b077ace8-d7bb-4321-b7a0-d55aea978e48",
//                     "name": "TokenRefreshView"
//                 }
//             ],
//             "login": [
//                 {
//                     "slug_id": "40b4fb85-dfb3-4ea2-a6af-81e0ee95e7a9",
//                     "name": "admin_login"
//                 },
//                 {
//                     "slug_id": "89131360-5557-4191-a25b-fda1c2d85d50",
//                     "name": "admin_logout"
//                 },
//                 {
//                     "slug_id": "1f83228f-ca82-47a4-a245-859535bf8f88",
//                     "name": "send_otp"
//                 }
//             ]
//         }
//     }
// };

// function formatPermissionName(name) {
//     return name.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
// }

// function hasPermission(roleName, permissionSlug) {
//     const role = responseData.data.roles.find(r => r.name === roleName);
//     return role && role.permissions.some(p => p.slug_id === permissionSlug && p.status);
// }

// function renderTable() {
//     const container = document.getElementById('permissionsTable');
//     let html = `
//         <div class="grid grid-cols-[1fr_repeat(3,80px)] items-center bg-white border-b py-3 px-4">
//             <div class="font-medium text-gray-900">Roles</div>
//             <div class="text-center text-sm font-medium text-gray-900">Member</div>
//             <div class="text-center text-sm font-medium text-gray-900">Manager</div>
//             <div class="text-center text-sm font-medium text-gray-900">Admin</div>
//         </div>
//     `;
    
//     Object.entries(responseData.data.grouped_permissions).forEach(([groupName, permissions]) => {
//         html += `
//             <div class="bg-gray-50 px-4 py-3">
//                 <h3 class="text-sm font-medium text-gray-800">${formatPermissionName(groupName)}</h3>
//             </div>
//         `;
//         permissions.forEach(permission => {
//             html += `
//                 <div class="grid grid-cols-[1fr_repeat(3,80px)] items-center bg-white px-4 py-2 border-b last:border-b-0">
//                     <div class="text-sm text-gray-600">${formatPermissionName(permission.name)}</div>
//                     <div class="flex justify-center">
//                         <input type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600" 
//                             data-permission="${permission.slug_id}" 
//                             data-role="member" 
//                             ${hasPermission('member', permission.slug_id) ? 'checked' : ''}>
//                     </div>
//                     <div class="flex justify-center">
//                         <input type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600" 
//                             data-permission="${permission.slug_id}" 
//                             data-role="manager" 
//                             ${hasPermission('manager', permission.slug_id) ? 'checked' : ''}>
//                     </div>
//                     <div class="flex justify-center">
//                         <input type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600" 
//                             data-permission="${permission.slug_id}" 
//                             data-role="admin" 
//                             ${hasPermission('admin', permission.slug_id) ? 'checked' : ''}>
//                     </div>
//                 </div>
//             `;
//         });
//     });
//     container.innerHTML = html;
//     document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
//         checkbox.addEventListener('change', (e) => {
//             const permission = e.target.dataset.permission;
//             const role = e.target.dataset.role;
//             const isChecked = e.target.checked;
//             console.log(`Role: ${role}, Permission: ${permission}, Status: ${isChecked}`);
//         });
//     });
// }

// document.addEventListener('DOMContentLoaded', renderTable);









async function role_has_permissions_list_api() {
    try {
        const access_token = sessionStorage.getItem("access_token");
        const response = await fetch(`${list_role_has_permissions_url}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Roles with permissions:', data);
            renderTable(data); // Render table after fetching
        } else {
            const error_data = await response.json();
            console.error('Failed to fetch roles:', error_data);
            show_toast("error", `Error: ${error_data.error || "Something went wrong"}`);
        }
    } catch (error) {
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later.");
    }
}

// Format permission names
function formatPermissionName(name) {
    return name.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
}

// Check if a role has a specific permission
function hasPermission(roles, roleName, permissionSlug) {
    const role = roles.find(r => r.name === roleName);
    return role && role.permissions.some(p => p.slug_id === permissionSlug && p.status);
}

// Render the permission table dynamically
function renderTable(responseData) {
    const container = document.getElementById('permissionsTable');
    if (!container) {
        console.error('Error: Table container not found');
        return;
    }

    const roles = responseData.data.roles;
    const groupedPermissions = responseData.data.grouped_permissions;

    let html = `
        <div class="grid grid-cols-[1fr_repeat(3,80px)] items-center bg-white border-b py-3 px-4">
            <div class="font-medium text-gray-900">Roles</div>
            <div class="text-center text-sm font-medium text-gray-900">Member</div>
            <div class="text-center text-sm font-medium text-gray-900">Manager</div>
            <div class="text-center text-sm font-medium text-gray-900">Admin</div>
        </div>
    `;

    Object.entries(groupedPermissions).forEach(([groupName, permissions]) => {
        html += `
            <div class="bg-gray-50 px-4 py-3">
                <h3 class="text-sm font-medium text-gray-800">${formatPermissionName(groupName)}</h3>
            </div>
        `;
        permissions.forEach(permission => {
            html += `
                <div class="grid grid-cols-[1fr_repeat(3,80px)] items-center bg-white px-4 py-2 border-b last:border-b-0">
                    <div class="text-sm text-gray-600">${formatPermissionName(permission.name)}</div>
                    <div class="flex justify-center">
                        <input type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600"
                            data-permission="${permission.slug_id}"
                            data-role="member"
                            ${hasPermission(roles, 'member', permission.slug_id) ? 'checked' : ''}>
                    </div>
                    <div class="flex justify-center">
                        <input type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600"
                            data-permission="${permission.slug_id}"
                            data-role="manager"
                            ${hasPermission(roles, 'manager', permission.slug_id) ? 'checked' : ''}>
                    </div>
                    <div class="flex justify-center">
                        <input type="checkbox" class="h-4 w-4 rounded border-gray-300 text-blue-600"
                            data-permission="${permission.slug_id}"
                            data-role="admin"
                            ${hasPermission(roles, 'admin', permission.slug_id) ? 'checked' : ''}>
                    </div>
                </div>
            `;
        });
    });

    container.innerHTML = html;

    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const permission = e.target.dataset.permission;
            const role = e.target.dataset.role;
            const isChecked = e.target.checked;
            console.log(`Role: ${role}, Permission: ${permission}, Status: ${isChecked}`);
            // Add API call here to update permission status
        });
    });
}

// Fetch and render the table when page loads
// document.addEventListener('DOMContentLoaded', role_has_permissions_list_api);


role_has_permissions_list_api()