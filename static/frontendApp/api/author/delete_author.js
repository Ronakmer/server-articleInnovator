
//  delete author api
function delete_author_api(slug_id, new_author){

    const api_url = `${delete_author_url}${slug_id}`;

    const current_page_url = window.location.href;
    const domain_slug_id = current_page_url.split('/').pop();


    // delete_api(api_url, slug_id)
    author_delete_toast(api_url, slug_id, new_author, domain_slug_id)

}

// Function to show the delete confirmation toast
function author_delete_toast(api_url, slug_id, new_author, domain_slug_id) {
    // Create input options for author selection if new_author is provided
    let inputOptions = {};
    let defaultInputValue = "";

    if (new_author && Array.isArray(new_author) && new_author.length > 0) {
        console.log(new_author,'new_author')
        inputOptions = new_author.reduce((options, item) => {
            options[item.username] = item.username; // Set both key and value to the name
            return options;
        }, {});

        defaultInputValue = new_author[0].username; // Set the first author's name as the default
    }

    Swal.fire({
        title: "Are you sure?",
        text: `You won't be able to revert this! Deleting author with ID: ${slug_id}.`,
        input: 'select',
        inputOptions: inputOptions,
        inputValue: defaultInputValue, // Set a default selected value if available
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!",
    }).then((result) => {
        if (result.isConfirmed) {
            // Proceed with deleting
            // delete_api(api_url, slug_id, domain_slug_id);
        }
    });
}
