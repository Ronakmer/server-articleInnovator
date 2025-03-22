




// Function to render dynamic 
function table_data_activity_log(tbody_name, response_data, current_page, limit) {

    const tbody = document.getElementById(tbody_name); 

    tbody.innerHTML = ''; 

    response_data.data.forEach((obj, index) => {
        const tr = document.createElement('tr');
        tr.classList.add('transition-all', 'duration-500', 'hover:bg-gray-50');

        tr.innerHTML = `
            <td class="py-3.5 pl-4 whitespace-nowrap">${index + 1 + (current_page - 1) * limit}</td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.message}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.level}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${formatDate(obj.time)}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.user_role}
            </td>
        `;
        tbody.appendChild(tr);
    });
}




function formatDate(isoString) {
    return new Date(isoString).toLocaleString();
}