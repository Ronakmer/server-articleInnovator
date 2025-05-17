

// Function to render dynamic 
function ai_rate_limiter_provider_data(response_data) {
    const tbody = document.getElementById('ai_rate_limiter_provider_tbody'); 

    tbody.innerHTML = ''; 

    const startIndex = response_data.startIndex || 0;

    response_data.provider_keys.forEach((obj, index) => {
        const tr = document.createElement('tr');
        tr.classList.add('transition-all', 'duration-500', 'hover:bg-gray-50');
        const rowIndex = startIndex + index + 1;
        
        tr.innerHTML = `
            <td class="py-3.5 pl-4 whitespace-nowrap">${rowIndex}</td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.name}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.config.model}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6 ">
                ${obj.config && obj.config.endpoint 
                    ? (obj.config.endpoint.length > 30 
                        ? obj.config.endpoint.slice(0, 30) + '...' 
                        : obj.config.endpoint) 
                    : "N/A"}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                  ${obj.config && obj.config.api_version 
                    ? (obj.config.api_version.length > 30 
                        ? obj.config.api_version.slice(0, 30) + '...' 
                        : obj.config.api_version) 
                    : "N/A"}

            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                
                    ${obj && obj.api_key 
                ? (obj.api_key.length > 30 
                    ? obj.api_key.slice(0, 30) + '...' 
                    : obj.api_key) 
                : "N/A"}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.rate_limit}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.rate_limit_period}
            </td>
        `;
        tbody.appendChild(tr);
    });
    handle_permissions();
}








// Function to render dynamic 
function ai_rate_limiter_worker_data(response_data) {
    const tbody = document.getElementById('ai_rate_limiter_worker_tbody'); 
    console.log(response_data)

    tbody.innerHTML = ''; 
    const startIndex = response_data.startIndex || 0;

    response_data.worker_data.workers.forEach((obj, index) => {
        const tr = document.createElement('tr');
        tr.classList.add('transition-all', 'duration-500', 'hover:bg-gray-50');
        const rowIndex = startIndex + index + 1;

        tr.innerHTML = `
            <td class="py-3.5 pl-4 whitespace-nowrap">${rowIndex}</td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${response_data.worker_data.workspace_id}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.pid}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.last_heartbeat}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.status}
            </td>
        `;
        tbody.appendChild(tr);
    });
    handle_permissions();
}












// Function to render dynamic 
function ai_rate_limiter_message_tbody_data(response_data) {
    const tbody = document.getElementById('ai_rate_limiter_message_tbody'); 
    const customer_count = document.getElementById('customer_count_id'); 
    customer_count.value = response_data.worker_data.rabbitmq.total_consumers;

    console.log(response_data,'0000xxx')
    tbody.innerHTML = ''; 

    // Create Total Message row
    const totalMessageRow = document.createElement('tr');
    totalMessageRow.innerHTML = `
        <th class="py-3.5 pl-4 text-left font-medium text-gray-900 whitespace-nowrap">Total Message</th>
        <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
            ${response_data.worker_data.rabbitmq.total_messages}
        </td>
    `;
    tbody.appendChild(totalMessageRow);

    // Create Per Second row
    const perSecondRow = document.createElement('tr');
    perSecondRow.innerHTML = `
        <th class="py-3.5 pl-4 text-left font-medium text-gray-900 whitespace-nowrap">Messages Ready</th>
        <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
            ${response_data.worker_data.rabbitmq.queues[0].messages_ready}
        </td>
    `;
    tbody.appendChild(perSecondRow);

    // Create Ack row
    const ackRow = document.createElement('tr');
    ackRow.innerHTML = `
        <th class="py-3.5 pl-4 text-left font-medium text-gray-900 whitespace-nowrap">Ack</th>
        <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
            ${response_data.worker_data.rabbitmq.queues[0].messages_unacknowledged}
        </td>
    `;
    tbody.appendChild(ackRow);


    handle_permissions();
}


