

// Domain Connect
function connect_domain() {
    // event.preventDefault(); 
    
    const domain_name = document.getElementById('domain-name').value; 
    console.log(domain_name,'domain_name')
    if (!domain_name) {
        // alert("Please enter a domain name");
        show_toast("error", `Error: Please enter a domain name`);

        return;
    }
    const temp_current_url = window.location.href;


    const url = `https://${domain_name}/wp-admin/authorize-application.php`; 
    const app_name = 'article-innovator-beta';
    const app_id = '0b8ccc2d-9d28-4d28-814c-9088cfdc6edb';
    
    const connect_url = `${url}?app_name=${app_name}&app_id=${app_id}&success_url=${temp_current_url}`; 
    console.log(connect_url,'connect_url')
    window.location.href = connect_url;
    
    
    //const connectDomain = document.getElementById('connecting_id');
    //connectDomain.innerText = 'Success';

    // https://127.0.0.1:8000/domain/add/?site_url=https%3A%2F%2Fronak-wolf.botxbyte.com&user_login=julie&password=fFDE%20YrOf%20Vs9C%20PeFn%205wxz%20KcYs
    return false; 
}

let current_page_url = window.location.href;
let domain_name = '';
let wp_username = '';
let wp_password = '';


const url_params = new URLSearchParams(window.location.search);

// Get user_login and password
wp_username = url_params.get('user_login');
wp_password = url_params.get('password');


// Extract the site_url parameter and process it
const siteUrl = url_params.get('site_url');

if (siteUrl) {
    domain_name = decodeURIComponent(siteUrl.replace(/\+/g, ' '));

    const url = new URL(domain_name);
    domain_name = url.hostname;  // Extracts the hostname (domain)
}


console.log('domain_name:', domain_name);
const domain_name_element = document.querySelector('[name="domain_name"]');
if(domain_name_element){
    domain_name_element.value = domain_name;
}

if(domain_name){
    
    // domain Connect line 
    document.getElementById("line1").classList.add("bg-indigo-600");
    

    // domain Simulate loading
    let mainLoader = document.getElementById('mainLoader');
    if(mainLoader){
        mainLoader.classList.remove('hidden');
    }

    let loader1 = document.getElementById('loader1');
    if(loader1){
        loader1.classList.remove('hidden');

    }

    // Simulate loading time for step 1
    setTimeout(() => {
        stopLoader('loader1-spinner');
        document.getElementById('loader2').classList.remove('hidden');


        // call add test article
        add_test_article();

    }, 2000);
}

let data = {
    wp_username : wp_username,
    wp_password : wp_password,
    domain_name : domain_name,
};




//  connect domain
function stopLoader(loaderId) {
    console.log("Stopping loader for:", loaderId); // Debugging line
    const loader = document.getElementById(loaderId);
    loader.classList.remove('animate-spin');
    loader.classList.remove('border-t-indigo-600');
    loader.classList.remove('w-6', 'h-6', 'border-2', 'p-2');
    // loader.classList.add('w-10', 'h-10'); // Comment this line if you don’t want to change the size

    loader.innerHTML = `<div class=""><svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 0C3.592 0 0 3.592 0 8C0 12.408 3.592 16 8 16C12.408 16 16 12.408 16 8C16 3.592 12.408 0 8 0ZM11.824 6.16L7.288 10.696C7.176 10.808 7.024 10.872 6.864 10.872C6.704 10.872 6.552 10.808 6.44 10.696L4.176 8.432C3.944 8.2 3.944 7.816 4.176 7.584C4.408 7.352 4.792 7.352 5.024 7.584L6.864 9.424L10.976 5.312C11.208 5.08 11.592 5.08 11.824 5.312C12.056 5.544 12.056 5.92 11.824 6.16Z" fill="#059669"/>
        </svg></div>`;
}