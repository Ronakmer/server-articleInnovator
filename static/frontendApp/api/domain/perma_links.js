// Function to toggle the selected tag in the input box
function perma_links(tag) {
        
    const inputField = document.getElementById('tagInput'); // Get the input field
    const currentValue = inputField.value; // Get the current value of the input
    const tagWithSlashes = `/${tag}/`; // Format the tag

    console.log({tagWithSlashes,currentValue})
    // Check if the tag is already present in the input
    if (currentValue.includes(tagWithSlashes)) {
        // Remove the tag if it exists
        inputField.value = currentValue.replace(tagWithSlashes, '/');
        if(inputField.value == '/'){
            inputField.value = '';
        }

    } else {
        // Append the tag if it does not exist
        inputField.value = (currentValue + tagWithSlashes).replaceAll('//','/'); 
    }
}

