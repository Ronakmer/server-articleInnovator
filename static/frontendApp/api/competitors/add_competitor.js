function render_data_to_table_sitemap(response_data, current_page, limit){
    
    table_data_sitemap('sitemap_tbody', response_data, 'delete_role_api', 'status_role_api', update_role_page_url,current_page, limit)
   
}


// URL Management Variables
let urlObjects = []; // Changed from Set to Array to store objects
let urlInput, addButton, urlListContainer;
var current_step = 1;
// Initialize URL Manager
function initializeUrlManager() {
    urlInput = document.getElementById('url-input');    
    addButton = urlInput.nextElementSibling;
    urlListContainer = document.getElementById('url-list-container');

    // Initialize urlObjects array with existing URLs
    const existingUrls = Array.from(urlListContainer.querySelectorAll('.text-gray-900.break-all')).map(el => el.textContent.trim());
    existingUrls.forEach((url, index) => {
        urlObjects.push({
            url: url,
            monitor_enabled: index === 0, // First one is monitored by default
            created_by: getCurrentUserId() // You'll need to implement this function
        });
    });

    // Add event listeners
    addButton.addEventListener('click', addUrlEntry);
    urlInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            addUrlEntry();
        }
    });
}

// Function to get current user ID (implement based on your auth system)
function getCurrentUserId() {
    // Replace this with your actual user ID retrieval logic
    return 1; // Default for now
}

// Function to toggle monitor status (ensure only one is active)
function toggleMonitor(urlToToggle, checkboxElement) {
    const urlObj = urlObjects.find(obj => obj.url === urlToToggle);
    
    if (urlObj) {
        if (checkboxElement.checked) {
            // If this URL is being enabled, disable all others
            urlObjects.forEach(obj => {
                if (obj.url !== urlToToggle) {
                    obj.monitor_enabled = false;
                    // Update the checkbox in the DOM
                    const otherCheckbox = document.querySelector(`input[data-url="${obj.url}"]`);
                    if (otherCheckbox) {
                        otherCheckbox.checked = false;
                    }
                }
            });
            urlObj.monitor_enabled = true;
        } else {
            urlObj.monitor_enabled = false;
        }
    }
    
    console.log('Updated URL Objects:', urlObjects);
}

// Function to create URL entry HTML
function createUrlEntry(urlObj) {
    const uniqueId = Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    const entry = document.createElement('div');
    entry.className = 'hover:bg-gray-50 transition-colors duration-200';
    entry.setAttribute('data-url', urlObj.url);
    
    entry.innerHTML = `
        <div class="flex flex-col">
            <table class="w-full table-fixed border border-gray-200 rounded-lg overflow-hidden">
                <tr class="h-[60px]">
                    <td style="width: 120px" class="py-2 px-3 bg-gray-100">
                        <span class="text-sm font-semibold text-gray-700">Url</span>
                    </td>
                    <td style="width: 350px" class="py-2 px-3 bg-white">
                        <div style="height: 44px; scrollbar-width: none; -ms-overflow-style: none;" class="overflow-y-auto scrollbar-none [&::-webkit-scrollbar]:hidden">
                            <span class="text-sm text-gray-900 break-all">${urlObj.url}</span>
                        </div>
                    </td>
                </tr>
                <tr class="h-[60px]">
                    <td style="width: 120px" class="py-2 px-3 bg-gray-100">
                        <span class="text-sm font-semibold text-gray-700">Monitor</span>
                    </td>
                    <td style="width: 350px" class="py-2 px-3 bg-white">
                        <div class="flex justify-between items-center">
                            <div class="flipswitch">
                                <input ${urlObj.monitor_enabled ? 'checked' : ''} id="monitor_enabled_${uniqueId}" 
                                       class="flipswitch-cb" name="monitor_enabled" type="checkbox" value="1"
                                       data-url="${urlObj.url}" onchange="toggleMonitor('${urlObj.url}', this)">
                                <label for="monitor_enabled_${uniqueId}" class="flipswitch-label">
                                    <div class="flipswitch-inner" data-on="Monitor ON" data-off="Monitor OFF"></div>
                                    <div class="flipswitch-switch"></div>
                                </label>
                            </div>
                            <button onclick="removeUrlEntry('${urlObj.url}', this)" 
                                    class="text-xs text-red-600 hover:text-red-800 font-medium flex items-center">
                                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                </svg>
                                Remove
                            </button>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    `;
    return entry;
}

