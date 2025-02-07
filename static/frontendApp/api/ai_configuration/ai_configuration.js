// Function to handle tab selection and field visibility
function handleTabSelection(tab) {
    if (!tab) return; // Prevent errors if the tab is null

    // Reset all tabs' styles
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach((t) => {
        t.style.backgroundColor = ''; // Reset to default background color
        const spanElement = t.querySelector('span');
        if (spanElement) {
            spanElement.style.color = ''; // Reset text color
        }
    });

    // Get selected tab attributes
    const color = tab.getAttribute('data-color');
    const tabName = tab.querySelector('span')?.textContent.trim(); // Safe access with optional chaining

    if (!tabName) return; // Avoid errors if tabName is undefined

    // Apply styles to the selected tab
    tab.style.backgroundColor = color;
    const spanElement = tab.querySelector('span');
    if (spanElement) {
        spanElement.style.color = '#fff';
    }

    // List of field IDs to hide/show
    const fieldIds = [
        'key_id', 'model_id', 'version_id', 'url_id',
        'email_id', 'type_id', 'button_id'
    ];

    // Hide all fields
    fieldIds.forEach(id => {
        const field = document.getElementById(id);
        if (field) {
            field.style.display = "none";
        }
    });

    // Show fields based on the selected tab
    const showFields = {
        'OpenAI': ['key_id', 'model_id', 'button_id', 'email_id'],
        'Azure': ['version_id', 'url_id', 'type_id', 'email_id', 'model_id', 'key_id', 'button_id'],
        'Claude': ['key_id', 'email_id', 'model_id', 'button_id']
    };

    if (showFields[tabName]) {
        showFields[tabName].forEach(id => {
            const field = document.getElementById(id);
            if (field) {
                field.style.display = "block";
            }
        });
    }

    // set hidden input field if it exists
    const apiProviderInput = document.getElementById('api_provider');

    if (apiProviderInput) {
        apiProviderInput.value = tabName;
    }


}

// Function to initialize the tabs on page load
function initializeTabs() {
    const tabs = document.querySelectorAll('.tab');

    tabs.forEach((tab) => {
        tab.addEventListener('click', () => handleTabSelection(tab));
    });

    setTimeout(() => {
        // update time 'api_provider' exists
        const apiProviderInput = document.getElementById('api_provider');
        if (apiProviderInput) {
            const preselectedProvider = apiProviderInput.value;
            if (preselectedProvider) {
                const preselectedTab = Array.from(tabs).find((tab) => {
                    return tab.querySelector('span')?.textContent.trim() === preselectedProvider;
                });
                if (preselectedTab) {
                    handleTabSelection(preselectedTab);
                }
            }
        }
    }, 500);

}

// Ensure the script runs after DOM is fully loaded
document.addEventListener('DOMContentLoaded', initializeTabs);





