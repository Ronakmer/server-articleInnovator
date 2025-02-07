

function error_message_data(error_data){

    var error_messages = ''

    // Check if there are specific field errors
    if (error_data.errors) {
        let fieldErrors = '';
        
        // Loop through all fields in the errors object
        for (const [field, messages] of Object.entries(error_data.errors)) {
            // Append each field error to fieldErrors
            fieldErrors += `<br><strong>${field}:</strong> ${messages.join(', ')}`;
        }
        
        // Add the field errors to the general error message
        error_messages += fieldErrors;
    }
    
    else{
        error_messages = error_data.error || "Something went wrong";
    }
    return error_messages.trim(); 
} 
        