// Function to add URL entry
function addUrlEntry() {
    const url = urlInput.value.trim();
    
    // Validation
    if (!url) {
        alert('Please enter a URL');
        return;
    }
    
    // Check if URL already exists
    const existingUrl = urlObjects.find(obj => obj.url === url);
    if (existingUrl) {
        alert('URL already exists');
        return;
    }

    // Create new URL object
    const newUrlObj = {
        url: url,
        monitor_enabled: urlObjects.length === 0, // First URL is monitored by default
        created_by: getCurrentUserId()
    };

    // If this is being set to monitor and there are existing URLs, disable others
    if (newUrlObj.monitor_enabled && urlObjects.length > 0) {
        urlObjects.forEach(obj => {
            obj.monitor_enabled = false;
            // Update existing checkboxes
            const checkbox = document.querySelector(`input[data-url="${obj.url}"]`);
            if (checkbox) {
                checkbox.checked = false;
            }
        });
    }

    // Add URL object to array and create entry
    urlObjects.push(newUrlObj);
    const entry = createUrlEntry(newUrlObj);
    urlListContainer.appendChild(entry);
    urlInput.value = '';
    
    console.log('Added URL Object:', newUrlObj);
    console.log('All URL Objects:', urlObjects);
}

// Function to remove URL entry
function removeUrlEntry(url, buttonElement) {
    // Remove from urlObjects array
    const index = urlObjects.findIndex(obj => obj.url === url);
    if (index > -1) {
        urlObjects.splice(index, 1);
    }
    
    // Remove from DOM
    buttonElement.closest('.hover\\:bg-gray-50').remove();
    
    console.log('Removed URL:', url);
    console.log('Remaining URL Objects:', urlObjects);
}

// Function to get all URL objects for form submission
function getAllUrlObjects() {
    return urlObjects;
}

// Function to get monitored URL
function getMonitoredUrl() {
    return urlObjects.find(obj => obj.monitor_enabled);
}

// Function to show loader overlay
function showSearchLoader() {
    const tableContainer = document.querySelector('.col-span-12.lg\\:col-span-7');
    if (tableContainer) {
        // Create loader overlay if it doesn't exist
        let overlay = document.getElementById('search-loader-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'search-loader-overlay';
            overlay.style.cssText = `
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 10;
                border-radius: 1rem;
            `;
            overlay.innerHTML = `
                <div style="
                    width: 32px;
                    height: 32px;
                    border: 3px solid #e5e7eb;
                    border-top: 3px solid #6366f1;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                "></div>
                <style>
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                </style>
            `;
            
            // Make table container relative positioned
            if (tableContainer.style.position !== 'relative') {
                tableContainer.style.position = 'relative';
            }
            
            tableContainer.appendChild(overlay);
        }
        overlay.style.display = 'flex';
    }
}

// Function to hide loader overlay
function hideSearchLoader() {
    const overlay = document.getElementById('search-loader-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// Function to handle search with debounce
let searchTimeout;
function handleSearch() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        get_sitemap_api();
    }, 500); // 500ms delay
}

function collectAICheckboxesState() {
    const wrapper = document.getElementById("ai-checkbox-wrapper");
    const checkboxes = wrapper.querySelectorAll('input[type="checkbox"]');
    const result = {};

    checkboxes.forEach(checkbox => {
        // Use the checkbox name as the key, e.g., is_author_selected_by_ai
        result[checkbox.name] = checkbox.checked;
    });

    return result;
}


