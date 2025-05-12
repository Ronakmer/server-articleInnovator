


function check_authentication_error(responseData){

    // Handle authentication error response
        if (responseData.error && responseData.error.includes("Authentication failed")) {
        window.location.href = login_page_url;
        return; // Stop further execution
    }
}