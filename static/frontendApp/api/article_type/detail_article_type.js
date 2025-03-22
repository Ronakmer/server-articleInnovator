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
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Title:</strong>${data.title}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Article Category:</strong> ${data.article_category}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Category:</strong> ${data.category}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Description:</strong>${data.description}</p>
                    </div>
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Color:</strong>
                        <span class="bg-${data.color_detail_id_data.bg_color} text-${data.color_detail_id_data.text_color} px-4 py-1 text-sm rounded-full">
                            ${data.color_detail_id_data.bg_color}
                        </span>
                        </p>
                    </div>
                    <div class="text-xl font-semibold text-gray-900">
                        <p class="text-lg"><strong>Article Type Image:</strong></p>
                        <div class="flex justify-center">
                            <img src="${data.article_type_image}" alt="${data.title} Flag" class="w-25 h-25 object-cover rounded-lg shadow-lg border-2 border-gray-200" />
                        </div>
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









