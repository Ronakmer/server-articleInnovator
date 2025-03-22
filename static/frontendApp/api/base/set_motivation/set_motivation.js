


// get_motivation api
async function get_motivation() {
    try {

        const access_token = localStorage.getItem("access_token");
        
        const workspace_slug_id = localStorage.getItem("workspace_slug_id");
        
        const query_params = new URLSearchParams();
        if (workspace_slug_id) {
            query_params.append("workspace_slug_id", workspace_slug_id);
        }

        const response = await fetch(`${process_motivation_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            // Handle successful response
            const data = await response.json();
            console.log('fetched successfully:', data);       
            const obj = data.data;   
            set_motivation(obj)

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
get_motivation()





function set_motivation(data){
    const element = document.querySelector("#motivation_quote");
    element.innerText = data.quote;
}