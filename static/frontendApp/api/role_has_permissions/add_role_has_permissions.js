

async function add_role_has_permissions_api() {

    const rolesData = [];

    const groupedByRole = permissionsList.reduce((acc, { role, permission, status }) => {
        if (status) {
            if (!acc[role]) acc[role] = [];
            acc[role].push(permission);
        }
        return acc;
    }, {});

    Object.entries(groupedByRole).forEach(([role, permissions]) => {
        rolesData.push({
            role: role,
            permissions: permissions.join(", ")
        });
    });

    console.log("Generated Roles Data:", rolesData);

    const access_token = localStorage.getItem("access_token");

    try {
        // Perform the API call
        const response = await fetch(add_role_has_permissions_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,

            },
            body: JSON.stringify(rolesData),
            // body: data,
        });
        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
           
            console.log(data)
            show_toast("success", `${data.message}`);

            // Redirect or show a success message
            if (response.ok) {
                setTimeout(() => {
                    location.reload();  
                }, 1000);
            }

        } else {
            
            const error_data = responseData;

            console.log(error_data)
            // Show api error
            var error_message = error_message_data(error_data);
            

            // Show the toast
            show_toast("error", `Error: ${error_message}`);
        
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("Network error. Please try again later");
    }
}


