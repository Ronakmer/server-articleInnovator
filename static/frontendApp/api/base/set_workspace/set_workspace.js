


function set_workspace() {
    const all_workspace_slug_id = localStorage.getItem("all_workspace_slug_id");
    let parsed_workspaces = [];

    if (all_workspace_slug_id) {
        try {
            parsed_workspaces = JSON.parse(all_workspace_slug_id);
        } catch (error) {
            console.error("Error parsing workspace data:", error);
            return;
        }
    }

    // console.log(parsed_workspaces);
    const div_data = document.getElementById('workspace_list');
    div_data.innerHTML = ""; // Clear existing content

    // Define the function here so it can be accessed from event listeners
    function set_workspace_to_session(slug_id, name, logo) {
        const temp_workspace_slug_id = localStorage.getItem("workspace_slug_id");
        
        localStorage.setItem("workspace_slug_id", slug_id);

        if(temp_workspace_slug_id != slug_id){
            location.reload();
        }

        const image = document.getElementById("workspace_logo");  // Assuming you assign an ID to the image
        const text = document.getElementById("workspace_name");  // Assuming you assign an ID to the second <p> tag
    
        // Change the image source
        image.src = logo;  // Set new image source here
    
        // Change the text content of the second <p> tag
        text.textContent = name;  // Set new text here
        
        
    }

    parsed_workspaces.forEach((obj) => {
        const label = document.createElement('label');
        label.classList.add("flex", "items-center", "px-4", "py-3", "text-sm", "cursor-pointer", "rounded-xl", "mb-1", "text-gray-700", "hover:bg-indigo-600/30");

        label.innerHTML = `
            <img src="${obj.logo}" class="w-[26px] h-[26px] mr-2 rounded-full">
            ${obj.name}
        `;

        // Use a closure to pass the values correctly
        label.addEventListener('click', () => set_workspace_to_session(obj.slug_id, obj.name, obj.logo));

        div_data.appendChild(label);
    });
    const temp = localStorage.getItem('workspace_slug_id');

    const temp_filter = parsed_workspaces.filter(t=>t.slug_id == temp);
    if(temp_filter.length == 0 && parsed_workspaces.length > 0 ){
        const {slug_id, name, logo} = parsed_workspaces[0]
        set_workspace_to_session(slug_id, name, logo)

    }else if(temp_filter.length > 0){
        const {slug_id, name, logo} = temp_filter[0]
        set_workspace_to_session(slug_id, name, logo)
    }
}


set_workspace();




