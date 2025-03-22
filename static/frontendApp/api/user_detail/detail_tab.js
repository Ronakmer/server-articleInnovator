
    // Get all tab buttons and contents
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

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
            const target = button.getAttribute('data-target');
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
    document.querySelector('.tab-button.active').click();