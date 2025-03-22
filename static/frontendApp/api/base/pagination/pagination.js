


// Function to create pagination UI using the provided Tailwind CSS structure
function render_pagination( total_count, limit, current_page, api_url, table_name, filters, delete_function_name, status_function_name, update_page_url, response_key, render_data_to_table=()=>{}, domain_slug_id) {
    const pagination_container = document.getElementById('pagination');
    pagination_container.innerHTML = ''; // Clear previous buttons

    const total_pages = Math.ceil(total_count / limit);

    // Pagination container
    const container = document.createElement('div');
    container.className = 'flex w-full items-center justify-between bg-white py-4';

    // Left-aligned text for showing results
    const results_info = document.createElement('div');
    results_info.className = 'flex-1';
    results_info.innerHTML = `
    <p class="text-sm text-gray-700">
        Showing
        <span class="font-medium">${(current_page - 1) * limit + 1}</span>
        to
        <span class="font-medium">${Math.min(current_page * limit, total_count)}</span>
        of
        <span class="font-medium">${total_count}</span>
        results
    </p>
    `;
    container.appendChild(results_info);

    // Pagination controls
    const pagination_controls = document.createElement('div');
    pagination_controls.className = 'hidden sm:flex sm:flex-1 sm:items-center sm:justify-end';

    const nav = document.createElement('nav');
    nav.className = 'isolate inline-flex space-x-1 rounded-md';
    nav.setAttribute('aria-label', 'Pagination');

    // Previous button
    if (current_page > 1) {
        const prev_button = document.createElement('button');
        // prev_button.href = '#';
        prev_button.className = 'relative inline-flex items-center rounded-lg px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0';
        prev_button.innerHTML = `
        <span class="sr-only">Previous</span>
        <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clip-rule="evenodd"></path>
        </svg>
        `;
        prev_button.addEventListener('click', async () => {
            await list_api(
                api_url,
                table_name,
                (current_page - 2) * limit,
                limit,
                filters,
                delete_function_name,
                status_function_name,
                update_page_url,
                current_page - 1,
                response_key,
                domain_slug_id,
                render_data_to_table
            );
        });
        nav.appendChild(prev_button);
    }

    // Page buttons with ellipsis
    for (let page = 1; page <= total_pages; page++) {
        if (
            page <= 2 ||
            page > total_pages - 2 ||
            page === current_page ||
            page === current_page - 1 ||
            page === current_page + 1
        ) {
            const page_button = document.createElement('button');
            // page_button.href = '#';
            page_button.textContent = page;
            page_button.className = `relative inline-flex items-center rounded-lg px-4 py-2 text-sm font-semibold ${
                page === current_page
                    ? 'bg-indigo-600 text-white'
                    : 'text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50'
            } focus:z-20 focus:outline-offset-0`;

            page_button.addEventListener('click', async () => {
                await list_api(
                    api_url,
                    table_name,
                    (page - 1) * limit,
                    limit,
                    filters,
                    delete_function_name,
                    status_function_name,
                    update_page_url,
                    page,
                    response_key,
                    domain_slug_id,
                    render_data_to_table
                );
            });
            nav.appendChild(page_button);
        } else if (page === 3 && current_page > 4) {
            const ellipsis = document.createElement('span');
            ellipsis.className =
                'relative inline-flex items-center rounded-lg px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-inset ring-gray-300 focus:outline-offset-0';
            ellipsis.textContent = '...';
            nav.appendChild(ellipsis);
        } else if (page === total_pages - 2 && current_page < total_pages - 3) {
            const ellipsis = document.createElement('span');
            ellipsis.className =
                'relative inline-flex items-center rounded-lg px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-inset ring-gray-300 focus:outline-offset-0';
            ellipsis.textContent = '...';
            nav.appendChild(ellipsis);
        }
    }

    // Next button
    if (current_page < total_pages) {
        const next_button = document.createElement('button');
        // next_button.href = '#';
        next_button.className = 'relative inline-flex items-center rounded-lg px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0';
        next_button.innerHTML = `
            <span class="sr-only">Next</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clip-rule="evenodd"></path>
            </svg>
        `;
        next_button.addEventListener('click', async () => {
            await list_api(
                api_url,
                table_name,
                current_page * limit,
                limit,
                filters,
                delete_function_name,
                status_function_name,
                update_page_url,
                current_page + 1,
                response_key,
                domain_slug_id,
                render_data_to_table
            );
        });
        nav.appendChild(next_button);
    }

    pagination_controls.appendChild(nav);
    container.appendChild(pagination_controls);

    pagination_container.appendChild(container);
}
  