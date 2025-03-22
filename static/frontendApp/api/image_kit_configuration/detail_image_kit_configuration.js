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
                        <p><strong>URL End Point:</strong> ${data.url_endpoint}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-800">
                        <p><strong>Public Key:</strong> ${data.public_key}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-800">
                        <p><strong>Private Key:</strong> ${data.private_key}</p>
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









