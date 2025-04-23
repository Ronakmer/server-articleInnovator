document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal-image-gen");
    const openModalButton = document.getElementById("openImageGenModal");
    const closeModalButton = document.getElementById("closeModal");
    const saveButton = document.getElementById("save-image");

    // Open modal when clicking the button
    if (openModalButton) {
        openModalButton.addEventListener("click", function () {
            modal.classList.remove("hidden");
        });
    }

    // Close modal when clicking the close button
    if (closeModalButton) {
        closeModalButton.addEventListener("click", function () {
            modal.classList.add("hidden");
        });
    }
    // Close modal when clicking the close button
    if (saveButton) {
        saveButton.addEventListener("click", function () {
            modal.classList.add("hidden");
        });
    }
});