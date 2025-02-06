document.addEventListener('DOMContentLoaded', () => {
    tabs();
    const sidebarButtons = document.querySelector('[data-pd-overlay="#docs-sidebar"]');
    const dropdownButtons = document.querySelectorAll('.dropdown-toggle');

    if (dropdownButtons) {
        dropdown();
    }
    if (sidebarButtons) {
        sidebar();
    }
  

});


function sidebar() {
    const sidebarToggle = document.querySelector('[data-pd-overlay="#docs-sidebar"]');

    // Get the sidebar element
    const sidebar = document.getElementById('docs-sidebar');
    // Add event listener to the document
    document.addEventListener('click', function (event) {
        // Check if the clicked element is the sidebar or a descendant of the sidebar
        if (sidebar && !sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) {
            closeSidebar();
        }
    });

    if (sidebarToggle) {
        // Add click event listener to the toggle button
        sidebarToggle.addEventListener('click', () => {
            // Toggle the visibility of the sidebar
            sidebar.classList.toggle('hidden');
            sidebar.classList.toggle('translate-x-0');
            sidebar.classList.toggle('transition-all');
            sidebar.classList.toggle('duration-300');
        });
    }

    // Add event listener to the document
    // document.addEventListener('click', function (event) {
    //     // Check if the clicked element is the sidebar or a descendant of the sidebar
    //         closeSidebar();
    // });
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            // Open the sidebar smoothly after a small delay
            setTimeout(openSidebar, 100);
        });
    }
    // Function to close the sidebar
    function closeSidebar() {
        sidebar.classList.add('hidden');
    }
}


function dropdown(params) {
    var buttons = document.querySelectorAll('.dropdown-toggle');

    buttons.forEach(function (button) {
        button.addEventListener('click', function () {
            var targetId = button.getAttribute('data-target');
            var targetDropdown = document.getElementById(targetId);
            // targetDropdown.toggleAttribute();
            if (targetDropdown.classList.contains('hidden')) {
                setTimeout((function () {
                    targetDropdown.classList.add('open');
                }
                ), 200)
                targetDropdown.classList.remove("hidden");
            } else {
                targetDropdown.classList.add("hidden");
            }

        })
    })
}