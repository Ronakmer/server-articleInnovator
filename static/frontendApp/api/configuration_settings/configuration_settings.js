 // Function to fetch configuration field definitions from the backend
 async function get_config_field() {
    try {
      const access_token = localStorage.getItem("access_token");

      const response = await fetch(`${get_config_field_url}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${access_token}`
        },
      });

      const responseData = await response.json();
      check_authentication_error(responseData);

      if (response.ok) {
        // Handle successful response
        create_config_field(responseData);  // Pass the response to field creation function
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

  // Function to create dynamic form fields based on the backend response
  function create_config_field(response_data) {
    // Ensure 'configDefinitions' has been populated with the backend response
    const configDefinitions = response_data;

    // Event listener for configuration type dropdown
    document.getElementById('name').addEventListener('change', function () {
      const selected = this.value;
      const fieldsContainer = document.getElementById('config-fields');
      fieldsContainer.innerHTML = '';

      // Check if there are config fields available for the selected configuration type
      if (configDefinitions[selected]) {
        configDefinitions[selected].forEach(field => {
            alert(0)
          const div = document.createElement('div');
          div.classList.add('flex', 'flex-col', 'gap-1');

          const label = document.createElement('label');
          label.innerText = field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
          label.classList.add('text-sm', 'font-medium', 'text-gray-700');

          const input = document.createElement('input');
          input.type = selected === 'retry' && field === 'count' ? 'number' : 'text';
          input.name = `config_${field}`;
          input.placeholder = field;
          input.required = true;
          input.classList.add('px-3', 'py-2', 'text-sm', 'border', 'rounded-lg', 'border-gray-300', 'focus:outline-none', 'focus:ring');

          div.appendChild(label);
          div.appendChild(input);
          fieldsContainer.appendChild(div);
        });
      }
    });
  }

//   // Call the function to fetch the configuration fields when the page is ready
//   document.addEventListener('DOMContentLoaded', async () => {
//     await  // Fetch and create form fields based on response data
//   });


get_config_field();