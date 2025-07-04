

function table_data_sitemap(tbody_name, response_data, delete_function_name, status_function_name, update_page_url, current_page, limit) {
    const tbody = document.getElementById(tbody_name);
    tbody.innerHTML = '';

    const sitemap_urls = response_data.data.sitemap_urls;
    const domain = response_data.data.domain;

    sitemap_urls.forEach((url, index) => {
        const tr = document.createElement('tr');
        tr.classList.add('transition-all', 'duration-500', 'hover:bg-gray-50');

        tr.innerHTML = `
            <td class="py-3.5 pl-4 whitespace-nowrap">${index + 1}</td>
            <td class="py-3.5 pl-4 whitespace-nowrap font-normal text-gray-900 pb-6">
                ${url}
            </td>
            <td class="py-3.5 pl-4">
                <button data-copy-text="${url}"
                    class="inline-flex items-center px-2 py-1.5 text-xs font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700"
                    onclick="copyToClipboard('${url}')">
                    <svg class="w-4 h-4 " fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    handle_permissions();
}
