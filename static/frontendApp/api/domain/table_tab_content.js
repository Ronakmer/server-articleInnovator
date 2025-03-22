

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".active-tab").click();
});


function show_table(event, tableId, api_name) {

    // call table api 
    if (['page', 'queries', 'countries', 'date'].includes(api_name)) {
        
        const response_data =  table_tab_content_api()

        if (response_data){
            table_content(response_data, api_name)
        }
    }
    if(api_name == 'categories'){
        list_category_api()
    }
    if(api_name == 'tags'){
        list_tag_api()
    }
    if(api_name == 'authors'){
        list_author_api()
    }

    
    var i, tabContent, tabButtons;

    // Hide all tab contents
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
        tabContent[i].classList.add("hidden");
    }

    // Remove active class from all tabs
    tabButtons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("active-tab");
        tabButtons[i].classList.remove("text-indigo-600");
        tabButtons[i].classList.remove("border-b-2");
        tabButtons[i].classList.remove("border-indigo-600");

        // Reset the span text color
        var span = tabButtons[i].querySelector(".count-number");
        if (span) {
            span.style.color = "#000000"; // Reset to black or default color
        }

    }

    // Show the selected table and set the active tab
    document.getElementById(tableId).classList.remove("hidden");
    event.currentTarget.classList.add("active-tab");
    event.currentTarget.classList.add("text-indigo-600");
    event.currentTarget.classList.add("border-b-2");
    event.currentTarget.classList.add("border-indigo-600");
    

    $(".count-number").removeClass('bg-indigo-500');
    $(event.currentTarget).find(".count-number").addClass('bg-indigo-500');


    // Change the span text color of the selected tab
    var selectedSpan = event.currentTarget.querySelector(".count-number");
    if (selectedSpan) {
        selectedSpan.style.color = "#ffffff"; // Change text color to white
    }
}



// ahow table data 
async function table_content(response_data, api_name) {
    const response_data_obj = await response_data;

    const tbody = document.getElementById(`${api_name}_tbody`);

    if (!tbody) {
        console.error(`Table body with ID ${api_name}_tbody not found.`);
        return;
    }

    tbody.innerHTML = ''; // Clear previous content

    // Extract and parse data based on api_name
    const console_metrics_data = response_data_obj.console_metrics_data_obj;

    // Prepare the data based on the api_name
    let parsed_data = [];

    if (api_name === 'queries') {
        parsed_data = JSON.parse(console_metrics_data.query_result);
    } else if (api_name === 'date') {
        parsed_data = JSON.parse(console_metrics_data.date_result);
    } else if (api_name === 'page') {
        parsed_data = JSON.parse(console_metrics_data.page_result);
    } else if (api_name === 'countries') {
        parsed_data = JSON.parse(console_metrics_data.country_result);
    }

    // If no data is found, show a message
    if (parsed_data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6">No data available.</td></tr>';
        return;
    }

    // Define a function to create the table rows dynamically
    const createTableRow = (data) => {
        const tr = document.createElement('tr');
        tr.classList.add('bg-white', 'transition-all', 'duration-500', 'hover:bg-gray-50');

        // Define the table columns dynamically based on the data
        let rowHTML = '';

        if (api_name === 'queries') {
            rowHTML = `
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-gray-800">${data.query || 'N/A'}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-blue">${data.total_clicks || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-violate">${data.total_impressions || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-green">${data.avg_ctr || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-orange">${data.avg_position || 0}</td>
            `;
        } else if (api_name === 'page') {
            rowHTML = `
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-gray-800">${data.page || 'N/A'}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-blue">${data.total_clicks || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-violate">${data.total_impressions || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-green">${data.avg_ctr || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-orange">${data.avg_position || 0}</td>
            `;
        } else if (api_name === 'date') {
            rowHTML = `
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-gray-800">${data.date || 'N/A'}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-blue">${data.total_clicks || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-violate">${data.total_impressions || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-green">${data.avg_ctr || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-orange">${data.avg_position || 0}</td>
            `;
        } else if (api_name === 'countries') {
            rowHTML = `
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-gray-800">${data.country || 'N/A'}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-blue">${data.total_clicks || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-violate">${data.total_impressions || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-green">${data.avg_ctr || 0}</td>
                <td class="py-3.5 pl-4 whitespace-nowrap text-xs font-normal text-custom-orange">${data.avg_position || 0}</td>
            `;
        }

        tr.innerHTML = rowHTML;
        return tr;
    };

    // Loop through the data and append rows to the table
    parsed_data.forEach((data) => {
        const tr = createTableRow(data);
        tbody.appendChild(tr);
    });
}