async function add_competitor() {
    alert(1)
    
    const competitor_domain_name = document.querySelector('[name="competitor_domain_name"]').value;
    const interval_unit = document.querySelector('[name="interval_unit"]').value;
    const interval = document.querySelector('[name="interval_value"]').value;
    const competitor_type = document.querySelector('input[name="competitor_type"]:checked')?.value;
    const domain_slug_id = document.querySelector('[name="ai_domain_slug_id"]').value;
    const prompt_slug_id = document.querySelector('[name="prompt_slug_id"]').value;
    const author_slug_id_ai = document.querySelector('[name="author_slug_id_ai"]').value || 'temp-author';
    const category_slug_id_ai = document.querySelector('[name="category_slug_id_ai"]').value;
    const tag_slug_id_ai = document.querySelector('[name="tag_slug_id_ai"]').value;
    const article_type_slug_id = document.querySelector('[name="article_type_id"]').value || 'article-type-slug-id';
    // const article_type_slug_id = "article-type-slug-id";
    const selectedRadio = document.querySelector('input[name="wp_status_ai"]:checked');
    const wp_status_ai = selectedRadio ? selectedRadio.value : null;
    const article_priority = document.querySelector('[name="article_priority"]').value;


    if(wp_status_ai == 'future'){

        const ai_date = document.querySelector("#ai_date_time_fields input[type='date']");
        const ai_time = document.querySelector("#ai_date_time_fields input[type='time']");
        
        const date_value = ai_date.value;
        const time_value = ai_time.value;
        
        if (date_value && time_value) {
            formatted_date_time = `${date_value}T${time_value}:00Z`;      
        }    
    }


    const aiCheckboxStateJson = collectAICheckboxesState();
     
    const data = new FormData();
    data.append("competitor_domain_name", competitor_domain_name);
    data.append("interval_unit", interval_unit);
    data.append("interval", interval);
    data.append("wp_status", wp_status_ai);
    data.append("selected_urls", JSON.stringify(getAllUrlObjects()));
    data.append("competitor_type", competitor_type);
    data.append("created_by", "1");
    data.append("article_priority", article_priority);

    
    data.append("article_status", "publish");
    
    if(wp_status_ai == "future"){
        data.append("wp_schedule_time", formatted_date_time);
    }
    data.append("ai_content_flags", JSON.stringify(aiCheckboxStateJson));
    data.append("domain_slug_id", domain_slug_id);
    data.append("prompt_slug_id", prompt_slug_id);
    data.append("author_slug_id_ai", author_slug_id_ai);
    data.append("category_slug_id_ai", category_slug_id_ai);
    data.append("tag_slug_id_ai", tag_slug_id_ai);
    data.append("article_type_slug_id", article_type_slug_id);


    const response = await add_api(add_competitor_url, data, null);
        
    if (response.success) {
        localStorage.setItem('competitor_domain_mapping_slug_id', response.data.domain_mapping_data.slug_id);
        if(competitor_type == "sitemap"){
            current_step = 2;
            showStep(current_step);
        }
        else if(competitor_type == "category"){
            
            current_step = 3;
            showStep(current_step);
            
        }
    }
    else{
        console.log("Competitor addition failed");
    }
}

async function get_sitemap_api() {
    
    // Show loader
    showSearchLoader();
    
    try {
        const competitor_domain_name_sitemap = document.querySelector('[name="competitor_domain_name_sitemap"]').value.trim();
        
        let current_page = 1; // Initialize current page
        const limit = 10; // Number of items per page
        const offset = (current_page - 1) * limit; // Calculate offset based on current page

        const filters = {
            competitor_domain_name: competitor_domain_name_sitemap,
        };

        const response_data = await list_api(scrap_sitemap_url, 'sitemap_tbody', offset, limit, filters, '', '', null, current_page, '', '', render_data_to_table_sitemap);
        
    } catch (error) {
        console.error('Error fetching sitemap data:', error);
    } finally {
        // Hide loader
        hideSearchLoader();
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeUrlManager();
});



//========================= userfull functions for add competitor =========================

function get_domain_data(){
    const domain_data = get_data_api(list_domain_url)    
    set_domain_dropdown(domain_data)
}
get_domain_data()


let article_type_data = '';
let set_article_type_id = '';

function get_article_type_data(){

    article_type_data = get_data_api(list_article_type_url)
    console.log(article_type_data,'000')
}
get_article_type_data()




function get_prompt_data(){
    const urlParams = new URLSearchParams(window.location.search);
    const article_type_slug_id = urlParams.get("article_type_slug_id");
    const searchParams = article_type_slug_id;

    const prompt_data = get_data_api(list_prompt_url, null, searchParams)    
    // const prompt_data = get_data_api(list_prompt_url)    
    set_prompt_dropdown(prompt_data)
}
// get_prompt_data();\


