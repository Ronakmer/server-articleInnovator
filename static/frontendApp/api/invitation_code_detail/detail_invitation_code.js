// Function to handle modal data and open it
function modal_data(data, title) {

    // Find the modal and its elements
    let modal = document.getElementById('base_modal');
    let modalTitle = document.getElementById('base_modal_title');
    let modalContent = document.getElementById('base_modal_content');
    let closeModalButton = document.getElementById('base_modal_close');

    // Set dynamic content in the modal
    if (data) {
        modalTitle.innerText = title || "Default Title"; // Set the modal title
    }

    // Function to open the modal
    function openModal() {
        if (modal) {
            modal.classList.add('active');

            modalContent.innerHTML = `
                <div class="p-4 space-y-4">
                    <div class="text-xl font-semibold text-gray-800">
                        <p><strong>Invitation Code:</strong> ${data.invitation_code}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-800">
                        <p><strong>Article Limitation:</strong> ${data.article_limitation}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-800">
                        <p><strong>Domain Limitation:</strong> ${data.domain_limitation}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-800">
                        <p><strong>Workspace Limitation:</strong> ${data.workspace_limitation}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-800">
                        <p><strong>Used:</strong>
                        ${data.used === false ? 
                            `<span class="bg-green-500 text-white px-4 py-1 text-sm rounded-full">
                                   Not Used
                                </span>` 
                            : `<span class="bg-red-600 text-white px-4 py-1 text-sm rounded-full">
                                   Used
                                </span>`}
                        
                        </p>
                    </div>
                    <div class="text-xl font-semibold text-gray-800">
                        <p><strong>Used Date:</strong> ${data.used_date}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-800">
                        <p><strong>Email:</strong> ${data.email_data.username}</p>
                    </div>
                </div>
            `; 

        } 
    }

    // Function to close the modal
    function closeModal() {
        if (modal) {
            modal.classList.remove('active');
        }
    }

    // Open the modal
    openModal();

    // Attach event listener to close modal button
    if (closeModalButton) {
        closeModalButton.addEventListener('click', closeModal);
    } 
}









