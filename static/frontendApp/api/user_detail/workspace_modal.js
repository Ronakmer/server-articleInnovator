
// Get modal and buttons
const workspace_modal = document.getElementById('workspace-modal');
const openModalButton = document.getElementById('open-modal-btn'); // Ensure this button exists
const closeModalButton = document.querySelector('.workspace-close-modal');

// Function to open the modal
function workspace_openModal() {
    if (workspace_modal) {
        workspace_modal.classList.add('active');
    } else {
        console.error("Modal not found!");
    }
}

// Function to close the workspace_modal
function workspace_closeModal() {
    if (workspace_modal) {
        workspace_modal.classList.remove('active');
    }
}

// Attach event listeners
if (openModalButton) {
    openModalButton.addEventListener('click', workspace_openModal);
} else {
    console.error("Open modal button not found!");
}

if (closeModalButton) {
    closeModalButton.addEventListener('click', workspace_closeModal);
} else {
    console.error("Close modal button not found!");
}


let set_workspace_ids = [];


// get workspace list 
function get_workspace_data(){
    workspace_data = get_data_api(list_workspace_url)
}

get_workspace_data()
