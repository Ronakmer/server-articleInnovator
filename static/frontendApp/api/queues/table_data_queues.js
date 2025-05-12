






// Function to render dynamic 
function table_data_queues(tbody_name, response_data, delete_function_name, status_function_name, update_page_url, current_page, limit) {

    const tbody = document.getElementById(tbody_name); 

    tbody.innerHTML = ''; 
    console.log(response_data,'response_data')
    response_data.data.forEach((obj, index) => {
        const tr = document.createElement('tr');
        
        const queueState = obj.data.queues?.[0]?.state;
        if (queueState === undefined) {
            const add_queue_btn = document.getElementById('add_queue_btn'); 

            add_queue_btn.classList.remove("hidden");

        }
        
        tr.classList.add('transition-all', 'duration-500', 'hover:bg-gray-50');
        tr.innerHTML = `
            
            <td class="py-3.5 pl-4 whitespace-nowrap">${index + 1 + (current_page - 1) * limit}</td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.queue_name}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.data.queues?.[0]?.state ?? 'N/A'}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.data.queues?.[0]?.messages ?? 0}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.data.queues?.[0]?.messages_ready ?? 0}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                <div class="flex items-center gap-2" data-permission="update_worker_scale">
                    <div class="flex mb-3 rounded-lg overflow-hidden border border-gray-300 w-full max-w-md">
                        <input type="text" aria-label="Recipient's username"class="flex-1 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" id="worker_scale_id" value="${obj.data.queues?.[0]?.worker_count ?? 0}" >
                        <button type="button" onclick="update_worker_scale('${obj.queue_name}')" id="button-addon2" class="px-4 py-2 bg-gray-200 text-gray-700 hover:bg-gray-300 border-l border-gray-300">
                        scale
                        </button>
                    </div>
                </div>
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.data.queues?.[0]?.message_stats?.ack ?? 0}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${obj.data.queues?.[0]?.message_stats?.deliver ?? 0}
            </td>
            ${obj.data.queues?.[0]?.state === undefined ? `
                <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6" data-permission="add_queue_api">
                    <button type="button" onclick="add_queue_api('${obj.queue_name}')" class="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600">
                        Add
                    </button>
                </td>` : `
                <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                </td>
            `}
                

        `;
        tbody.appendChild(tr);
    });
handle_permissions();

}



