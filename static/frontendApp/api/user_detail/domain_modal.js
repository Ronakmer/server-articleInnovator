// Domain Modal
const domain_modal = document.getElementById('domain-modal');
const domain_closeModalButton = document.querySelector('.domain-close-modal');

// Function to open the domain modal
function domain_openModal() {
    if (domain_modal) {
        domain_modal.classList.add('active');
    } else {
        console.error("Domain modal not found!");
    }
}

// Function to close the domain modal
function domain_closeModal() {
    if (domain_modal) {
        domain_modal.classList.remove('active');
    }
}

// Attach close button event
if (domain_closeModalButton) {
    domain_closeModalButton.addEventListener('click', domain_closeModal);
} else {
    console.error("Domain close button not found!");
}





// get domain list 
function get_domain_data(){
    domain_data = get_data_api(list_domain_url)
}

get_domain_data()