// Global array to store selected URLs
let selectedArticleUrls = [];

function table_data_article_urls(tbody_name, response_data, delete_function_name, status_function_name, update_page_url, current_page, limit) {
    const tbody = document.getElementById(tbody_name);
    tbody.innerHTML = '';

    const found_articles = response_data.found_articles || [];

    found_articles.forEach((article, index) => {
        const url = article.url;
        const foundAt = article.found_at || '-';
        const competitorSelectedUrlSlugId = article.competitor_selected_url_slug_id || '';
        const checkboxId = `article_checkbox_${index}`;

        const tr = document.createElement('tr');
        tr.classList.add('transition-all', 'duration-500', 'hover:bg-gray-50');

        tr.innerHTML = `
            <td class="py-3.5 pl-4 whitespace-nowrap">
                <input type="checkbox" id="${checkboxId}" class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500" 
                       onchange="handleArticleCheckboxChange('${url}', '${competitorSelectedUrlSlugId}', this.checked)">
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap">${index + 1}</td>
            <td class="py-3.5 pl-4 whitespace-nowrap text-gray-900 text-sm">
                ${url}
            </td>
            <td class="py-3.5 pl-4 whitespace-nowrap text-gray-700 text-sm">
                ${foundAt}
            </td>
            
        `;

        tbody.appendChild(tr);
    });

    handle_permissions();
}

// Function to handle select all checkbox
function handleSelectAll(isChecked) {
    // Get all article checkboxes
    const articleCheckboxes = document.querySelectorAll('input[type="checkbox"][id^="article_checkbox_"]');
    
    if (isChecked) {
        // Select all - check all checkboxes and add URLs to selected array
        articleCheckboxes.forEach(checkbox => {
            checkbox.checked = true;
            // Extract URL and slug_id from the checkbox's onchange attribute
            const onchangeAttr = checkbox.getAttribute('onchange');
            const urlMatch = onchangeAttr.match(/handleArticleCheckboxChange\('([^']+)', '([^']*)', this\.checked\)/);
            if (urlMatch) {
                const url = urlMatch[1];
                const competitorSelectedUrlSlugId = urlMatch[2];
                const articleObj = {
                    url: url,
                    competitor_selected_url_slug_id: competitorSelectedUrlSlugId
                };
                // Check if this URL is not already in the array
                if (!selectedArticleUrls.some(item => item.url === url)) {
                    selectedArticleUrls.push(articleObj);
                }
            }
        });
    } else {
        // Deselect all - uncheck all checkboxes and clear selected array
        articleCheckboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
        selectedArticleUrls = [];
    }
    
    console.log('Select All - Selected URLs:', selectedArticleUrls);
}

// Function to handle checkbox changes
function handleArticleCheckboxChange(url, competitorSelectedUrlSlugId, isChecked) {
    if (isChecked) {
        // Add article object to selected array if not already present
        const articleObj = {
            url: url,
            competitor_selected_url_slug_id: competitorSelectedUrlSlugId
        };
        if (!selectedArticleUrls.some(item => item.url === url)) {
            selectedArticleUrls.push(articleObj);
        }
    } else {
        // Remove article object from selected array
        const index = selectedArticleUrls.findIndex(item => item.url === url);
        if (index > -1) {
            selectedArticleUrls.splice(index, 1);
        }
        
        // Uncheck the select all checkbox if this item is unchecked
        const selectAllCheckbox = document.getElementById('select-all-checkbox');
        if (selectAllCheckbox) {
            selectAllCheckbox.checked = false;
        }
    }
    
    // Check if all checkboxes are selected to update select all checkbox
    const articleCheckboxes = document.querySelectorAll('input[type="checkbox"][id^="article_checkbox_"]');
    const checkedCheckboxes = document.querySelectorAll('input[type="checkbox"][id^="article_checkbox_"]:checked');
    const selectAllCheckbox = document.getElementById('select-all-checkbox');
    
    if (selectAllCheckbox && articleCheckboxes.length > 0) {
        selectAllCheckbox.checked = articleCheckboxes.length === checkedCheckboxes.length;
    }
    
    console.log('Selected URLs:', selectedArticleUrls);
}

// Function to get selected URLs
function getSelectedArticleUrls() {
    return selectedArticleUrls;
}

// Function to clear selected URLs
function clearSelectedArticleUrls() {
    selectedArticleUrls = [];
    // Uncheck all checkboxes including select all
    const allCheckboxes = document.querySelectorAll('input[type="checkbox"][id^="article_checkbox_"], #select-all-checkbox');
    allCheckboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
}
