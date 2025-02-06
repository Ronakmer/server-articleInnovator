const modal = document.getElementById('default-modal');
const toggleButton = document.querySelector('[data-modal-toggle]');
const closeModalButton = document.querySelector('.close-modal');

// Function to open the modal
function openModal(tab_id) {
    modal.classList.add('active');
    
    // Tabs - Button
    $("button[data-modal-target='category']").removeClass("text-indigo-600 border-b-2 border-indigo-600 active");
    $("button[data-modal-target='tag']").removeClass("text-indigo-600 border-b-2 border-indigo-600 active");
    $("button[data-modal-target='author']").removeClass("text-indigo-600 border-b-2 border-indigo-600 active");

    $("button[data-modal-target='" + tab_id +"']").addClass("text-indigo-600 border-b-2 border-indigo-600 active");
    console.log("button[data-modal-target='" + tab_id +"']");
    // Content
    $("#category").addClass("hidden");
    $("#tag").addClass("hidden");        
    $("#author").addClass("hidden");
    $("#"+tab_id).removeClass("hidden");

}

// Function to close the modal
function closeModal() {
    modal.classList.remove('active');
}

// Toggle modal visibility
toggleButton.addEventListener('click', openModal);
closeModalButton.addEventListener('click', closeModal);













// Get all tab buttons and contents
const tabButtons = document.querySelectorAll('.tab-modal-button');
const tabContents = document.querySelectorAll('.tab-modal-content');

// Add click event to each tab button
tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons
        tabButtons.forEach(btn => {
            btn.classList.remove('text-indigo-600', 'border-b-2', 'border-indigo-600', 'active');
            btn.classList.add('text-gray-500', 'hover:text-gray-700');
        });
    
        // Add active class to the clicked button
        button.classList.add('text-indigo-600', 'border-b-2', 'border-indigo-600', 'active');
        button.classList.remove('text-gray-500', 'hover:text-gray-700');

        // Show the corresponding tab content
        const target = button.getAttribute('data-modal-target');
        tabContents.forEach(content => {
            if (content.id === target) {
                content.classList.remove('hidden');
            } else {
                content.classList.add('hidden');
            }
        });
    });
}); 

// Show the first tab content by default
document.querySelector('.tab-modal-button.active').click();