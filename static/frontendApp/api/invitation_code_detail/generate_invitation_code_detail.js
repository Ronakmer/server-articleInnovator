


// generate api
async function generate_invitation_code_detail_api() {
    try {

        const access_token = localStorage.getItem("access_token");


        const response = await fetch(generate_invitation_code_detail_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('fetched successfully:', data);
                
                const invitation_code_detail_form = document.querySelector('[name="invitation_code_detail_form"]');
                const invitation_code = invitation_code_detail_form.querySelector('[name="invitation_code"]');
                invitation_code.value = data.invitation_code;


            // show_toast("success", "Roles fetched successfully");
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
