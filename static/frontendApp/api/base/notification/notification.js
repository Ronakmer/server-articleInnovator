

// notification api
async function notification_api() {
    try {

        const access_token = localStorage.getItem("access_token");
        
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");

        const query_params = new URLSearchParams();

        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }
        query_params.append("read_status", 'False');
    

        const response = await fetch(`${list_notification_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });
        const responseData = await response.json();

        check_authentication_error(responseData)



        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('fetched successfully:', data);

            // const obj = data.notifications;
            set_notification_data(data)
            
        } else {
            const error_data = responseData;
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

notification_api()



function set_notification_data(data) {
    
    let notificationTotal = document.getElementById("notification_total"); // Make sure this element exists in your HTML
    notificationTotal.innerText = (data && data.total_count) ? data.total_count : 0;

    let notificationList = document.getElementById("notification_list"); // Make sure this element exists in your HTML
    notificationList.innerHTML = ""; // Clear existing notifications

    const objs = data.data;

    objs.forEach(obj => {
        notificationList.innerHTML += `
            <li class="p-3 border-b hover:bg-indigo-50">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M15.834 6.66699C17.2147 6.66699 18.334 5.5477 18.334 4.16699C18.334 2.78628 17.2147 1.66699 15.834 1.66699C14.4533 1.66699 13.334 2.78628 13.334 4.16699C13.334 5.5477 14.4533 6.66699 15.834 6.66699Z"
                                stroke="#6F767E" stroke-width="1.25"
                                stroke-linecap="round" stroke-linejoin="round" />
                            <path
                                d="M11.666 1.66699H7.49935C3.33268 1.66699 1.66602 3.33366 1.66602 7.50033V12.5003C1.66602 16.667 3.33268 18.3337 7.49935 18.3337H12.4993C16.666 18.3337 18.3327 16.667 18.3327 12.5003V8.33366"
                                stroke="#6F767E" stroke-width="1.25"
                                stroke-linecap="round" stroke-linejoin="round" />
                        </svg>

                        <p class="text-gray-700 ml-2">${obj.message}</p>
                    </div>
                    <span class="text-gray-500 flex items-center">
                        ${obj.send_time}
                        <svg class="ml-1" width="8" height="8" viewBox="0 0 8 8"
                            fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="4" cy="4" r="4" fill="#4F46E5" />
                        </svg>
                    </span>
                </div>
            </li>
        `;
    });
}





async function read_as_mark(){
    
    const access_token = localStorage.getItem("access_token");

    const workspace_slug_id = localStorage.getItem("workspace_slug_id");

    const data = new FormData();

    // data.append("workspace_slug_id", workspace_slug_id);   
    if(workspace_slug_id){
        data.append("workspace_slug_id", workspace_slug_id);
    }


    try {
        // Perform the API call
        const response = await fetch(list_process_notification_url, {
            // method: 'PUT',
            method: 'PATCH',
            headers: {
                // 'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,

            },
            body: data,
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