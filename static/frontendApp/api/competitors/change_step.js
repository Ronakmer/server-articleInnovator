
function showStep(stepNumber) {

    
    // Reset all step circles
    for (let i = 0; i <= 6; i++) {
        const circle = document.getElementById(`step${i}-circle`);
        if (circle) {
            if (i <= stepNumber) {
                circle.classList.add('bg-indigo-600', 'text-white');
                circle.classList.remove('bg-gray-200', 'text-gray-500');
            } else {
                circle.classList.add('bg-gray-200', 'text-gray-500');
                circle.classList.remove('bg-indigo-600', 'text-white');
            }
        }
    }

    // Reset all step lines
    for (let i = 1; i <= 5; i++) {
        const line = document.getElementById(`line${i}`);
        if (line) {
            if (i < stepNumber) {
                line.classList.add('bg-indigo-600');
                line.classList.remove('bg-gray-300');
            } else {
                line.classList.add('bg-gray-300');
                line.classList.remove('bg-indigo-600');
            }
        }
    }

    // Show/hide step content (now including step 0)
    for (let i = 0; i <= 6; i++) {
        const stepContent = document.getElementById(`step${i}`);
        if (stepContent) {
            if (i === stepNumber) {
                stepContent.classList.remove('hidden');
            } else {
                stepContent.classList.add('hidden');
            }
        }
    }

    // Call specific function for step 2
    if (stepNumber === 2) {
        if (typeof get_article_urls === 'function') {
            get_article_urls();
        } else {
            console.error('get_article_urls function not found');
        }
    }
    else if(stepNumber === 4){
        if (typeof get_html_content === 'function') {
            get_html_content();
        } else {
            console.error('get_html_content function not found');
        }
    }
    else if(stepNumber === 3){
        
        
        get_category_html_content();
    }
}
