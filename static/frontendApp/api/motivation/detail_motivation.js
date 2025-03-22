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

            let workspaces = data.workspace_id_data.map(workspace => workspace.name).join(", ");
            
            modalContent.innerHTML = `
                <div class="p-4 space-y-4">
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Quote:</strong> ${data.quote}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Quote Author:</strong> ${data.quote_author}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Start Date:</strong>${data.start_date}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>End Date:</strong>${data.end_date}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Workspace:</strong>${workspaces}</p>
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









