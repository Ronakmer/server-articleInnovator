



// Define date variables
let start_date = '';
let end_date = '';

// Function to calculate last 7 days
function getLast7Days() {
    const today = new Date();
    const last7Days = new Date(today);
    last7Days.setDate(today.getDate() - 7);
    
    return {
        start: last7Days.toISOString().split('T')[0], // Format as YYYY-MM-DD
        end: today.toISOString().split('T')[0] // Format as YYYY-MM-DD
    };
}

// Initialize dates with last 7 days if not provided
function initializeDates() {
    if (!start_date && !end_date) {
        const last7Days = getLast7Days();
        start_date = last7Days.start;
        end_date = last7Days.end;
        
        // Update date inputs if they exist in the DOM
        const startDateInput = document.querySelector('[name="start_date"]');
        const endDateInput = document.querySelector('[name="end_date"]');
        
        if (startDateInput) startDateInput.value = start_date;
        if (endDateInput) endDateInput.value = end_date;
    }
}

// Function to handle date filter changes
function filter_by_date() {
    const startDateInput = document.querySelector('[name="start_date"]');
    const endDateInput = document.querySelector('[name="end_date"]');
    
    if (startDateInput && endDateInput) {
        // Only update if values are not empty
        if (startDateInput.value) start_date = startDateInput.value;
        if (endDateInput.value) end_date = endDateInput.value;
        
        // Load data with updated dates
        loadDomainData();
    }
}

// Get the slug ID from the URL
function getSlugId() {
    const current_page_url = window.location.href;
    return current_page_url.split('/').pop();
}

// Load all domain data
function loadDomainData() {
    try {
        const slug_id = getSlugId();
        
        // Log the selected dates for debugging
        console.log("Loading data for period:", start_date, "to", end_date);
        
        // Fetch all data with proper error handling
        let domain_console_data = domain_console_graph_api(domain_console_metrics_url, slug_id, start_date, end_date);
        let domain_analytics_data = domain_analytics_graph_api(domain_analytics_metrics_url, slug_id, start_date, end_date);
        let domain_article_data = domain_article_graph_api(domain_article_metrics_url, slug_id, start_date, end_date);
        
        // Render charts and visualizations
        detail_domain_chart(domain_console_data, domain_analytics_data, domain_article_data, slug_id);
        right_said_bar_category_count(domain_article_data);
    } catch (error) {
        console.error("Error loading domain data:", error);
        // Display user-friendly error message if needed
    }
}

// Initialize the application
function initApp() {
    initializeDates();
    loadDomainData();
    
    // Add event listeners
    const startDateInput = document.querySelector('[name="start_date"]');
    const endDateInput = document.querySelector('[name="end_date"]');
    const filterButton = document.querySelector('#filter_button'); // Assuming there's a filter button
    
    if (filterButton) {
        filterButton.addEventListener('click', filter_by_date);
    } else {
        // If no button exists, add change listeners to date inputs
        if (startDateInput) startDateInput.addEventListener('change', filter_by_date);
        if (endDateInput) endDateInput.addEventListener('change', filter_by_date);
    }
}

// Run the app when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initApp);























