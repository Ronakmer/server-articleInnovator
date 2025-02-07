


var file_input = document.getElementById('file-input');

if(file_input){
    file_input.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (!file) return;
    
        const previewContainer = document.getElementById('preview-container');
        const croppedImage = document.getElementById('cropped-image');
        const cropControls = document.getElementById('crop-controls');
        const dragLogoText = document.getElementById('drag-logo-text');
        const chooseFileText = document.getElementById('choose-file-text');
        const cropButton = document.getElementById('crop-button');
        const reader = new FileReader();
    
        let cropper;
    
        reader.onload = function (event) {
            // Show the preview container
            previewContainer.classList.remove('hidden');
    
            // Hide the drag logo and choose file text
            dragLogoText.classList.add('hidden');
            chooseFileText.classList.add('hidden');
    
            // Set the preview image
            croppedImage.src = event.target.result;
    
            // Initialize the cropper
            cropper = new Cropper(croppedImage, {
                aspectRatio: 1,
                viewMode: 1,
                autoCropArea: 1,
                movable: false,
                scalable: false,
                zoomable: false,
            });
    
            // Show crop controls
            cropControls.classList.remove('hidden');
        };
    
        reader.readAsDataURL(file);
    
        document.getElementById('crop-button').addEventListener('click', () => {
            const croppedCanvas = cropper.getCroppedCanvas({
                width: 300,
                height: 300,
            });
    
            croppedImage.src = croppedCanvas.toDataURL();
    
            //  save crop image
            document.getElementById('file-input').files = (function() {
                const dataURL = croppedCanvas.toDataURL();
                const [header, base64] = dataURL.split(',');
                const byteString = atob(base64);
                const arrayBuffer = new ArrayBuffer(byteString.length);
                const uint8Array = new Uint8Array(arrayBuffer);
                for (let i = 0; i < byteString.length; i++) uint8Array[i] = byteString.charCodeAt(i);
                const blob = new Blob([uint8Array], { type: 'image/png' });
                const file = new File([blob], 'image.png', { type: 'image/png' });
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                return dataTransfer.files;
            })();
            
            cropper.destroy(); // Destroy the cropper after cropping
    
        });
    
    
        document.getElementById('reset-button').addEventListener('click', () => {
            cropper.destroy();
            previewContainer.classList.add('hidden');
            cropControls.classList.add('hidden');
            dragLogoText.classList.remove('hidden');
            chooseFileText.classList.remove('hidden');
            cropButton.classList.remove('hidden'); // Show the crop button again when reset
            e.target.value = ""; // Reset file input
        });
    });
    
}






















