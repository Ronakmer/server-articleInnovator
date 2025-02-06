

// function convert_file_to_base64(file) {
//     alert(file)
//     return new Promise((resolve, reject) => {
//         const reader = new FileReader();

//         // Define the onload event
//         reader.onload = function() {
//             resolve(reader.result.split(',')[1]); // Extract the base64 part
//         };

//         // Define the onerror event
//         reader.onerror = function(error) {
//             reject(error);
//         };

//         // Read the file as a data URL
//         reader.readAsDataURL(file);
//     });
// }

function convertFileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}
