
let start_date = '2024-11-25';  // Replace with dynamic date if needed
let end_date = '2025-01-25';    // Replace with dynamic date if needed

// let start_date = '';  // Replace with dynamic date if needed
// let end_date = '';    // Replace with dynamic date if needed


// // Function to calculate last 7 days
// function getLast7Days() {
//     const today = new Date();
//     const last7Days = new Date(today);
//     last7Days.setDate(today.getDate() - 7);
    
//     const formattedStartDate = last7Days.toISOString().split('T')[0]; // Format as YYYY-MM-DD
//     const formattedEndDate = today.toISOString().split('T')[0]; // Format as YYYY-MM-DD
    
//     return { start: formattedStartDate, end: formattedEndDate };
// }


// if (!start_date && !end_date) {
//     const last7Days = getLast7Days();
//     start_date = last7Days.start;
//     end_date = last7Days.end;
// }


// function filter_by_date() {
//     let temp_start_date = document.querySelector('[name="start_date"]').value;
//     let temp_end_date = document.querySelector('[name="end_date"]').value;
    
//     // If the user has selected dates, use them, otherwise, keep the default
//     start_date = temp_start_date || start_date;
//     end_date = temp_end_date || end_date;
    
//     // Optional: You can log the selected or default dates for debugging
//     console.log("Start Date: ", start_date);
//     console.log("End Date: ", end_date);
// }

// alert(start_date)
// alert(end_date)




let current_page_url = window.location.href;
const slug_id = current_page_url.split('/').pop();


let domain_console_data = domain_console_graph_api(domain_console_metrics_url, slug_id, start_date, end_date);
let domain_analytics_data = domain_analytics_graph_api(domain_analytics_metrics_url, slug_id, start_date, end_date);
let domain_article_data = domain_article_graph_api(domain_article_metrics_url, slug_id, start_date, end_date);



detail_domain_chart(domain_console_data, domain_analytics_data, domain_article_data, slug_id)

right_said_bar_category_count(domain_article_data)



