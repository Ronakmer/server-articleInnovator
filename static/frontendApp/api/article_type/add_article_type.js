
let article_type_field_data = '';
let color_detail_data = '';
let set_color_slug_id = '';
let set_article_type_field_slug_id = '';



function filter_article_type_form() {
    const selectedValue = document.getElementById("type").value;

    const articleTypeField = document.getElementById("article_type_field");
    const rabbitmqWorker = document.getElementById("rabbitmq_worker");
    const supportiveVariables = document.getElementById("supportive_variables");
    const categorySection = document.getElementById("category_section");

    const shouldHide = selectedValue === "manual";

    // Toggle visibility
    articleTypeField.style.display = shouldHide ? 'none' : 'block';
    rabbitmqWorker.style.display = shouldHide ? 'none' : 'block';
    supportiveVariables.style.display = shouldHide ? 'none' : 'block';
    categorySection.style.display = shouldHide ? 'none' : 'block';
}


function add_article_type_api() {

    // Get the form element
    const article_type_form = document.querySelector('[name="article_type_form"]');

    // Collect form data using the name attributes
    const article_category = article_type_form.querySelector('[name="article_category"]').value;
    const category = article_type_form.querySelector('[name="category"]').value;
    const article_type_field_slug_id = article_type_form.querySelector('[name="article_type_field"]').value;
    const color_detail_slug_id = article_type_form.querySelector('[name="color"]').value;
    const title = article_type_form.querySelector('[name="title"]').value;
    const description = article_type_form.querySelector('[name="description"]').value;
    const rabbitmq_worker = article_type_form.querySelector('[name="rabbitmq_worker"]').value;
    const article_type_image = article_type_form.querySelector('[name="article_type_image"]');

    const supportive_variables_data = create_variables_json()

    const data = new FormData();
    // If the category is 'manual', append only necessary data
    if(article_category === 'manual'){
        alert(0);  // For debugging purposes, you can remove this after testing
        data.append("article_category", article_category);
        data.append("color_detail_slug_id", color_detail_slug_id);
        data.append("description", description);
        data.append("title", title);
    } else {
        // If not 'manual', append all data
        data.append("article_category", article_category);
        data.append("category", category);
        data.append("article_type_field_slug_id", article_type_field_slug_id);
        data.append("color_detail_slug_id", color_detail_slug_id);
        data.append("title", title);
        data.append("description", description);
        data.append("rabbitmq_worker", rabbitmq_worker);
        data.append("supportive_variables_data", supportive_variables_data);
    }

    if (article_type_image && article_type_image.files && article_type_image.files[0]) {
        data.append('article_type_image', article_type_image.files[0]);
    }



    const current_url = window.location.pathname;
    const is_update_page = current_url.includes('/update/');

    (async ()=>{ 
        if (is_update_page) {
            const slug_id = current_url.split('/update/')[1].split('/')[0];
            console.log("Found ID:", slug_id);
            await update_api(update_article_type_url, data, slug_id, list_article_type_page_url);
        } else {
            await add_api(add_article_type_url, data, list_article_type_page_url);
        }
    })()

}



(async ()=>{      
    const current_url = window.location.pathname;
    if (current_url.includes('/update/')) {
        
        const slug_id = current_url.split('/update/')[1].split('/')[0];
        console.log("Found ID:", slug_id); 
        
        const temp_api_url = `${list_article_type_url}?slug_id=${slug_id}`;
        var data_obj = await set_data_api(temp_api_url, slug_id);

        const temp_variables_api_url = `${list_variables_url}?article_type_slug_id=${slug_id}`;
        var variables_data_obj = await set_data_api(temp_variables_api_url, '');
        console.log(variables_data_obj,'variables_data_obj')



        // Get the form element
        const article_type_form = document.querySelector('[name="article_type_form"]');

        // Collect form data using the name attributes
        const article_category = article_type_form.querySelector('[name="article_category"]');
        const category = article_type_form.querySelector('[name="category"]');
        const article_type_field_slug_id = article_type_form.querySelector('[name="article_type_field"]');
        const color_slug_id = article_type_form.querySelector('[name="color"]');
        const title = article_type_form.querySelector('[name="title"]');
        const description = article_type_form.querySelector('[name="description"]');
        const rabbitmq_worker = article_type_form.querySelector('[name="rabbitmq_worker"]');
        const article_type_image = article_type_form.querySelector('[name="article_type_image"]');
    
        
        if (data_obj && data_obj.data && data_obj.data.length > 0) {
            article_category.value = data_obj.data[0].article_category;
            category.value = data_obj.data[0].category;
            title.value  = data_obj.data[0].title;
            description.value  = data_obj.data[0].description;            
            rabbitmq_worker.value  = data_obj.data[0].rabbitmq_worker;            
            set_color_slug_id = data_obj.data[0].color_detail_id_data.slug_id
            set_article_type_field_slug_id = data_obj.data[0].article_type_field_id_data.map(field => field.slug_id).join(', ')
            
            await populateSupportiveVariables(variables_data_obj);
            filter_article_type_form();

        } else {
            // name.value = ''; 
            window.location.href = error_page;
        }
        
    }
})()
     

function get_article_type_field_data(){

    article_type_field_data = get_data_api(list_article_type_field_url)
}
get_article_type_field_data()



function get_color_detail_data(){
    
    color_detail_data = get_data_api(list_color_detail_url)
}
get_color_detail_data()














// ######################### varibal ######################### 

