
// workspace
document.addEventListener('DOMContentLoaded', function () {

    const workspace_div = ai_configuration_form.querySelector('[id="workspace-div"]');

    if(workspace_div){

    
        workspace_data.then((response) => {

            
            const teamMembers = response.data || [];  // Ensure data is loaded
            

            let workspace_ids = [];
            const workspaceInput = document.querySelector('input[name="workspace_id"]'); // Reference to the hidden input


            // set the hidden input value with the workspace_ids as a comma-separated string
            function setWorkspaceInput() {
                workspaceInput.value = workspace_ids.join(',');
            }
            

            const customSelect = document.querySelector('.member_custom_select');
            const selectedItemsContainer = document.querySelector('.member_selected_items');
            const dropdownContainer = document.querySelector('.member_custom_select_dropdown');
            const input = document.querySelector('.member_custom_select input');

            function createTeamMemberElement(member) {
                const div = document.createElement('div');
                div.className = 'px-4 cursor-pointer flex items-center';
                div.innerHTML = `
                    <label class="flex w-full items-center p-2 text-sm rounded-xl mb-1 text-gray-600 bg-white hover:bg-indigo-600/15" id="set_workspace_${member.slug_id}">
                    <input type="checkbox" class="mr-2"> 
                    <img src="${member.logo}" alt="${member.name}" class="w-6 h-6 mr-1 rounded-full">
                    ${member.name}
                    </label>
                    `;
                div.dataset.slug_id = member.slug_id;

                const label = div.querySelector('label');
                const checkbox = div.querySelector('input[type="checkbox"]');

                label.addEventListener('click', function () {
                    if (!checkbox.checked) {
                        checkbox.checked = true;
                        label.classList.add('bg-indigo-600/15');
                        label.classList.remove('bg-white');
                        addMemberToSelectedList(member);
                    } else {
                        checkbox.checked = false;
                        label.classList.remove('bg-indigo-600/15');
                        label.classList.add('bg-white');
                        removeMemberFromSelectedList(member.slug_id);
                    }
                });

                return div;
            }

            function createSelectedItemElement(member) {
                const div = document.createElement('div');
                div.className = 'bg-blue-100 rounded-full relative px-3 py-2 flex items-center text-sm';
                div.innerHTML = `
                    <img src="${member.logo}" alt="${member.name}" class="w-4 h-4 rounded-full mr-1">
                    <span class="mr-1">${member.name}</span>
                    <button class="absolute top-1 -right-0 hover:opacity-90" data-id="${member.slug_id}">
                    <svg width="10" height="10" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 0C2.245 0 0 2.245 0 5C0 7.755 2.245 10 5 10C7.755 10 10 7.755 10 5C10 2.245 7.755 0 5 0ZM6.68 6.15C6.825 6.295 6.825 6.535 6.68 6.68C6.605 6.755 6.51 6.79 6.415 6.79C6.32 6.79 6.225 6.755 6.15 6.68L5 5.53L3.85 6.68C3.775 6.755 3.68 6.79 3.585 6.79C3.49 6.79 3.395 6.755 3.32 6.68C3.175 6.535 3.175 6.295 3.32 6.15L4.47 5L3.32 3.85C3.175 3.705 3.175 3.465 3.32 3.32C3.465 3.175 3.705 3.175 3.85 3.32L5 4.47L6.15 3.32C6.295 3.175 6.535 3.175 6.68 3.32C6.825 3.465 6.825 3.705 6.68 3.85L5.53 5L6.68 6.15Z" fill="#DF6137"/>
                    </svg>
                    </button>
                    `;
                return div;
            }


            function addMemberToSelectedList(member) {
                // Check if the member is already added by slug_id
                const isAlreadySelected = [...selectedItemsContainer.children].some(item => {
                    return item.querySelector('button').dataset.id === member.slug_id;
                });
            
                if (!isAlreadySelected) {
                    // If not already selected, create and append the member
                    const selectedItem = createSelectedItemElement(member);
                    selectedItemsContainer.appendChild(selectedItem);
                    input.value = ''; // Clear the input
                    input.focus(); // Refocus the input

                    // set slug_id in list
                    workspace_ids.push(member.slug_id);
                    setWorkspaceInput();


                } else {
                    console.log(`Member with slug_id ${member.slug_id} is already selected.`);
                }
            }
            

            function removeMemberFromSelectedList(slug_id) {
                // Remove from selectedItemsContainer
                const itemToRemove = selectedItemsContainer.querySelector(`button[data-id="${slug_id}"]`);
                if (itemToRemove) {
                    itemToRemove.closest('div').remove();
                    input.focus();

                    // remove slug_id in list
                    workspace_ids = workspace_ids.filter(id => id !== slug_id);
                    setWorkspaceInput();

                }
            
                // Remove from dropdownContainer
                const memberElement = dropdownContainer.querySelector(`[data-slug_id="${slug_id}"]`);
                if (memberElement) {
                    const checkbox = memberElement.querySelector('input[type="checkbox"]');
                    if (checkbox) {
                        checkbox.checked = false;
                    }
            
                    const label = memberElement.querySelector('label');
                    if (label) {
                        label.classList.remove('bg-indigo-600/15');
                        label.classList.add('bg-white');
                    }
                }
            }

            if(dropdownContainer){
                teamMembers.forEach(member => {
                    const memberElement = createTeamMemberElement(member);
                    dropdownContainer.appendChild(memberElement);
                });
            }

            if(customSelect){
                input.addEventListener('focus', () => {
                    customSelect.classList.add('active');
                });
            }

            if(input){
                input.addEventListener('input', () => {
                    const searchTerm = input.value.toLowerCase();
                    Array.from(dropdownContainer.children).forEach(child => {
                        const name = child.querySelector('label').textContent.toLowerCase();
                        child.style.display = name.includes(searchTerm) ? '' : 'none';
                    });
                });
            }

            
            // update time set data
            // setTimeout(() => {
            
            //     if (typeof set_workspace_ids === 'string') {
            //         if (set_workspace_ids.includes(',')) {
            //             // If it's a comma-separated list, split it and trim each item
            //             set_workspace_ids = set_workspace_ids.split(',').map(item => item.trim());
            //         } else {
            //             // If it's a single ID, wrap it in an array
            //             set_workspace_ids = [set_workspace_ids.trim()];
            //         }
            //     }
                
                
            //     // update time set data
            //     if (Array.isArray(set_workspace_ids)) {
            //         set_workspace_ids.forEach(workspaceId => {
            //             console.log(`Workspace ID: ${workspaceId}`);
            //             document.getElementById(`set_workspace_${workspaceId}`).click();

            //         });
            //     } else {
            //         console.error('set_workspace is not an array:', set_workspace_ids);
            //     }
            // }, 100);


            if(input){
                // Add keydown event listener for backspace functionality
                input.addEventListener('keydown', (e) => {
                    if (e.key === 'Backspace' && input.value === '' && selectedItemsContainer.lastChild) {
                        const lastSelectedItem = selectedItemsContainer.lastChild;
                        const id = lastSelectedItem.querySelector('button').dataset.id;
                        console.log(id,'89')
                        removeMemberFromSelectedList(id);
                    }
                });
            }

            if(selectedItemsContainer){

                // Use event delegation for close button clicks
                selectedItemsContainer.addEventListener('click', (e) => {
                    if (e.target.closest('button')) {
                        const id = e.target.closest('button').dataset.id;
                        removeMemberFromSelectedList(id);
                    }
                });
                setWorkspaceInput();
                
            }

            document.addEventListener('click', (e) => {
                if (!customSelect.contains(e.target)) {
                    customSelect.classList.remove('active');
                }
            });



        }) 

    
        .catch((error) => {
            console.error('Error:', error);
        });
    }

});
