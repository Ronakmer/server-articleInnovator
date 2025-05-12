





function handle_permissions() {
    const all_permissions_data = JSON.parse(localStorage.getItem("all_permissions_data")) || [];
    console.log(all_permissions_data, "all_permissions_data");

    // Get all elements with the `data-permission` attribute
    document.querySelectorAll("[data-permission]").forEach((menuItem) => {
        const permissions = menuItem.getAttribute("data-permission").split(",").map(p => p.trim());

        // Show the element if the user has at least one of the permissions
        if (permissions.some(permission => all_permissions_data.includes(permission))) {
            menuItem.classList.remove("hidden");
        }
    });
}



// Ensure this function runs after the page loads
// document.addEventListener("DOMContentLoaded", handle_permissions);

































