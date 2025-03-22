

    
// Add Test category
async function add_test_category() {
    const access_token = localStorage.getItem("access_token");

    try{
        const response = await fetch(add_test_category_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,

            },
            body: JSON.stringify(data),
            // body: data,
        });
        if (response.ok) {
            // Handle successful response
            const data = await response.json();
           
            console.log(data)
            

            const loader = document.getElementById('loader6-spinner');
            if (data.status_code === 200 || data.status_code === 201) {
                // categoryLabel.innerText = 'Success';
                
                loader.classList.remove('animate-spin');
                loader.classList.remove('border-t-indigo-600');
                loader.classList.remove('w-6', 'h-6', 'border-2', 'p-2');
                // loader.classList.add('w-10', 'h-10'); // Comment this line if you don’t want to change the size
                
                loader.innerHTML = `<div class=""><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 0C3.592 0 0 3.592 0 8C0 12.408 3.592 16 8 16C12.408 16 16 12.408 16 8C16 3.592 12.408 0 8 0ZM11.824 6.16L7.288 10.696C7.176 10.808 7.024 10.872 6.864 10.872C6.704 10.872 6.552 10.808 6.44 10.696L4.176 8.432C3.944 8.2 3.944 7.816 4.176 7.584C4.408 7.352 4.792 7.352 5.024 7.584L6.864 9.424L10.976 5.312C11.208 5.08 11.592 5.08 11.824 5.312C12.056 5.544 12.056 5.92 11.824 6.16Z" fill="#059669"/>
                    </svg></div>`;

                document.getElementById('loader7').classList.remove('hidden');

                    
                const id = data.response_text.id;
                delete_test_category(id); 

            } 
            if (data.status_code === 401) {
                loader.classList.remove('animate-spin');
                loader.classList.remove('border-t-red-600');
                loader.classList.remove('bg-red-600');
                loader.classList.remove('w-6', 'h-6', 'border-2', 'p-2');

                loader.innerHTML = `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <g clip-path="url(#clip0_496_33571)">
                    <path d="M8 16C12.4183 16 16 12.4183 16 8C16 3.58172 12.4183 0 8 0C3.58172 0 0 3.58172 0 8C0 12.4183 3.58172 16 8 16Z" fill="#FF4141"/>
                    <path d="M8.72798 4.05923C8.72798 3.54111 8.40237 3.12109 8.00071 3.12109C7.59905 3.12109 7.27344 3.54111 7.27344 4.05923V9.94386C7.27344 10.462 7.59905 10.882 8.00071 10.882C8.40237 10.882 8.72798 10.462 8.72798 9.94386V4.05923Z" fill="white"/>
                    <path d="M8.00067 12.8773C8.40231 12.8773 8.72791 12.5517 8.72791 12.1501C8.72791 11.7484 8.40231 11.4229 8.00067 11.4229C7.59903 11.4229 7.27344 11.7484 7.27344 12.1501C7.27344 12.5517 7.59903 12.8773 8.00067 12.8773Z" fill="white"/>
                    </g>
                    <defs>
                    <clipPath id="clip0_496_33571">
                    <rect width="16" height="16" fill="white"/>
                    </clipPath>
                    </defs>
                </svg>`

                ErrorDomain =  document.getElementById('ErrorDomain')

                ErrorDomain.innerHTML = '<strong>Error:</strong> Unauthorized';
                ErrorDomain.classList.add('p-2', 'mb-4', 'border', 'border-gray-200', 'rounded-lg', 'text-xs', 'bg-red-100', 'text-red-600');

            }
            if (data.status_code === 404) {

                loader.classList.remove('animate-spin');
                loader.classList.remove('border-t-red-600');
                loader.classList.remove('bg-red-600');
                loader.classList.remove('w-6', 'h-6', 'border-2', 'p-2');

                loader.innerHTML = `<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <g clip-path="url(#clip0_496_33571)">
                    <path d="M8 16C12.4183 16 16 12.4183 16 8C16 3.58172 12.4183 0 8 0C3.58172 0 0 3.58172 0 8C0 12.4183 3.58172 16 8 16Z" fill="#FF4141"/>
                    <path d="M8.72798 4.05923C8.72798 3.54111 8.40237 3.12109 8.00071 3.12109C7.59905 3.12109 7.27344 3.54111 7.27344 4.05923V9.94386C7.27344 10.462 7.59905 10.882 8.00071 10.882C8.40237 10.882 8.72798 10.462 8.72798 9.94386V4.05923Z" fill="white"/>
                    <path d="M8.00067 12.8773C8.40231 12.8773 8.72791 12.5517 8.72791 12.1501C8.72791 11.7484 8.40231 11.4229 8.00067 11.4229C7.59903 11.4229 7.27344 11.7484 7.27344 12.1501C7.27344 12.5517 7.59903 12.8773 8.00067 12.8773Z" fill="white"/>
                    </g>
                    <defs>
                    <clipPath id="clip0_496_33571">
                    <rect width="16" height="16" fill="white"/>
                    </clipPath>
                    </defs>
                </svg>`


                ErrorDomain =  document.getElementById('ErrorDomain')

                ErrorDomain.innerHTML = '<strong>Error:</strong> Please download and connect botoxbyte plugin';
                ErrorDomain.classList.add('p-2', 'mb-4', 'border', 'border-gray-200', 'rounded-lg', 'text-xs', 'bg-red-100', 'text-red-600');

            }

        } else {
            
            const error_data = await response.json();

            console.log(error_data)
            // Show api error
            var error_message = error_message_data(error_data);
            

            // Show the toast
            show_toast("error", `Error: ${error_message}`);
        
        }
    
    
    }
    catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("Network error. Please try again later");
    }
}

// add_test_category();