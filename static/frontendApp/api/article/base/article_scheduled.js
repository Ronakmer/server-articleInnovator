

function ai_toggle_date_time_fields() {
    const date_time_fields = document.getElementById('ai_date_time_fields');
    const selectedRadio = document.querySelector('input[name="wp_status_ai"]:checked').value;

    console.log(selectedRadio, 'selectedRadio');

    // Toggle date-time fields based on "future" radio button value
    if (selectedRadio === 'future') {
        date_time_fields.classList.remove('hidden');  // Show fields
    } else {
        date_time_fields.classList.add('hidden');  // Hide fields
    }
}



function manual_toggle_date_time_fields() {
    const date_time_fields = document.getElementById('manual_date_time_fields');
    const selectedRadio = document.querySelector('input[name="wp_status_manual"]:checked').value;

    console.log(selectedRadio, 'selectedRadio');

    // Toggle date-time fields based on "future" radio button value
    if (selectedRadio === 'future') {
        date_time_fields.classList.remove('hidden');  // Show fields
    } else {
        date_time_fields.classList.add('hidden');  // Hide fields
    }
}


