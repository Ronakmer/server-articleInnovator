

// Function to render dynamic category count data
async function right_said_bar_category_count(domain_article_data) {

    try {
        const domain_article_data_obj = await domain_article_data; // Await the promise

        const tbody = document.getElementById('right_said_bar_category_count_id'); // Get the table body element

        // Access category article count from the response
        const categoryArticleCount = domain_article_data_obj.metrics_data.category_article_count; 

        // Clear the table body before inserting new rows
        tbody.innerHTML = '';

        // Check if category_article_count is available and is an object
        if (!categoryArticleCount || typeof categoryArticleCount !== 'object') {
            throw new Error("Invalid category_article_count data.");
        }

        // Build the rows for each category
        const rows = Object.entries(categoryArticleCount).map(([category, count]) => {
            const tr = document.createElement('tr');
            tr.classList.add('transition-all', 'duration-500', 'hover:bg-gray-50');

            // Insert category name and count into the table row
            tr.innerHTML = `
                <td class="py-3.5 pl-4">${category}</td>
                <td class="py-3.5 pl-4">${count}</td>
            `;
            return tr;
        });

        // Append all rows at once for better performance
        tbody.append(...rows);
        tbody.classList.add('overflow-y-auto', 'max-h-60'); // Adjust max height as needed


    } catch (error) {
        console.error("Error in right_said_bar_category_count:", error.message);
        
        // If there's an error, show a user-friendly message
        const tbody = document.getElementById('right_said_bar_category_count_id');
        tbody.innerHTML = `
            <tr>
                <td colspan="2" class="py-3.5 pl-4 text-center text-gray-500">
                    Failed to load category data. Please try again later.
                </td>
            </tr>
        `;
    }
}
