



// Function to render dynamic category count data
async function right_said_bar_category_count(domain_article_data) {
    try {
        const domain_article_data_obj = 
            domain_article_data instanceof Promise 
                ? await domain_article_data  // Await only if it's a promise
                : domain_article_data; 

        const tbody = document.getElementById('right_said_bar_category_count_id');
        if (!tbody) {
            throw new Error("Table body element not found.");
        }

        // Ensure `metrics_data` and `category_article_count` exist
        const categoryArticleCount = domain_article_data_obj?.metrics_data?.category_article_count ?? {};

        // Debugging: Check what `category_article_count` contains
        console.log("Category Article Count:", categoryArticleCount);

        // Check if it's a valid object
        if (typeof categoryArticleCount !== 'object' || Array.isArray(categoryArticleCount)) {
            throw new Error("Invalid category_article_count data format.");
        }

        // Clear the table body before inserting new rows
        tbody.innerHTML = '';

        // Build the rows for each category
        const rows = Object.entries(categoryArticleCount).map(([category, count]) => {
            const tr = document.createElement('tr');
            tr.classList.add('transition-all', 'duration-500', 'hover:bg-gray-50');
            tr.innerHTML = `<td class="py-3.5 pl-4">${category}</td><td class="py-3.5 pl-4">${count}</td>`;
            return tr;
        });

        // Append rows
        tbody.append(...rows);
        tbody.classList.add('overflow-y-auto', 'max-h-60');

    } catch (error) {
        console.error("Error in right_said_bar_category_count:", error.message);

        // Show a user-friendly message if there's an error
        const tbody = document.getElementById('right_said_bar_category_count_id');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="2" class="py-3.5 pl-4 text-center text-gray-500">
                        Failed to load category data. Please try again later.
                    </td>
                </tr>
            `;
        }
    }
}

