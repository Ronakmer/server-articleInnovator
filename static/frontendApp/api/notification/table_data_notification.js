




// Function to render dynamic 
function table_data_notification(tbody_name, response_data, current_page, limit, delete_function_name) {

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
                ${formatDate(obj.time)}
            </td>
            <td class="py-3.5 px-4 hidden" data-permission="delete_notification" >
                <div class="flex font-poppins">
                    <!-- delete -->
                    <a href="#" class="mr-2 hidden" data-permission="delete_notification"  onclick="${delete_function_name}('${obj.slug_id}')">
                        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"
                            xmlns="http://www.w3.org/2000/svg">
                            <rect width="32" height="32" rx="16" fill="#EAECF0"></rect>
                            <path
                                d="M22 12.4867C21.9867 12.4867 21.9667 12.4867 21.9467 12.4867C18.42 12.1333 14.9 12 11.4133 12.3533L10.0533 12.4867C9.77334 12.5133 9.52667 12.3133 9.5 12.0333C9.47334 11.7533 9.67334 11.5133 9.94667 11.4867L11.3067 11.3533C14.8533 10.9933 18.4467 11.1333 22.0467 11.4867C22.32 11.5133 22.52 11.76 22.4933 12.0333C22.4733 12.2933 22.2533 12.4867 22 12.4867Z"
                                fill="#E64646"></path>
                            <path
                                d="M13.6667 11.8133C13.64 11.8133 13.6133 11.8133 13.58 11.8067C13.3133 11.76 13.1267 11.5 13.1733 11.2333L13.32 10.36C13.4267 9.72 13.5733 8.83333 15.1267 8.83333H16.8733C18.4333 8.83333 18.58 9.75333 18.68 10.3667L18.8267 11.2333C18.8733 11.5067 18.6867 11.7667 18.42 11.8067C18.1467 11.8533 17.8867 11.6667 17.8467 11.4L17.7 10.5333C17.6067 9.95333 17.5867 9.84 16.88 9.84H15.1333C14.4267 9.84 14.4133 9.93333 14.3133 10.5267L14.16 11.3933C14.12 11.64 13.9067 11.8133 13.6667 11.8133Z"
                                fill="#E64646"></path>
                            <path
                                d="M18.14 23.1667H13.86C11.5333 23.1667 11.44 21.88 11.3667 20.84L10.9333 14.1267C10.9133 13.8533 11.1267 13.6133 11.4 13.5933C11.68 13.58 11.9133 13.7867 11.9333 14.06L12.3667 20.7733C12.44 21.7867 12.4667 22.1667 13.86 22.1667H18.14C19.54 22.1667 19.5667 21.7867 19.6333 20.7733L20.0667 14.06C20.0867 13.7867 20.3267 13.58 20.6 13.5933C20.8733 13.6133 21.0867 13.8467 21.0667 14.1267L20.6333 20.84C20.56 21.88 20.4667 23.1667 18.14 23.1667Z"
                                fill="#E64646"></path>
                            <path
                                d="M17.1067 19.5H14.8867C14.6133 19.5 14.3867 19.2733 14.3867 19C14.3867 18.7267 14.6133 18.5 14.8867 18.5H17.1067C17.38 18.5 17.6067 18.7267 17.6067 19C17.6067 19.2733 17.38 19.5 17.1067 19.5Z"
                                fill="#E64646"></path>
                            <path
                                d="M17.6667 16.8333H14.3333C14.06 16.8333 13.8333 16.6067 13.8333 16.3333C13.8333 16.06 14.06 15.8333 14.3333 15.8333H17.6667C17.94 15.8333 18.1667 16.06 18.1667 16.3333C18.1667 16.6067 17.94 16.8333 17.6667 16.8333Z"
                                fill="#E64646"></path>
                        </svg>
                    </a>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
handle_permissions();

}




function formatDate(isoString) {
    return new Date(isoString).toLocaleString();
}