


// list api
async function get_article_type_field_data(api_url) {
    try {

        const access_token = localStorage.getItem("access_token");
        

        const response = await fetch(api_url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        const responseData = await response.json();

        check_authentication_error(responseData)

        if (response.ok) {
            // Handle successful response
            const data = responseData;
            console.log('00000:', data);
            const fields = data.data_field; // Extract fields from response

            generateDynamicFields(fields)

            // show_toast("success", "Roles fetched successfully");
        } else {
            const error_data = responseData;
            console.error('Failed to fetch roles:', error_data);

            const errorMessage = error_data.error || "Something went wrong";
            show_toast("error", `Error: ${errorMessage}`);
        }
    } catch (error) {
        // Handle network or other errors
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later.");
    }
}






// Function to generate dynamic fields
function generateDynamicFields(fields) {

    const container = document.querySelector('[name="dynamic_fields_container"]');

    // Clear the container before appending new fields
    container.innerHTML = "";

    const prompt_data = document.querySelector('[name="prompt_data"]');

    // create a json data (add time)
    const set_prompt_data_input = (key, value)=>{
        const json_data = JSON.parse(prompt_data.value || '{}');
        json_data[key]=value;
        prompt_data.value=JSON.stringify(json_data);
    }

    // get data from json (update time)
    const get_prompt_data_input = (key)=>{
        const json_data = JSON.parse(prompt_data.value || '{}');
        return json_data[key] || '';
    }


    fields.forEach(field => {
        const fieldWrapper = document.createElement("div");
        fieldWrapper.classList.add("field-wrapper", "mb-4");

        // Create label
        const label = document.createElement("label");
        label.setAttribute("for", field.slug_id);
        label.textContent = field.label;
        label.classList.add("mb-2",  "text-sm",  "font-medium",  "text-gray-600",  "w-full",  "flex",  "items-center");

        // Create input
        const input = document.createElement("input");
        input.setAttribute("type", field.field_type || "text");
        input.addEventListener("change", (e)=>{
            set_prompt_data_input(field.name, e.target.value);
        });
        input.value = get_prompt_data_input(field.name)
        input.setAttribute("name", field.name);
        input.setAttribute("id", field.slug_id);
        input.setAttribute("placeholder", field.placeholder);
        input.required = field.required;

        input.classList.add(
            "block",
            "w-full",
            "px-3",
            "py-1.5",
            "pr-8",
            "text-sm",
            "font-normal",
            "shadow-xs",
            "text-gray-900",
            "bg-transparent",
            "border",
            "border-gray-300",
            "rounded-lg",
            "placeholder-gray-400",
            "focus:outline-none",
            "leading-relaxed"
        );
        // Append label and input to the wrapper
        fieldWrapper.appendChild(label);
        fieldWrapper.appendChild(input);

        // Append the wrapper to the container
        container.appendChild(fieldWrapper);
    });
}
