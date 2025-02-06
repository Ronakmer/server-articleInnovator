

function show_toast(icon, title, timer = 3000) {
    const toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false, // Ensures no buttons are displayed
        timer: timer,
        timerProgressBar: true, // Displays a progress bar during the timer
        didOpen: (toast) => {
            toast.addEventListener("mouseenter", Swal.stopTimer);
            toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
    });

    toast.fire({
        icon: icon, // 'success', 'error', 'warning', 'info', 'question'
        title: title, // Message text
    });
}




// delete toast
function delete_toast(api_url, slug_id){
    Swal.fire({
        title: 'Are you sure?',
        text: `You won't be able to revert this! Deleting role with ID: ${slug_id}`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            // Proceed with deleting
            delete_api(api_url, slug_id);
        }
    });
}
