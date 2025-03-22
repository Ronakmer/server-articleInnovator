




// Ensure the script runs after the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById('default-modal');
    const closeModalButton = document.querySelector('.close-modal');

    // Function to open the modal
    window.openModal = function (tab_id) { // Attach to the window object for global access
        if (!modal) {
            console.error("Modal element not found.");
            return;
        }

        modal.classList.add('active');

        // Tabs - Button
        $("button[data-modal-target]").removeClass("text-indigo-600 border-b-2 border-indigo-600 active");
        $("button[data-modal-target='" + tab_id + "']").addClass("text-indigo-600 border-b-2 border-indigo-600 active");

        // Content
        $("#category, #tag, #author").addClass("hidden");
        $("#" + tab_id).removeClass("hidden");
    };

    // Function to close the modal
    window.closeModal = function () {
        if (!modal) {
            console.error("Modal element not found.");
            return;
        }
        modal.classList.remove('active');
    };

    // Attach event listener for the close button
    if (closeModalButton) {
        closeModalButton.addEventListener('click', closeModal);
    }
});
    












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