// Function to create a new name-value group
function addNameValueGroup() {
    const container = document.getElementById('name-value-wrapper');
    const groups = container.querySelectorAll('.name-value-group');
    const newIndex = groups.length;
    
    // Clone the first group
    const newGroup = groups[0].cloneNode(true);
    
    // Clear input values
    newGroup.querySelector('input[name="name[]"]').value = '';
    newGroup.querySelector('textarea[name="value[]"]').value = '';
    newGroup.querySelector('input[name="required[]"]').checked = false;
    
    // Add data-index attribute
    newGroup.setAttribute('data-index', newIndex);
    
    // Show remove button for added groups
    const removeBtn = newGroup.querySelector('.remove-name-value-btn');
    if (removeBtn) {
        removeBtn.classList.remove('hidden');
    }
    
    // Add the new group to the container
    container.appendChild(newGroup);
    
    // Add event listener to remove button
    if (removeBtn) {
        removeBtn.addEventListener('click', function() {
            container.removeChild(newGroup);
            // Reindex remaining groups
            updateGroupIndices();
        });
    }
    
    return newGroup;
}

// Function to update data-index attributes after removal
function updateGroupIndices() {
    const container = document.getElementById('name-value-wrapper');
    const groups = container.querySelectorAll('.name-value-group');
    groups.forEach((group, index) => {
        group.setAttribute('data-index', index);
    });
}

// Function to create JSON from form fields
function create_variables_json() {
    const nameValueGroups = document.querySelectorAll('.name-value-group');
    const variables = [];

    nameValueGroups.forEach(group => {
        const nameInput = group.querySelector('input[name="name[]"]');
        const valueInput = group.querySelector('textarea[name="value[]"]');
        const requiredCheckbox = group.querySelector('input[name="required[]"]');
        const slugIdInput = group.querySelector('input[name="variables_slug_id[]"]');  // Get hidden slug_id

        const nameVal = nameInput.value.trim();
        const valueVal = valueInput.value.trim();
        const requiredVal = requiredCheckbox?.checked || false;
        const slugIdVal = slugIdInput ? slugIdInput.value.trim() : '';


        // if (nameVal && valueVal) {
        //     variables.push({
        //         name: nameVal,
        //         value: valueVal,
        //         required: requiredVal
        //     });
        // }
        if (nameVal && valueVal) {
            const entry = {
                name: nameVal,
                value: valueVal,
                required: requiredVal
            };
            if (slugIdVal) {
                entry.slug_id = slugIdVal;
            }
            variables.push(entry);
        }
    });

    console.log(variables);
    return JSON.stringify(variables);
}

// Function to populate supportive variables from API data
async function populateSupportiveVariables(variables_data_obj) {
    if (!variables_data_obj || !variables_data_obj.data || 
        !Array.isArray(variables_data_obj.data) || 
        variables_data_obj.data.length === 0) {
        console.log("No supportive variables data to populate");
        return;
    }
    
    console.log("Populating supportive variables:", variables_data_obj.data);
    
    const container = document.getElementById('name-value-wrapper');
    
    // Make sure we have the first group as template
    let firstGroup = container.querySelector('.name-value-group');
    if (!firstGroup) {
        console.error("Cannot find name-value-group template");
        return;
    }
    
    // Clear existing groups except the first one (template)
    const existingGroups = container.querySelectorAll('.name-value-group');
    for (let i = 1; i < existingGroups.length; i++) {
        container.removeChild(existingGroups[i]);
    }
    
    // Reset the first group
    firstGroup.setAttribute('data-index', '0');
    
    // Populate first group if we have data
    if (variables_data_obj.data.length > 0) {
        const firstVar = variables_data_obj.data[0];
        const nameInput = firstGroup.querySelector('input[name="name[]"]');
        const valueInput = firstGroup.querySelector('textarea[name="value[]"]');
        const requiredCheckbox = firstGroup.querySelector('input[name="required[]"]');
        const slugIdInput = firstGroup.querySelector('input[name="variables_slug_id[]"]'); // ✅ added here

        nameInput.value = firstVar.name || '';
        valueInput.value = firstVar.value || '';
        requiredCheckbox.checked = firstVar.required || false;
        // alert(firstVar.slug_id)
        if (slugIdInput) {
            slugIdInput.value = firstVar.slug_id || '';
        }

    }
    
    // Create and populate additional groups for remaining data, but manually instead of using the button
    for (let i = 1; i < variables_data_obj.data.length; i++) {
        const newGroup = addNameValueGroup();
        
        if (newGroup) {
            const supportiveVar = variables_data_obj.data[i];
            const nameInput = newGroup.querySelector('input[name="name[]"]');
            const valueInput = newGroup.querySelector('textarea[name="value[]"]');
            const requiredCheckbox = newGroup.querySelector('input[name="required[]"]');
            
            const slugIdInput = newGroup.querySelector('input[name="variables_slug_id[]"]'); // ✅ added here
            if (slugIdInput) {
                slugIdInput.value = supportiveVar.slug_id || '';
            }


            nameInput.value = supportiveVar.name || '';
            valueInput.value = supportiveVar.value || '';
            requiredCheckbox.checked = supportiveVar.required || false;
        }
    }
    
    console.log("Finished populating supportive variables");
}

// Initialize add button event listener
// document.addEventListener('DOMContentLoaded', function() {
//     const addButton = document.getElementById('add-name-value-btn');
//     if (addButton) {
//         addButton.addEventListener('click', addNameValueGroup);
//     }
// });