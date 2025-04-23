









// Function to create an article card
function createArticleCard(article) {
    return `

        <div class="bg-white p-4 rounded-2xl border border-gray-200" id="bg_${article.slug_id}" onclick="get_article_type('${article.article_category}', '${article.title}', '${article.slug_id}')">
            <div class="flex items-center mb-2">
                <div class="p-3 bg-gray-100 rounded-xl mr-3">
                    <img src="${article.article_type_image}" alt="${article.title}" class="h-[40px] w-[40px] object-cover rounded-t-lg">
                </div>
                <div>
                    <h3 class="font-semibold pb-2">${article.title}</h3>
                    <div class="text-gray-600 mb-2">
                        <span class="px-2 py-1 bg-${article.color_detail_id_data.bg_color} text-${article.color_detail_id_data.text_color} rounded-full text-xs">${article.article_category}</span>
                    </div>
                </div>
            </div>
            
            <p class="text-sm text-gray-700">${article.description}</p>
        </div>

    `;
}

// Function to render articles
function renderArticles(articleTypes) {
    const container = document.getElementById('articles-container');

    if (!Array.isArray(articleTypes) || articleTypes.length === 0) {
        console.error('Invalid or empty articleTypes data:', articleTypes);
        container.innerHTML = "<p>No articles available.</p>";
        return;
    }

    container.innerHTML = articleTypes.map(createArticleCard).join(""); // Efficient DOM update
}

// API function to fetch article types
async function article_type_api(selectedCategory = null) {
    try {
        const access_token = localStorage.getItem("access_token");
        const query_params = new URLSearchParams();

        if (selectedCategory && selectedCategory !== "All") {
            query_params.append("article_category", selectedCategory);
        }

        const response = await fetch(`${list_article_type_url}?${query_params.toString()}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            },
        });

        if (response.ok) {
            const data = await response.json();
            console.log('API Response Data:', data);
            
            renderArticles(data.data); // Render all fetched articles
        } else {
            const error_data = await response.json();
            console.error('Failed to fetch article types:', error_data);
            show_toast("error", `Error: ${error_data.error || "Something went wrong"}`);
        }
    } catch (error) {
        console.error('Network error:', error);
        show_toast("error", "Network error. Please try again later.");
    }
}


article_type_api(); // Fetch and render all articles initially






// Handle category button clicks
document.querySelectorAll('button[data-category]').forEach(button => {
    button.addEventListener('click', function() {
        document.querySelectorAll('button[data-category]').forEach(btn => {
            btn.classList.remove('bg-white');
            btn.classList.add('bg-gray-100');
        });

        this.classList.remove('bg-gray-100');
        this.classList.add('bg-white');

        const category = this.getAttribute('data-category');
        console.log('Selected Category:', category);

        article_type_api(category);
    });
});












// article_type set in onclick 
function get_article_type(article_type_category, article_type_title, slug_id){
        
    const current_url = window.location.href;

    
    // store step in session
    localStorage.setItem("article_type_category", article_type_category);
    localStorage.setItem("article_type_title", article_type_title);
    localStorage.setItem("current_url", current_url);
    localStorage.setItem("article_type_slug_id", slug_id);


    const add_article_ai = document.getElementById("add_article_ai");
    const add_article_manual = document.getElementById("add_article_manual");



    // set color
    const previouslySelected = document.querySelector('.selected-article');
    if (previouslySelected) {
        previouslySelected.style.backgroundColor = ''; // Reset background color
        previouslySelected.classList.remove('selected-article');
    }
    // Select the clicked article card and set its background color
    const selected_div = document.getElementById(`bg_${slug_id}`);
    if(selected_div){

        selected_div.style.backgroundColor = '#cbced4';  // Set selected background color
        selected_div.classList.add('selected-article');  // Mark this as selected
    }



    if (article_type_category === "outliner" || article_type_category === "generative" || article_type_category === "rephrase") {
        add_article_ai.classList.remove("hidden");
        add_article_ai.classList.add("block");
        add_article_manual.classList.remove("block");
        add_article_manual.classList.add("hidden");
        // temp_set_data()
        
        // setTimeout(function() {
        // }, 500);  // Delay the execution until the element is available
        temp_set_ai_data();


    } 
    else if(article_type_category === "manual") {
        add_article_ai.classList.remove("block");
        add_article_ai.classList.add("hidden");
        add_article_manual.classList.remove("hidden");
        add_article_manual.classList.add("block");

        // setTimeout(function() {
        // }, 500);  // Delay the execution until the element is available
        temp_set_manual_data();

    } else {
        // Hide both sections if the article_type_category is not recognized
        add_article_ai.classList.add("hidden");
        add_article_manual.classList.add("hidden");
    }

}




window.addEventListener('load', () => {
    const stored_article_type_category = localStorage.getItem("article_type_category");
    if (stored_article_type_category) {
        // selected_article = false;
        
        get_article_type(stored_article_type_category, '');
    }

});


