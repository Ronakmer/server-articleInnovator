






// Initialize permissions state
let permissionsList = [];

async function role_has_permissions_list_api() {
    try {
        const access_token = localStorage.getItem("access_token");
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

// Function to render the table with roles and permissions
function renderTable(responseData) {
    const container = document.getElementById("permissionsTable");
    if (!container) {
        console.error("Error: Table container not found");
        return;
    }

    const { roles, grouped_permissions } = responseData.data;

    // Dynamically generate role headers
    const roleHeaders = roles.map(role => `<div class="text-center text-sm font-medium text-gray-900">${formatPermissionName(role.name)}</div>`).join("");

    // Start building the HTML structure with dynamic role headers
    let html = `
        <div class="grid grid-cols-[1fr_repeat(${roles.length},80px)] items-center bg-white border-b py-3 px-4">
            <div class="font-medium text-gray-900">Permissions</div>
            ${roleHeaders}
        </div>
    `;

    // Loop through grouped permissions and render each group with checkboxes for roles
    Object.entries(grouped_permissions).forEach(([groupName, permissions]) => {
        html += `
            <div class="bg-gray-50 px-4 py-3">
                <h3 class="text-sm font-medium text-gray-800">${formatPermissionName(groupName)}</h3>
            </div>
        `;

        permissions.forEach(({ slug_id, name }) => {
            const permissionRow = `
                <div class="grid grid-cols-[1fr_repeat(${roles.length},80px)] items-center bg-white px-4 py-2 border-b last:border-b-0">
                    <div class="text-sm text-gray-600">${formatPermissionName(name)}</div>
                    ${roles.map(role => {
                        const isChecked = hasPermission(roles, role.name, slug_id) ? "checked" : "";
                        return `
                            <div class="flex justify-center">
                                <input type="checkbox" class="permission-checkbox h-4 w-4 rounded border-gray-300 text-blue-600"
                                    data-permission="${slug_id}" data-role="${role.name}" ${isChecked}>
                            </div>
                        `;
                    }).join("")}
                </div>
            `;

            html += permissionRow;

            // Store the initial permissions in the permissions list
            roles.forEach(role => {
                if (hasPermission(roles, role.name, slug_id)) {
                    permissionsList.push({ role: role.name, permission: slug_id, status: true });
                }
            });
        });
    });

    // Update the container's innerHTML with the generated table
    container.innerHTML = html;

    // Handle checkbox changes using event delegation for better performance
    container.addEventListener("change", (e) => {
        if (e.target.classList.contains("permission-checkbox")) {
            const { permission, role } = e.target.dataset;
            const isChecked = e.target.checked;

            // Update the permission status in the permissionsList
            const index = permissionsList.findIndex(p => p.role === role && p.permission === permission);
            if (index !== -1) permissionsList[index].status = isChecked;
            else permissionsList.push({ role, permission, status: isChecked });

            console.log("Updated Permissions List:", permissionsList);

            // Send the updated permissions to the backend
            // updatePermissions(permissionsList);
        }
    });
}

role_has_permissions_list_api();










