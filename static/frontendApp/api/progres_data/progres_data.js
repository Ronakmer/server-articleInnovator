


let totalProgress = 0;
let logCounter = 1;

function update_progress_ui(logMessage, progressIncrement = 0) {
    // Input validation
    if (!logMessage) return;
    
    // Update progress
    totalProgress = Math.min(totalProgress + progressIncrement, 100);
    
    // Update progress bar
    const progressBar = document.getElementById('progressbar_id');
    const progressText = document.getElementById('progressbar_percentage');
    progressBar.style.width = `${totalProgress}%`;
    progressBar.setAttribute('aria-valuenow', totalProgress);
    progressText.textContent = `${Math.round(totalProgress)}%`;

    // Create and add log entry
    const logContainer = document.getElementById('log-container');

    const logItem = document.createElement('li');
    logItem.classList.add('flex', 'items-center', 'gap-2', 'text-pink-400');
    logItem.innerHTML = `
        <span class="inline-block min-w-[20px] text-right">${logCounter++}.</span>
        <span class="flex-1">${logMessage}</span>
    `;
    logContainer.appendChild(logItem);
    logContainer.scrollTop = logContainer.scrollHeight;
}



let log_percentage = null;
let log_text = null;

// Extract domain_slug_id from URL
const temp_url = new URLSearchParams(window.location.search);
const domain_slug_id = temp_url.get('domain_slug_id');

async function progres_data_api(domain_slug_id) {
    try {
        const access_token = localStorage.getItem("access_token");

        const query_params = new URLSearchParams();
        if (domain_slug_id) {
            query_params.append("domain_slug_id", domain_slug_id);
        }

        const response = await fetch(`${progres_data}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });
        const responseData = await response.json();

        check_authentication_error(responseData)


        if (!response.ok) {
            const error_data = responseData;
            console.error('Failed to fetch progress data:', error_data);
            show_toast("error", `Error: ${error_data.error || "Something went wrong"}`);
            return;
        }

        const data = responseData;
        console.log('Progress Data:', data);

        log_text = data.progress_data?.log_text ?? null;
        log_percentage = data.progress_data?.log_percentage ?? null;

        // if (!log_text) return;
        update_progress_ui(log_text, log_percentage);


    } catch (error) {
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later.");
    }
}

// Initial API call and set interval
if (domain_slug_id) {
    progres_data_api(domain_slug_id);

    // Fetch progress data every 5 seconds
    let intervalId = setInterval(async () => {
        let prev_log_text = log_text; // Store the last log text
        await progres_data_api(domain_slug_id);

        // Stop interval if no new log text
        if (log_text === prev_log_text || log_text === null) {
            console.log('Stopping interval: No new logs found.');
            clearInterval(intervalId);
            // alert("Done");
            show_toast("success", `All Data are Fetch`);
            setTimeout(() => {
                window.location.href = list_domain_page_url;
            }, 2000);

        }
    }, 2000); // Runs every 5 seconds
}
