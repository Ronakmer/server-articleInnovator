

    
// Add Test category
async function delete_test_category(test_category_id) {
    const access_token = localStorage.getItem("access_token");

    data.test_category_id = test_category_id;

    console.log(data)
    try{
        const response = await fetch(delete_test_category_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`,
            },
            body: JSON.stringify(data),
            // body: data,
        });

        const responseData = await response.json();

        check_authentication_error(responseData)


        if (response.ok) {
            // Handle successful response
            const data = responseData;
           
            console.log(data)
            

            // const deletecategoryLabel = document.getElementById('delete_test_category_id');
            const loader = document.getElementById('loader7-spinner');
                
            if (data.status_code === 200 || data.status_code === 201) {
                // deletecategoryLabel.innerText = 'Success';
                loader.classList.remove('animate-spin');
                loader.classList.remove('border-t-indigo-600');
                loader.classList.remove('w-6', 'h-6', 'border-2', 'p-2');
                // loader.classList.add('w-10', 'h-10'); // Comment this line if you don’t want to change the size
                
                loader.innerHTML = `<div class=""><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 0C3.592 0 0 3.592 0 8C0 12.408 3.592 16 8 16C12.408 16 16 12.408 16 8C16 3.592 12.408 0 8 0ZM11.824 6.16L7.288 10.696C7.176 10.808 7.024 10.872 6.864 10.872C6.704 10.872 6.552 10.808 6.44 10.696L4.176 8.432C3.944 8.2 3.944 7.816 4.176 7.584C4.408 7.352 4.792 7.352 5.024 7.584L6.864 9.424L10.976 5.312C11.208 5.08 11.592 5.08 11.824 5.312C12.056 5.544 12.056 5.92 11.824 6.16Z" fill="#059669"/>
                    </svg></div>`;

                // document.getElementById('loader6').classList.remove('hidden');
                document.getElementById('step2').classList.remove('hidden');
                // Optionally, you can adjust the position of step2 to be below step1
                document.getElementById('step2').style.display = 'block';

                document.getElementById("step2-circle").classList.add("bg-indigo-600");
                document.getElementById("line2").classList.add("bg-indigo-600");
                


            }
            if (data.status_code === 401) {
                loader.innerText = 'Unauthorized';
            }
            

        } else {
            
            const error_data = responseData;

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
