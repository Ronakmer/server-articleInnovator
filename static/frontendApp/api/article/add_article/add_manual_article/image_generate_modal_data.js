

// Store selected images
let selectedImages = [];

// Function to populate the image grid
function set_google_image_data(imageResults) {
    const container = document.querySelector('.image-container');
    container.innerHTML = ""; // Clear existing images

    if (!imageResults || imageResults.length === 0) {
        container.innerHTML = "<p>No images found.</p>";
        return;
    }

    imageResults.forEach((image) => {
        const imageBox = document.createElement('div');
        imageBox.classList.add('relative', 'break-inside-avoid', 'mainbox-cls');

        imageBox.innerHTML = `
            <img src="${image.image}" alt="${image.title}" class="w-full h-auto rounded-lg shadow-md">
            <div class="absolute top-2 left-2">
                <input type="checkbox" class="form-checkbox h-5 w-5 text-blue-600 rounded focus:ring-blue-500 border-gray-300" 
                    data-image-url="${image.image}" onchange="handleImageSelection(this)">
            </div>
        `;

        container.appendChild(imageBox);
    });
}

// Function to handle image selection
function handleImageSelection(checkbox) {
    const imageUrl = checkbox.getAttribute("data-image-url");
    
    if (checkbox.checked) {
        if (!selectedImages.includes(imageUrl)) {
            selectedImages.push(imageUrl);
        }
    } else {
        selectedImages = selectedImages.filter(url => url !== imageUrl);
    }

    updateSelectedImages();
}

// Function to update selected images section
function updateSelectedImages() {
    const selectedContainer = document.querySelector('.selected-images-container');
    selectedContainer.innerHTML = ""; // Clear existing images

    selectedImages.forEach((url, index) => {
        const imageElement = document.createElement('div');
        imageElement.classList.add('relative');

        imageElement.innerHTML = `
            <div class="items-center">
                <div>
                    <img src="${url}" alt="Selected Image" class="w-full object-cover mr-3">
                </div>
            </div>
            <!-- Remove icon -->
            <button class="remove-option absolute top-1 right-1 bg-red-600 shadow-md rounded-full p-1"
                onclick="removeSelectedImage(${index})">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        `;

        selectedContainer.appendChild(imageElement);
    });
}

// Function to remove selected image and uncheck checkbox
function removeSelectedImage(index) {
    const removedImageUrl = selectedImages[index];

    // Remove the image from the selected list
    selectedImages.splice(index, 1);
    updateSelectedImages();

    // Find and uncheck the corresponding checkbox
    const checkboxes = document.querySelectorAll('.image-container input[type="checkbox"]');
    checkboxes.forEach((checkbox) => {
        if (checkbox.getAttribute("data-image-url") === removedImageUrl) {
            checkbox.checked = false;
        }
    });
}









function set_image_template_data(response) {


    const container = document.querySelector(".select-template"); // Target the grid container
    container.innerHTML = ""; // Clear existing content

    if (!response.success || !response.data.length) {
        container.innerHTML = "<p class='text-gray-500'>No templates found.</p>";
        return;
    }

    response.data.forEach((item) => {
        const template = document.createElement("div");
        template.classList.add("relative", "break-inside-avoid", "mainbox-cls");

        template.innerHTML = `
            <img src="${item.template_image_path}" 
                alt="${item.name}"
                class="w-full h-auto rounded-xl shadow-md">
            
        `;

        container.appendChild(template);
    });

}











function set_generated_images(data){

    if (data.success && data.urls.length > 0) {
        let container = document.querySelector(".generated-images");
        container.innerHTML = ""; // Clear existing images

        data.urls.forEach((item, index) => {
            let div = document.createElement("div");
            div.className = "relative break-inside-avoid mainbox-cls";

            div.innerHTML = `
                <img src="${item.url}" alt="Generated image" class="w-full h-auto rounded-xl shadow-md">
                <div class="absolute top-2 left-2">
                    <input type="radio" name="selectedImage" value="${item.url}" class="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300" ${index === 0 ? 'checked' : ''}>
                </div>
            `;

            container.appendChild(div);
        });
        // Add event listener for radio buttons
        document.querySelectorAll('input[name="selectedImage"]').forEach(radio => {
            radio.addEventListener('change', function () {
                document.getElementById("image-url").value = this.value; 

            });
        });
    }

}

