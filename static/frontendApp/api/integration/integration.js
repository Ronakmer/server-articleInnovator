//  // Function to fetch integrationuration field definitions from the backend
//  async function get_integration_field() {
//     try {
//       const access_token = localStorage.getItem("access_token");

//       const response = await fetch(`${get_integration_field_url}`, {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json',
//           'Authorization': `Bearer ${access_token}`
//         },
//       });

//       const responseData = await response.json();
//       check_authentication_error(responseData);

//       if (response.ok) {
//         // Handle successful response
//         create_integration_field(responseData);  // Pass the response to field creation function
//       } else {
//         const error_data = responseData;
//         console.error('Failed to fetch roles:', error_data);
//         const errorMessage = error_data.error || "Something went wrong";
//         show_toast("error", `Error: ${errorMessage}`);
//       }
//     } catch (error) {
//       // Handle network or other errors
//       console.error('Network error:', error);
//       show_toast("error", "Network error. Please try again later.");
//     }
//   }

//   // Function to create dynamic form fields based on the backend response
//   function create_integration_field(response_data) {
//     // Ensure 'integrationDefinitions' has been populated with the backend response
//     const integrationDefinitions = response_data;

//     // Event listener for integrationuration type dropdown
//     document.getElementById('integration_type').addEventListener('change', function () {
//       const selected = this.value;
//       const fieldsContainer = document.getElementById('integration-fields');
//       fieldsContainer.innerHTML = '';

//       // Check if there are integration fields available for the selected integrationuration type
//       if (integrationDefinitions[selected]) {
//         integrationDefinitions[selected].forEach(field => {
//           const div = document.createElement('div');
//           div.classList.add('flex', 'flex-col', 'gap-1');

//           const label = document.createElement('label');
//           label.innerText = field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
//           label.classList.add('text-sm', 'font-medium', 'text-gray-700');

//           const input = document.createElement('input');
//           input.type = selected === 'retry' && field === 'count' ? 'number' : 'text';
//           input.name = `integration_${field}`;
//           input.placeholder = field;
//           input.required = true;
//           input.classList.add('px-3', 'py-2', 'text-sm', 'border', 'rounded-lg', 'border-gray-300', 'focus:outline-none', 'focus:ring');

//           div.appendChild(label);
//           div.appendChild(input);
//           fieldsContainer.appendChild(div);
//         });
//       }
//     });
//   }

// //   // Call the function to fetch the integrationuration fields when the page is ready
// //   document.addEventListener('DOMContentLoaded', async () => {
// //     await  // Fetch and create form fields based on response data
// //   });


// get_integration_field();








// Function to fetch integration field definitions from the backend
async function getIntegrationFieldsFromBackend() {
  try {
    const access_token = localStorage.getItem("access_token");

    const response = await fetch(get_integration_field_url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${access_token}`,
      },
    });

    const data = await response.json();
    check_authentication_error(data);

    if (response.ok) {
      populateIntegrationTypesDropdown(data);     // Populate the dropdown with integration types
      setupFieldRenderListener(data);             // Setup dynamic field rendering
    } else {
      const errorMessage = data.error || "Something went wrong";
      console.error('Failed to fetch integration fields:', errorMessage);
      show_toast("error", `Error: ${errorMessage}`);
    }
  } catch (error) {
    console.error('Network error:', error);
    show_toast("error", "Network error. Please try again later.");
  }
}



// Populate dropdown options dynamically from backend data
function populateIntegrationTypesDropdown(integrationData) {
  const selectElement = document.getElementById('integration_type');
  selectElement.innerHTML = `<option value="">Select Type</option>`; // Reset dropdown

  Object.keys(integrationData).forEach(key => {
    const option = document.createElement('option');
    option.value = key;
    option.textContent = capitalizeWords(key);
    selectElement.appendChild(option);
  });
}

// Handle integration type selection and generate dynamic fields
function setupFieldRenderListener(integrationData) {
  document.getElementById('integration_type').addEventListener('change', function () {
    const selectedType = this.value;
    const fieldsContainer = document.getElementById('integration-fields');
    fieldsContainer.innerHTML = ''; // Clear existing fields

    const fields = integrationData[selectedType];
    if (fields && Array.isArray(fields)) {
      fields.forEach(field => {
        const fieldName = field.name;
        const fieldType = field.type;

        const fieldDiv = document.createElement('div');
        fieldDiv.className = 'flex flex-col gap-1';

        const label = document.createElement('label');
        label.textContent = capitalizeWords(fieldName.replace(/_/g, ' '));
        label.className = 'text-sm font-medium text-gray-700';

        let input;
        if (fieldType === 'textarea') {
          input = document.createElement('textarea');
          input.rows = 4;
        } else {
          input = document.createElement('input');
          input.type = fieldType === 'number' ? 'number' : 'text'; // add type logic if needed
        }

        input.name = `integration_${fieldName}`;
        input.placeholder = fieldName;
        input.required = true;
        input.className = 'px-3 py-2 text-sm border rounded-lg border-gray-300 focus:outline-none focus:ring';

        fieldDiv.appendChild(label);
        fieldDiv.appendChild(input);
        fieldsContainer.appendChild(fieldDiv);
      });
    }
  });
}

// Helper to capitalize words
function capitalizeWords(str) {
  return str.replace(/\b\w/g, char => char.toUpperCase());
}

// Fetch integration fields on page load
document.addEventListener('DOMContentLoaded', getIntegrationFieldsFromBackend);






