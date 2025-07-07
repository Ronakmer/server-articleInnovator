// Global variables for state management
let selectedElement = null;
let selectedInput = null;
let extraValueArray = [];
let removeContentArray = [];
let currentSelectorData = null;

// Add status tracking for selectors
let selectorStatus = {
    'source_title': false,
    'source_tags': false,
    'source_categories': false,
    'source_author': false,
    'source_published_date': false,
    'source_featured_image': false,
    'source_content': false,
    'seo': false
};

async function get_html_content() {
    const competitor_domain_mapping_slug_id = localStorage.getItem('competitor_domain_mapping_slug_id');
    const access_token = localStorage.getItem("access_token");
    
    // Show loader in HTML container
    showHtmlLoader();
    
    const params = new URLSearchParams();
    
    if (competitor_domain_mapping_slug_id) {
        params.append("competitor_domain_mapping_slug_id", competitor_domain_mapping_slug_id);
    }
    params.append("type", "article");

    const full_url = `${scrap_html_content_url}?${params.toString()}`;

    try {
        const response = await fetch(full_url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            }
        });

        const response_data = await response.json();
        console.log("API Response - HTML content and selectors:", response_data);
        
        if (response.ok && response_data.status === "success") {
            // Store the selector data globally from the API nested structure
            currentSelectorData = response_data.data.selectors?.selectors_data?.selectors || {};
            
            // Update aiSelector variable for compatibility with existing functions
            window.aiSelector = currentSelectorData;
            
            // Store only the competitor_domain_mapping_id for API calls
            window.competitor_domain_mapping_id = response_data.data.competitor_domain_mapping_id;
            
            // Store slug IDs from API response for add selector functionality
            if (response_data.data.competitor_article_url_slug_id) {
                localStorage.setItem('competitor_article_url_slug_id', response_data.data.competitor_article_url_slug_id);
                console.log('Stored competitor_article_url_slug_id:', response_data.data.competitor_article_url_slug_id);
            }
            
            if (response_data.data.competitor_selected_url_slug_id) {
                localStorage.setItem('competitor_selected_url_slug_id', response_data.data.competitor_selected_url_slug_id);
                console.log('Stored competitor_selected_url_slug_id:', response_data.data.competitor_selected_url_slug_id);
            }
            
            console.log('API Selector Data Loaded:', currentSelectorData);
            console.log('Available selector keys from API:', Object.keys(currentSelectorData));
            
            // Display the HTML content
            displayHtmlContent(response_data.data.html_content);
            
            // Initialize the interface using old code style
            if (typeof addTagInteractivity === 'function') {
                addTagInteractivity();
            } else {
                // Fallback to built-in initialization
                initializeSelectorInterface();
            }
            
            // Update button status indicators after loading data
            updateAllButtonStatus();
            
            // After successful API load and initialization, highlight title button
            initializeDefaultTitleButton();
            
            show_toast("success", response_data.data.message || "Content loaded successfully");
        } else {
            show_toast("error", response_data.data.message || "Something went wrong");
            hideHtmlLoader();
        }
    } catch (error) {
        console.error("Network error:", error);
        show_toast("error", "Network error. Please try again later.");
        hideHtmlLoader();
    }
}

/**
 * Show simple loader in main HTML container
 */
function showHtmlLoader() {
    const htmlContainer = document.getElementById('html-container-article');
    if (!htmlContainer) {
        console.error("HTML container not found");
        return;
    }

    // Clear container and show just the spinner
    htmlContainer.innerHTML = `
                <div style="
                    width: 40px;
                    height: 40px;
                    border: 4px solid #e5e7eb;
                    border-top: 4px solid #6366f1;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
            margin: 200px auto;
                "></div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
}

/**
 * Hide loader from main HTML container
 */
function hideHtmlLoader() {
    const htmlContainer = document.getElementById('html-container-article');
    if (htmlContainer) {
        htmlContainer.innerHTML = '';
    }
}

/**
 * Display HTML content in an iframe for safe rendering
 */
function displayHtmlContent(htmlContent) {
    const htmlContainer = document.getElementById('html-container-article');
    if (!htmlContainer) {
        console.error("HTML container not found");
        return;
    }

    // Hide HTML loader but keep overlay for future use
    hideHtmlLoader();
    
    // Process HTML content to fix mixed content issues
    const processedHtml = fixMixedContentImages(htmlContent);
    
    // Create iframe for safe HTML rendering
    htmlContainer.innerHTML = '';
    const iframe = document.createElement('iframe');
    iframe.id = 'html-content-iframe';
    iframe.style.width = '100%';
    iframe.style.height = '600px';
    // iframe.style.border = '1px solid #e5e7eb';
    iframe.style.borderRadius = '8px';
    
    // Use srcdoc for better content loading
    iframe.srcdoc = processedHtml;
    
    htmlContainer.appendChild(iframe);
    
    // Wait for iframe to load then add interactivity
    iframe.addEventListener('load', function() {
        console.log('Iframe loaded successfully');
        setTimeout(() => {
            if (typeof addTagInteractivity === 'function') {
                addTagInteractivity();
            } else {
            addHtmlInteractivity();
            }
        }, 100);
    });
    
    // Fallback: if iframe doesn't load in 2 seconds, try direct content injection
    setTimeout(() => {
        if (!iframe.contentDocument || !iframe.contentDocument.body || iframe.contentDocument.body.innerHTML.trim() === '') {
            console.warn('Iframe failed to load, trying direct content injection');
            try {
                iframe.contentDocument.open();
                iframe.contentDocument.write(processedHtml);
                iframe.contentDocument.close();
                setTimeout(() => {
                    if (typeof addTagInteractivity === 'function') {
                        addTagInteractivity();
                    } else {
                    addHtmlInteractivity();
                    }
                }, 100);
            } catch (error) {
                console.error('Failed to inject content into iframe:', error);
                // Last resort: use div with innerHTML
                displayHtmlContentFallback(processedHtml, htmlContainer);
            }
        }
    }, 2000);
}

/**
 * Fallback method to display HTML content using div with innerHTML
 */
function displayHtmlContentFallback(htmlContent, container) {
    console.log('Using fallback method to display HTML content');
    container.innerHTML = '';
    
    const contentDiv = document.createElement('div');
    contentDiv.id = 'html-content-div';
    contentDiv.style.width = '100%';
    contentDiv.style.height = '600px';
    contentDiv.style.border = '1px solid #e5e7eb';
    contentDiv.style.borderRadius = '8px';
    contentDiv.style.overflow = 'auto';
    contentDiv.style.padding = '10px';
    contentDiv.style.backgroundColor = '#fff';
    
    // Set the HTML content
    contentDiv.innerHTML = htmlContent;
    
    container.appendChild(contentDiv);
    
    // Add interactivity to the HTML elements
    if (typeof addTagInteractivity === 'function') {
        addTagInteractivity();
    } else {
    addHtmlInteractivityFallback();
    }
}

/**
 * Fix mixed content issues and remove advertising scripts
 */
function fixMixedContentImages(htmlContent) {
    // Create a temporary div to parse HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = htmlContent;
    
    // Remove Google AdSense and advertising-related scripts and elements
    removeAdvertisingContent(tempDiv);
    
    // Find all img elements and fix src attributes
    const images = tempDiv.querySelectorAll('img');
    images.forEach(img => {
        // Fix src attribute
        const src = img.getAttribute('src');
        if (src && src.startsWith('http://')) {
            const httpsUrl = src.replace('http://', 'https://');
            img.setAttribute('src', httpsUrl);
            console.log(`Converted image URL: ${src} -> ${httpsUrl}`);
        }
        
        // Fix data-src for lazy loaded images
        const dataSrc = img.getAttribute('data-src');
        if (dataSrc && dataSrc.startsWith('http://')) {
            const httpsUrl = dataSrc.replace('http://', 'https://');
            img.setAttribute('data-src', httpsUrl);
            console.log(`Converted data-src URL: ${dataSrc} -> ${httpsUrl}`);
        }
        
        // Fix srcset attribute
        const srcset = img.getAttribute('srcset');
        if (srcset && srcset.includes('http://')) {
            const httpsSrcset = srcset.replace(/http:\/\//g, 'https://');
            img.setAttribute('srcset', httpsSrcset);
            console.log('Converted srcset URLs to HTTPS');
        }
    });
    
    // Fix link elements (CSS, favicons, etc.)
    const links = tempDiv.querySelectorAll('link[href^="http://"]');
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('http://')) {
            const httpsUrl = href.replace('http://', 'https://');
            link.setAttribute('href', httpsUrl);
            console.log(`Converted link URL: ${href} -> ${httpsUrl}`);
        }
    });
    
    // Fix script sources (but only keep non-advertising scripts)
    const scripts = tempDiv.querySelectorAll('script[src^="http://"]');
    scripts.forEach(script => {
        const src = script.getAttribute('src');
        if (src && src.startsWith('http://')) {
            const httpsUrl = src.replace('http://', 'https://');
            script.setAttribute('src', httpsUrl);
            console.log(`Converted script URL: ${src} -> ${httpsUrl}`);
        }
    });
    
    // Fix background images in style attributes
    const elementsWithStyle = tempDiv.querySelectorAll('[style*="background-image"]');
    elementsWithStyle.forEach(element => {
        let style = element.getAttribute('style');
        if (style && style.includes('http://')) {
            style = style.replace(/http:\/\//g, 'https://');
            element.setAttribute('style', style);
            console.log('Converted background image URL in style attribute');
        }
    });
    
    // Fix CSS background images in style tags
    const styleTags = tempDiv.querySelectorAll('style');
    styleTags.forEach(styleTag => {
        let cssContent = styleTag.textContent;
        if (cssContent && cssContent.includes('http://')) {
            cssContent = cssContent.replace(/http:\/\//g, 'https://');
            styleTag.textContent = cssContent;
            console.log('ARTICLE: Converted background image URLs in CSS');
        }
    });
    
    // Add meta tag to upgrade insecure requests - FIXED CSP PLACEMENT
    if (!htmlContent.includes('upgrade-insecure-requests')) {
        const existingHead = tempDiv.querySelector('head');
        if (existingHead) {
            // Insert CSP meta tag at the very beginning of head
            const cspMeta = document.createElement('meta');
            cspMeta.setAttribute('http-equiv', 'Content-Security-Policy');
            cspMeta.setAttribute('content', 'upgrade-insecure-requests');
            existingHead.insertBefore(cspMeta, existingHead.firstChild);
            
            // Add viewport meta if not exists
            if (!existingHead.querySelector('meta[name="viewport"]')) {
                const viewportMeta = document.createElement('meta');
                viewportMeta.setAttribute('name', 'viewport');
                viewportMeta.setAttribute('content', 'width=device-width, initial-scale=1');
                existingHead.appendChild(viewportMeta);
            }
            
            // Add CSS to fix iframe content positioning - OPTIMIZED TO MINIMIZE EMPTY SPACES
            const iframeFixStyle = document.createElement('style');
            iframeFixStyle.textContent = `
                html { 
                    margin: 0 !important; 
                    padding: 0 !important; 
                    width: 100% !important;
                    height: 100% !important;
                    overflow: visible !important;
                }
                body { 
                    margin: 0 !important; 
                    padding: 2px !important; 
                    width: calc(100% - 4px) !important;
                    min-width: calc(100% - 4px) !important;
                    max-width: calc(100% - 4px) !important;
                    overflow-x: visible !important;
                    overflow-y: auto !important;
                    box-sizing: border-box !important;
                    position: relative !important;
                    left: 0 !important;
                    right: 0 !important;
                    min-height: auto !important;
                    height: auto !important;
                }
                * { 
                    box-sizing: border-box !important;
                }
                img { 
                    max-width: 100% !important; 
                    height: auto !important; 
                    display: block !important;
                    margin: 2px 0 !important;
                }
                /* Reset all common container classes - MINIMAL PADDING */
                .container, .content, .main, .wrapper, .page, .site, .layout,
                .row, .col, .column, .grid, .flex, .section, .block,
                .inner, .center, .middle, .core, .primary {
                    width: 100% !important; 
                    max-width: 100% !important;
                    min-width: 0 !important;
                    margin: 0 !important;
                    padding: 2px !important;
                    position: relative !important;
                    left: 0 !important;
                    right: 0 !important;
                    transform: none !important;
                    float: none !important;
                    clear: both !important;
                }
                /* Reset layout elements - MINIMAL SPACING */
                div, section, article, header, main, aside, footer, nav {
                    position: relative !important;
                    left: 0 !important;
                    right: 0 !important;
                    margin: 0 !important;
                    padding: 1px 2px !important;
                    float: none !important;
                    transform: translateX(0px) !important;
                }
                /* Text elements - TIGHT SPACING */
                p, h1, h2, h3, h4, h5, h6, span {
                    max-width: 100% !important;
                    word-wrap: break-word !important;
                    margin: 2px 0 !important;
                    padding: 1px 0 !important;
                }
                /* Fix tables and media - COMPACT */
                table {
                    width: 100% !important;
                    max-width: 100% !important;
                    table-layout: auto !important;
                    margin: 2px 0 !important;
                    border-collapse: collapse !important;
                }
                td, th {
                    padding: 2px 4px !important;
                }
                pre, code {
                    white-space: pre-wrap !important;
                    word-wrap: break-word !important;
                    overflow-wrap: break-word !important;
                    max-width: 100% !important;
                    margin: 2px 0 !important;
                    padding: 2px !important;
                }
                /* Reset any absolute/fixed positioning that causes cutting */
                [style*="position: absolute"], [style*="position: fixed"] {
                    position: relative !important;
                    left: 0 !important;
                    right: 0 !important;
                    top: auto !important;
                }
                /* Reset negative margins that cause left cutting */
                [style*="margin-left: -"], [style*="margin-right: -"] {
                    margin-left: 0 !important;
                    margin-right: 0 !important;
                }
                /* Reset transforms that cause content shifting */
                [style*="transform"], [style*="translateX"], [style*="translate3d"] {
                    transform: none !important;
                }
                /* Remove excessive bottom spacing */
                br {
                    line-height: 0.5 !important;
                }
                /* Compact lists */
                ul, ol {
                    margin: 2px 0 !important;
                    padding-left: 15px !important;
                }
                li {
                    margin: 1px 0 !important;
                }
            `;
            existingHead.appendChild(iframeFixStyle);
            
            console.log('ARTICLE: Added CSP meta tag and iframe fix styles to existing head');
        } else {
            // Create head with proper CSP placement
            const headElement = document.createElement('head');
            const cspMeta = document.createElement('meta');
            cspMeta.setAttribute('http-equiv', 'Content-Security-Policy');
            cspMeta.setAttribute('content', 'upgrade-insecure-requests');
            headElement.appendChild(cspMeta);
            
            const viewportMeta = document.createElement('meta');
            viewportMeta.setAttribute('name', 'viewport');
            viewportMeta.setAttribute('content', 'width=device-width, initial-scale=1');
            headElement.appendChild(viewportMeta);
            
            // Add CSS to fix iframe content positioning - OPTIMIZED TO MINIMIZE EMPTY SPACES
            const iframeFixStyle = document.createElement('style');
            iframeFixStyle.textContent = `
                html { 
                    margin: 0 !important; 
                    padding: 0 !important; 
                    width: 100% !important;
                    height: 100% !important;
                    overflow: visible !important;
                }
                body { 
                    margin: 0 !important; 
                    padding: 2px !important; 
                    width: calc(100% - 4px) !important;
                    min-width: calc(100% - 4px) !important;
                    max-width: calc(100% - 4px) !important;
                    overflow-x: visible !important;
                    overflow-y: auto !important;
                    box-sizing: border-box !important;
                    position: relative !important;
                    left: 0 !important;
                    right: 0 !important;
                    min-height: auto !important;
                    height: auto !important;
                }
                * { 
                    box-sizing: border-box !important;
                }
                img { 
                    max-width: 100% !important; 
                    height: auto !important; 
                    display: block !important;
                    margin: 2px 0 !important;
                }
                /* Reset all common container classes - MINIMAL PADDING */
                .container, .content, .main, .wrapper, .page, .site, .layout,
                .row, .col, .column, .grid, .flex, .section, .block,
                .inner, .center, .middle, .core, .primary {
                    width: 100% !important; 
                    max-width: 100% !important;
                    min-width: 0 !important;
                    margin: 0 !important;
                    padding: 2px !important;
                    position: relative !important;
                    left: 0 !important;
                    right: 0 !important;
                    transform: none !important;
                    float: none !important;
                    clear: both !important;
                }
                /* Reset layout elements - MINIMAL SPACING */
                div, section, article, header, main, aside, footer, nav {
                    position: relative !important;
                    left: 0 !important;
                    right: 0 !important;
                    margin: 0 !important;
                    padding: 1px 2px !important;
                    float: none !important;
                    transform: translateX(0px) !important;
                }
                /* Text elements - TIGHT SPACING */
                p, h1, h2, h3, h4, h5, h6, span {
                    max-width: 100% !important;
                    word-wrap: break-word !important;
                    margin: 2px 0 !important;
                    padding: 1px 0 !important;
                }
                /* Fix tables and media - COMPACT */
                table {
                    width: 100% !important;
                    max-width: 100% !important;
                    table-layout: auto !important;
                    margin: 2px 0 !important;
                    border-collapse: collapse !important;
                }
                td, th {
                    padding: 2px 4px !important;
                }
                pre, code {
                    white-space: pre-wrap !important;
                    word-wrap: break-word !important;
                    overflow-wrap: break-word !important;
                    max-width: 100% !important;
                    margin: 2px 0 !important;
                    padding: 2px !important;
                }
                /* Reset any absolute/fixed positioning that causes cutting */
                [style*="position: absolute"], [style*="position: fixed"] {
                    position: relative !important;
                    left: 0 !important;
                    right: 0 !important;
                    top: auto !important;
                }
                /* Reset negative margins that cause left cutting */
                [style*="margin-left: -"], [style*="margin-right: -"] {
                    margin-left: 0 !important;
                    margin-right: 0 !important;
                }
                /* Reset transforms that cause content shifting */
                [style*="transform"], [style*="translateX"], [style*="translate3d"] {
                    transform: none !important;
                }
                /* Remove excessive bottom spacing */
                br {
                    line-height: 0.5 !important;
                }
                /* Compact lists */
                ul, ol {
                    margin: 2px 0 !important;
                    padding-left: 15px !important;
                }
                li {
                    margin: 1px 0 !important;
                }
            `;
            headElement.appendChild(iframeFixStyle);
            
            tempDiv.insertBefore(headElement, tempDiv.firstChild);
            console.log('ARTICLE: Created new head with CSP meta tag and iframe fix styles');
        }
    }
    
    return tempDiv.innerHTML;
}

/**
 * Remove advertising content and scripts to prevent conflicts
 */
function removeAdvertisingContent(container) {
    // Remove Google AdSense elements
    const adElements = container.querySelectorAll('.adsbygoogle, ins.adsbygoogle, [class*="adsbygoogle"], [id*="google_ads"], [class*="google-ad"], [id*="div-gpt-ad"]');
    adElements.forEach(el => {
        console.log('Removed AdSense element:', el.className || el.id);
        el.remove();
    });
    
    // Remove scripts that contain advertising code
    const scripts = container.querySelectorAll('script');
    scripts.forEach(script => {
        const scriptContent = script.textContent || script.src || '';
        const scriptSrc = script.getAttribute('src') || '';
        
        // Check for advertising-related scripts
        const isAdScript = 
            scriptContent.includes('adsbygoogle') ||
            scriptContent.includes('googletag') ||
            scriptContent.includes('__googlefc') ||
            scriptContent.includes('google_ad') ||
            scriptSrc.includes('googletagservices') ||
            scriptSrc.includes('googlesyndication') ||
            scriptSrc.includes('googleadservices') ||
            scriptSrc.includes('doubleclick') ||
            scriptSrc.includes('adsystem.google') ||
            scriptSrc.includes('pagead2.googlesyndication') ||
            scriptSrc.includes('googletagmanager');
            
        if (isAdScript) {
            console.log('Removed advertising script:', scriptSrc || 'inline script');
            script.remove();
        }
    });
    
    // Remove ad-related iframes
    const iframes = container.querySelectorAll('iframe');
    iframes.forEach(iframe => {
        const src = iframe.getAttribute('src') || '';
        const isAdFrame = 
            src.includes('googlesyndication') ||
            src.includes('doubleclick') ||
            src.includes('googleadservices') ||
            src.includes('google.com/pagead') ||
            iframe.name?.includes('google_ads');
            
        if (isAdFrame) {
            console.log('Removed advertising iframe:', src);
            iframe.remove();
        }
    });
    
    // Remove elements with ad-related classes or IDs
    const adSelectors = [
        '[class*="advertisement"]',
        '[id*="advertisement"]', 
        '[class*="ad-banner"]',
        '[id*="ad-banner"]',
        '[class*="sponsored"]',
        '[id*="sponsored"]',
        '.ad, .ads',
        '#ad, #ads',
        '[class*="adsense"]',
        '[id*="adsense"]'
    ];
    
    adSelectors.forEach(selector => {
        try {
            const elements = container.querySelectorAll(selector);
            elements.forEach(el => {
                console.log('Removed ad-related element:', selector, el.className || el.id);
                el.remove();
            });
        } catch (error) {
            // Ignore selector errors
        }
    });
    
    console.log('Advertising content cleanup completed');
}

/**
 * Initialize title input with API data (from original code)
 */
function initializeTitleInput() {
    const inputFieldsContainer = document.getElementById('input-fields-container');
    if (!inputFieldsContainer) {
        console.error('Input fields container not found');
        return;
    }

    console.log(inputFieldsContainer, 'inputFieldsContainer')
    // Clear existing inputs
    inputFieldsContainer.innerHTML = '';

    // Define the selector key for title with source_ prefix
    const selectorKey = 'source_title';

    // Ensure aiSelector is populated before accessing it
    if (!window.aiSelector) {
        console.warn('AI Selector is not populated yet.');
        return;
    }

    // Get the corresponding selector data for title
    const selectorData = window.aiSelector[selectorKey];
    console.log('Selector Data:', selectorData);

    // Call the function to add inputs dynamically for the title
    addStandardInputs(inputFieldsContainer, selectorKey, selectorData);
}

/**
 * Add standard inputs (from original code design)
 */
function addStandardInputs(container, selectorKey, selectorData) {
    // Convert the selector data to match the expected format
    const formattedData = {
        css_selector: selectorData?.selector || '',
        attribute: selectorData?.attribute || '',
        multiple: selectorData?.multiple || false
    };

    if (selectorKey === 'seo') {
        container.innerHTML = `
            <div id="seo" class="w-full md:w-1/2 input-section">
                <label class="block font-semibold text-gray-700 mb-2">SEO Settings</label>

                <div class="flex items-center mt-2 border md:w-1/2 p-2 w-full rounded-lg">
                    <input type="checkbox" id="set_metatitle" name="set_metatitle" class="mr-2 p-2 border rounded-lg">
                    <label for="set_metatitle">Set Metatitle</label>
                </div>

                <div class="flex items-center mt-2 border md:w-1/2 p-2 w-full rounded-lg">
                    <input type="checkbox" id="set_metakeywords" name="set_metakeywords" class="mr-2 p-2 border rounded-lg">
                    <label for="set_metakeywords">Set Metakeywords</label>
                </div>
                <div class="flex items-center mt-2 border md:w-1/2 p-2 w-full rounded-lg">
                    <input type="checkbox" id="set_desc" name="set_desc" class="mr-2 p-2 border rounded-lg">
                    <label for="set_desc">Set Description</label>
                </div>
            </div>
        `;
    } else {
        // Add a warning message for null selectors
        const warningMessage = selectorData === null ?
            `<div class="text-yellow-600 text-sm mt-2">No selector available for ${selectorKey}</div>` : '';

        container.innerHTML = `
            <div id="${selectorKey}" class="w-full md:w-1/2 input-section">
                <label class="block font-semibold text-gray-700 mb-2">${selectorKey.replace('source_', '').charAt(0).toUpperCase() + selectorKey.replace('source_', '').slice(1)}</label>
                <div class="relative w-full md:w-1/2">
                    <input type="text" 
                        placeholder="Enter selector"
                        name="selector_value" 
                        value="${formattedData.css_selector}" 
                        class="w-full p-2 pr-12 border rounded-lg">
                    <button type="button" class="search-icon absolute inset-y-0 right-0 flex items-center px-3 bg-indigo-100 hover:bg-indigo-200 rounded-r-lg border-l transition-colors">
                        <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                    </button>
                </div>
                ${warningMessage}
                
                <div class="flex items-center mt-2 border md:w-1/2 p-2 w-full rounded-lg w-fit">
                    <input type="checkbox" 
                        id="multiple" 
                        name="is_multiple" 
                        class="mr-2" 
                        ${formattedData.multiple ? 'checked' : ''}>
                    <label for="multiple">Multiple</label>
                </div>

                <div class="flex items-center mt-2 border md:w-1/2 p-2 w-full rounded-lg">
                    <div class="flex items-center border p-2 rounded-lg w-full">
                        <input type="checkbox" 
                            id="attribute" 
                            name="is_attribute" 
                            class="mr-2 p-2 border rounded-lg" 
                            ${formattedData.attribute ? 'checked' : ''}>
                        <label for="attribute">Attribute</label>
                    </div>
                    <input type="text" 
                        name="attribute_value" 
                        placeholder="SRC, HREF" 
                        class="w-full p-2 border rounded-lg" 
                        value="${formattedData.attribute || ''}">
                </div>

                <input type="hidden" name="selector_key" value="${selectorKey}">
            </div>
        `;

        // Add click event for search icon
        const searchIcon = container.querySelector('.search-icon');
        if (searchIcon) {
            searchIcon.addEventListener('click', function () {
                const input = container.querySelector('input[name="selector_value"]');
                const attributeInput = container.querySelector('input[name="attribute_value"]');
                const isAttribute = container.querySelector('input[name="is_attribute"]')?.checked;

                if (input && input.value) {
                    // Create selectorData object for proper preview
                    const selectorData = {
                        selector: input.value,
                        attribute: isAttribute ? attributeInput?.value : null
                    };
                    updatePreviewContent(selectorData);
                }
            });
        }

        // Add event listeners after rendering
        const input = container.querySelector('input[name="selector_value"]');
        if (input) {
            input.addEventListener('input', function () {
                // Update the old status system
                updateSelectorStatus(null, this);
                // Update the button status indicator
                updateButtonStatusFromInput(selectorKey, this.value);
            });
        }
    }
}

/**
 * Add content inputs with original design
 */
function addContentInputs(container, selectorKey, selectorData) {
    // Convert the selector data to match the expected format
    const formattedData = {
        css_selector: selectorData?.selector || '',
        attribute: selectorData?.attribute || '',
        multiple: selectorData?.multiple || false,
        remove_selectors: selectorData?.remove_selectors || []
    };

    // Add a warning message for null selectors
    const warningMessage = selectorData === null ?
        `<div class="text-yellow-600 text-sm mt-2">No Content Selector Available</div>` : '';

    container.innerHTML = `
        <div id="title" class="w-full md:w-1/2 input-section">
            <label class="block font-semibold text-gray-700 mb-2">Add Content</label>
            <div class="relative w-full md:w-1/2">
                <input type="text" 
                    placeholder="h2, entry title" 
                    name="selector_value" 
                    value="${formattedData.css_selector}" 
                    class="w-full p-2 pr-12 border rounded-lg">
                <button type="button" class="search-icon absolute inset-y-0 right-0 flex items-center px-3 bg-indigo-100 hover:bg-indigo-200 rounded-r-lg border-l transition-colors">
                    <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                </button>
            </div>
            ${warningMessage}
            
            <div class="flex items-center mt-2 border md:w-1/2 p-2 w-full rounded-lg w-fit">
                <input type="checkbox" 
                    id="multiple" 
                    name="is_multiple" 
                    class="mr-2" 
                    ${formattedData.multiple ? 'checked' : ''}>
                <label for="multiple">Multiple</label>
            </div>

            <div class="flex items-center mt-2 border md:w-1/2 p-2 w-full rounded-lg">
                <div class="flex items-center border p-2 rounded-lg w-full">
                    <input type="checkbox" 
                        id="attribute" 
                        name="is_attribute" 
                        class="mr-2 p-2 border rounded-lg" 
                        ${formattedData.attribute ? 'checked' : ''}>
                    <label for="attribute">Attribute</label>
                </div>
                <input type="text" 
                    name="attribute_value" 
                    placeholder="SRC, HREF" 
                    class="w-full p-2 border rounded-lg" 
                    value="${formattedData.attribute || ''}">
            </div>

            <!-- Add Extra Value Toggle Section -->
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; border: 1px solid #d1d5db; border-radius: 8px; width: 100%; max-width: 50%;">
                <label style="color: #374151;">Add extra value</label>
                <label style="position: relative; display: inline-flex; align-items: center; cursor: pointer;">
                    <input type="checkbox" id="extra-value-toggle" style="display: none;">
                    <div style="width: 44px; height: 24px; background-color: #d1d5db; border-radius: 12px; position: relative; transition: all 0.3s ease;" class="toggle-switch">
                        <div style="width: 20px; height: 20px; background-color: white; border-radius: 50%; position: absolute; top: 2px; left: 2px; transition: all 0.3s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.2);" class="toggle-dot"></div>
                    </div>
                </label>
            </div>

            <div id="extra-values-container" class="mt-4"></div>

            <input type="hidden" name="selector_key" value="${selectorKey}">

        </div>
        <div id="remove-content" class="w-full md:w-1/2 input-section">
            <label class="block font-semibold text-gray-700 mb-2">Remove Content</label>
            <div id="remove-content-container" class="flex flex-col gap-2">
                <!-- Remove content inputs will be added here dynamically -->
            </div>

            <!-- Add Extra Value Toggle Section For Remove Content-->
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; border: 1px solid #d1d5db; border-radius: 8px; width: 100%; max-width: 50%; margin-top: 8px;">
                <label style="color: #374151;">Add extra value</label>
                <label style="position: relative; display: inline-flex; align-items: center; cursor: pointer;">
                    <input type="checkbox" id="remove-extra-value-toggle" style="display: none;">
                    <div style="width: 44px; height: 24px; background-color: #d1d5db; border-radius: 12px; position: relative; transition: all 0.3s ease;" class="toggle-switch">
                        <div style="width: 20px; height: 20px; background-color: white; border-radius: 50%; position: absolute; top: 2px; left: 2px; transition: all 0.3s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.2);" class="toggle-dot"></div>
                    </div>
                </label>
            </div>

            <div id="remove-content-checkboxes-container" class="mt-4"></div>
        </div>
    `;

    // Add click event for search icon
    const searchIcon = container.querySelector('.search-icon');
    if (searchIcon) {
        searchIcon.addEventListener('click', function () {
            const input = container.querySelector('input[name="selector_value"]');
            const attributeInput = container.querySelector('input[name="attribute_value"]');
            const isAttribute = container.querySelector('input[name="is_attribute"]')?.checked;

            if (input && input.value) {
                // Create selectorData object for proper preview
                const selectorData = {
                    selector: input.value,
                    attribute: isAttribute ? attributeInput?.value : null
                };
                updatePreviewContent(selectorData);
                // Update button status when search is clicked
                updateButtonStatusFromInput(selectorKey, input.value);
            }
        });
    }

    // Add input event listener for real-time status updates
    const selectorInput = container.querySelector('input[name="selector_value"]');
    if (selectorInput) {
        selectorInput.addEventListener('input', function() {
            updateButtonStatusFromInput(selectorKey, this.value);
        });
    }

    // Add event listeners
    document.getElementById('extra-value-toggle').addEventListener('change', function () {
        const container = document.getElementById('extra-values-container');
        
        // Force visual update for old toggle design
        forceToggleUpdate(this);
        
        if (this.checked) {
            addExtraValueInputs();
        } else {
            container.innerHTML = '';
            // Clear the extra value array and hide the table when toggle is off
            extraValueArray = [];
            updateTable();
        }
    });

    document.getElementById('remove-extra-value-toggle').addEventListener('change', function () {
        const container = document.getElementById('remove-content-checkboxes-container');
        
        // Force visual update for old toggle design
        forceToggleUpdate(this);
        
        if (this.checked) {
            addRemoveContentCheckboxes(container);
        } else {
            container.innerHTML = '';
            removeContentArray = [];
            console.log('Remove content array reset:', removeContentArray);
        }
    });

    // Populate remove content inputs with remove_selectors
    const removeContentContainer = document.getElementById('remove-content-container');
    if (formattedData.remove_selectors && formattedData.remove_selectors.length > 0) {
        formattedData.remove_selectors.forEach((selector, index) => {
            removeContentContainer.appendChild(createRemoveContentInput(selector));
        });
    } else {
        // Add one empty input if no remove selectors
        removeContentContainer.appendChild(createRemoveContentInput());
    }

    // Initialize removeContentArray with remove_selectors
    removeContentArray = [...(formattedData.remove_selectors || [])];
    console.log('Initial Remove Content Array:', removeContentArray);
}

/**
 * Create remove content input (consistent styling)
 */
function createRemoveContentInput(value = '') {
    const inputDiv = document.createElement('div');
    inputDiv.className = 'flex items-center gap-2 mb-2';
    inputDiv.innerHTML = `
        <input type="text" 
            placeholder="CSS selector to remove" 
            class="w-full md:w-1/2 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" 
            value="${value}">
        <button type="button" 
            class="add-btn px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
            title="Add new input" style="min-width: 40px; flex-shrink: 0;">+</button>
        <button type="button" 
            class="remove-btn px-3 py-2 bg-gray-300 text-white rounded-lg hover:bg-gray-600 transition-colors font-medium"
            title="Remove this input" style="min-width: 40px; flex-shrink: 0;">−</button>
    `;
    
    console.log('Created remove content input with buttons:', inputDiv.innerHTML);

    // Add event listeners to buttons
    const addBtn = inputDiv.querySelector('.add-btn');
    const removeBtn = inputDiv.querySelector('.remove-btn');
    const input = inputDiv.querySelector('input');

    console.log('Add button found:', addBtn);
    console.log('Remove button found:', removeBtn);

    if (addBtn) {
        addBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log('Add button clicked');
            addRemoveContentInput();
        });
    }

    if (removeBtn) {
        removeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            console.log('Remove button clicked');
            const container = document.getElementById('remove-content-container');
            if (container.children.length > 1) {
                inputDiv.remove();
                updateRemoveContentArray();
            } else {
                // Clear the input value if it's the last one
                input.value = '';
                updateRemoveContentArray();
            }
        });
    }
    
    if (input) {
        input.addEventListener('input', updateRemoveContentArray);
    }

    return inputDiv;
}

/**
 * Add remove content input (standardized version)
 */
function addRemoveContentInput() {
    const container = document.getElementById('remove-content-container');
    if (!container) return;
    
    const newInput = createRemoveContentInput();
    container.appendChild(newInput);
    updateRemoveContentArray();
}

/**
 * Remove content input (from original code)
 */
function removeContentInput(button) {
    const container = document.getElementById('remove-content-container');
    if (container.children.length > 1) {
        button.closest('.flex').remove();
        updateRemoveContentArray();
    }
}

/**
 * Add remove content checkboxes (from original code)
 */
function addRemoveContentCheckboxes(container) {
    // Clear any existing checkboxes
    container.innerHTML = '';

    // Define the checkbox names and their associated actions
    const checkboxNames = [
        { label: 'Remove Blocker Images', name: 'remove_blocker_images' },
        { label: 'Remove Google Analytics', name: 'remove_google_analytics' },
        { label: 'Remove Google Advanced', name: 'remove_google_advanced' },
        { label: 'Remove Script', name: 'remove_script' },
        { label: 'Remove 404 Internal Links', name: 'remove_404_internal_links' }
    ];

    // Create and append the checkboxes
    checkboxNames.forEach((checkbox, index) => {
        const checkboxWrapper = document.createElement('div');
        checkboxWrapper.classList.add('flex', 'items-center', 'mt-2', 'border', 'md:w-1/2', 'p-2', 'w-full', 'rounded-lg', 'w-fit');

        const inputCheckbox = document.createElement('input');
        inputCheckbox.type = 'checkbox';
        inputCheckbox.id = `remove-checkbox-${index + 1}`;
        inputCheckbox.name = checkbox.name;
        inputCheckbox.classList.add('mr-2');

        const label = document.createElement('label');
        label.setAttribute('for', `remove-checkbox-${index + 1}`);
        label.innerText = checkbox.label;

        // Add the checkbox and label to the wrapper
        checkboxWrapper.appendChild(inputCheckbox);
        checkboxWrapper.appendChild(label);

        // Append the wrapper to the container
        container.appendChild(checkboxWrapper);
    });
}

/**
 * Add extra value inputs (from original code)
 */
function addExtraValueInputs() {
    const container = document.getElementById('extra-values-container');

    // Create a new input pair (Add Column Name and Selector Value)
    const extraValueSection = document.createElement('div');
    extraValueSection.classList.add('extra-value-input-section', 'mb-2', 'flex', 'gap-2', 'items-center');

    // Create Add Column Name input
    const columnNameInput = document.createElement('input');
    columnNameInput.type = 'text';
    columnNameInput.placeholder = 'Add Column Name';
    columnNameInput.classList.add('p-2', 'border', 'rounded-lg', 'w-full');

    // Create Selector Value input
    const selectorValueInput = document.createElement('input');
    selectorValueInput.type = 'text';
    selectorValueInput.placeholder = 'Selector Value';
    selectorValueInput.classList.add('p-2', 'border', 'rounded-lg', 'w-full');
    // Mark this as an extra value input to prevent HTML click interference
    selectorValueInput.setAttribute('data-extra-value-input', 'true');

    // Create Add button to add more inputs
    const addButton = document.createElement('button');
    addButton.classList.add('px-2', 'py-1', 'text-white', 'bg-indigo-600', 'rounded-lg', 'hover:bg-indigo-700');
    addButton.innerText = '+';
    addButton.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        addExtraValueInputs();
    });

    // Create Remove button to remove both input fields
    const removeButton = document.createElement('button');
    removeButton.classList.add('px-2', 'py-1', 'text-white', 'bg-gray-300', 'rounded-lg', 'hover:bg-gray-400');
    removeButton.innerText = '-';
    removeButton.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        console.log('Removing extra value input section');
        // Remove input section
        extraValueSection.remove();
        // Also update the array when removing
        updateExtraValueArray();
    });

    // Append the inputs and buttons to the container
    extraValueSection.appendChild(columnNameInput);
    extraValueSection.appendChild(selectorValueInput);
    extraValueSection.appendChild(addButton);
    extraValueSection.appendChild(removeButton);

    // Append the section to the container
    container.appendChild(extraValueSection);

    // Listen for changes in the input fields to update the array
    columnNameInput.addEventListener('input', updateExtraValueArray);
    selectorValueInput.addEventListener('input', updateExtraValueArray);
    
    // Debug: Log when extra value inputs are created
    console.log('Created extra value inputs, current array:', extraValueArray);
}

/**
 * Update extra value array (from original code)
 */
function updateExtraValueArray() {
    console.log('🔄 === STARTING updateExtraValueArray() ===');
    
    // Check if extra values container exists
    const extraValuesContainer = document.getElementById('extra-values-container');
    console.log('Extra values container found:', extraValuesContainer);
    console.log('Extra values container innerHTML:', extraValuesContainer ? extraValuesContainer.innerHTML : 'Container not found');

    // Get all input fields for Column Name and Selector Value (more flexible approach)
    const columnNameInputs = document.querySelectorAll('input[placeholder="Add Column Name"]');
    const selectorValueInputs = document.querySelectorAll('input[placeholder="Selector Value"]');

    console.log('Found column inputs:', columnNameInputs.length);
    console.log('Found selector inputs:', selectorValueInputs.length);

    // Debug: log the actual inputs found
    console.log('Column inputs:', columnNameInputs);
    console.log('Selector inputs:', selectorValueInputs);

    // Clear the existing array
    extraValueArray = [];
    console.log('Cleared extraValueArray, starting fresh...');

    // Early exit if no inputs found
    if (columnNameInputs.length === 0) {
        console.log('❌ EARLY EXIT: No column name inputs found! Check if inputs with placeholder "Add Column Name" exist.');
        return;
    }
    
    if (selectorValueInputs.length === 0) {
        console.log('❌ EARLY EXIT: No selector value inputs found! Check if inputs with placeholder "Selector Value" exist.');
        return;
    }

    console.log('✅ Both input types found, proceeding to loop...');

    // Loop through all inputs and append their values to the array
    columnNameInputs.forEach((columnNameInput, index) => {
        const columnName = columnNameInput.value.trim();
        const selectorValue = selectorValueInputs[index] ? selectorValueInputs[index].value.trim() : '';

        console.log(`Input ${index}:`);
        console.log(`  - Column Name Input:`, columnNameInput);
        console.log(`  - Column Name Value: "${columnName}" (length: ${columnName.length})`);
        console.log(`  - Selector Input:`, selectorValueInputs[index]);
        console.log(`  - Selector Value: "${selectorValue}" (length: ${selectorValue.length})`);
        console.log(`  - Both filled? Column: ${!!columnName}, Selector: ${!!selectorValue}`);
        console.log(`  - Raw values - Column: "${columnNameInput.value}", Selector: "${selectorValueInputs[index] ? selectorValueInputs[index].value : 'N/A'}"`);

        // Only add to the array if both fields are filled
        if (columnName && selectorValue) {
            console.log(`✅ Adding to array: ${columnName} -> ${selectorValue}`);
            extraValueArray.push({
                column_name: columnName,
                selector_value: selectorValue
            });
        } else {
            console.log(`❌ Not adding - missing values. Column: "${columnName}", Selector: "${selectorValue}"`);
            if (!columnName && selectorValue) {
                console.log(`💡 TIP: You have a selector but no column name. Type something in "Add Column Name" field first!`);
            } else if (columnName && !selectorValue) {
                console.log(`💡 TIP: You have a column name but no selector. Click on an HTML element to set the selector!`);
            } else if (!columnName && !selectorValue) {
                console.log(`💡 TIP: Both fields are empty. Add a column name and click an HTML element!`);
            }
        }
    });

    // Log the updated array (for debugging purposes)
    console.log('🔥 FINAL RESULT - Updated Extra Value Array:', extraValueArray);
    console.log('🔥 Array length:', extraValueArray.length);
    console.log('🔥 === ENDING updateExtraValueArray() ===');

    // Update the table display with the values from the extraValueArray
    updateTable();
}

/**
 * Debug function to check extra value status
 */
function debugExtraValueStatus() {
    console.log('=== DEBUG EXTRA VALUE STATUS ===');
    console.log('1. Extra values container:', document.getElementById('extra-values-container'));
    console.log('2. Extra value toggle state:', document.getElementById('extra-value-toggle')?.checked);
    console.log('3. Extra value input sections:', document.querySelectorAll('.extra-value-input-section').length);
    console.log('4. Column name inputs:', document.querySelectorAll('input[placeholder="Add Column Name"]').length);
    console.log('5. Selector value inputs:', document.querySelectorAll('input[placeholder="Selector Value"]').length);
    console.log('6. Current extraValueArray:', extraValueArray);
    console.log('7. Table container:', document.getElementById('extra_value_tbody_article'));
    console.log('================================');
}

// Call this function to debug
window.debugExtraValues = debugExtraValueStatus;

/**
 * Test function to manually add extra value
 */
function testAddExtraValue() {
    const columnInputs = document.querySelectorAll('input[placeholder="Add Column Name"]');
    const selectorInputs = document.querySelectorAll('input[placeholder="Selector Value"]');
    
    if (columnInputs.length > 0 && selectorInputs.length > 0) {
        columnInputs[0].value = "Test Column";
        selectorInputs[0].value = "h1.entry-title";
        updateExtraValueArray();
        console.log("Test values added - check if table appears");
            } else {
            console.log("No extra value inputs found - make sure to toggle 'Add extra value' ON first");
            // Also log all inputs we can find for debugging
            const allInputs = document.querySelectorAll('input');
            console.log('All inputs found:', allInputs.length);
            allInputs.forEach((input, index) => {
                console.log(`Input ${index}:`, input.placeholder, input.value);
            });
        }
}

window.testAddExtraValue = testAddExtraValue;

/**
 * Simple manual checker for inputs
 */
function checkInputsManually() {
    console.log('=== MANUAL INPUT CHECK ===');
    
    // Check for all inputs on the page
    const allInputs = document.querySelectorAll('input');
    console.log(`Total inputs on page: ${allInputs.length}`);
    
    // Check specifically for our placeholders
    const columnInputs = document.querySelectorAll('input[placeholder="Add Column Name"]');
    const selectorInputs = document.querySelectorAll('input[placeholder="Selector Value"]');
    
    console.log(`Column name inputs found: ${columnInputs.length}`);
    console.log(`Selector value inputs found: ${selectorInputs.length}`);
    
    // Log details of each relevant input
    columnInputs.forEach((input, index) => {
        console.log(`Column Input ${index}:`, {
            element: input,
            value: input.value,
            placeholder: input.placeholder,
            class: input.className
        });
    });
    
    selectorInputs.forEach((input, index) => {
        console.log(`Selector Input ${index}:`, {
            element: input,
            value: input.value,
            placeholder: input.placeholder,
            class: input.className
        });
    });
    
    // Try to manually create array
    if (columnInputs.length > 0 && selectorInputs.length > 0) {
        const manualArray = [];
        for (let i = 0; i < Math.min(columnInputs.length, selectorInputs.length); i++) {
            const columnValue = columnInputs[i].value.trim();
            const selectorValue = selectorInputs[i].value.trim();
            
            console.log(`Pair ${i}: "${columnValue}" -> "${selectorValue}"`);
            
            if (columnValue && selectorValue) {
                manualArray.push({
                    column_name: columnValue,
                    selector_value: selectorValue
                });
            }
        }
        console.log('Manual array result:', manualArray);
    }
    
    console.log('=========================');
}

window.checkInputsManually = checkInputsManually;

/**
 * Check which input is currently focused
 */
function checkFocusedInput() {
    console.log('Currently focused input:', selectedInput);
    if (selectedInput) {
        console.log('Focused input details:', {
            placeholder: selectedInput.placeholder,
            value: selectedInput.value,
            hasDataAttribute: selectedInput.getAttribute('data-extra-value-input'),
            class: selectedInput.className
        });
    } else {
        console.log('No input is currently focused');
    }
}

window.checkFocusedInput = checkFocusedInput;

/**
 * Fresh test function to bypass caching
 */
function freshExtraValueTest() {
    console.log('🆕 === FRESH EXTRA VALUE TEST ===');
    
    const columnInputs = document.querySelectorAll('input[placeholder="Add Column Name"]');
    const selectorInputs = document.querySelectorAll('input[placeholder="Selector Value"]');
    
    console.log('🆕 Column inputs found:', columnInputs.length);
    console.log('🆕 Selector inputs found:', selectorInputs.length);
    
    if (columnInputs.length > 0) {
        console.log('🆕 Column input 0 value:', `"${columnInputs[0].value}"`);
    }
    
    if (selectorInputs.length > 0) {
        console.log('🆕 Selector input 0 value:', `"${selectorInputs[0].value}"`);
    }
    
    // Try to create array manually
    const testArray = [];
    for (let i = 0; i < Math.min(columnInputs.length, selectorInputs.length); i++) {
        const colVal = columnInputs[i].value.trim();
        const selVal = selectorInputs[i].value.trim();
        
        console.log(`🆕 Pair ${i}: "${colVal}" + "${selVal}"`);
        
        if (colVal && selVal) {
            testArray.push({ column_name: colVal, selector_value: selVal });
            console.log(`🆕 ✅ Added to test array`);
        } else {
            console.log(`🆕 ❌ Not adding - missing values`);
        }
    }
    
    console.log('🆕 Test array result:', testArray);
    console.log('🆕 === END FRESH TEST ===');
    
    return testArray;
}

window.freshExtraValueTest = freshExtraValueTest;

/**
 * Force update extra value array with working logic
 */
function forceUpdateExtraValueArray() {
    console.log('🚀 === FORCE UPDATE EXTRA VALUE ARRAY ===');
    
    const columnInputs = document.querySelectorAll('input[placeholder="Add Column Name"]');
    const selectorInputs = document.querySelectorAll('input[placeholder="Selector Value"]');
    
    console.log('🚀 Column inputs found:', columnInputs.length);
    console.log('🚀 Selector inputs found:', selectorInputs.length);
    
    // Clear the existing array
    extraValueArray = [];
    
    // Create the array using working logic
    for (let i = 0; i < Math.min(columnInputs.length, selectorInputs.length); i++) {
        const colVal = columnInputs[i].value.trim();
        const selVal = selectorInputs[i].value.trim();
        
        console.log(`🚀 Pair ${i}: "${colVal}" + "${selVal}"`);
        
        if (colVal && selVal) {
            extraValueArray.push({ column_name: colVal, selector_value: selVal });
            console.log(`🚀 ✅ Added to extraValueArray`);
        }
    }
    
    console.log('🚀 Final extraValueArray:', extraValueArray);
    
    // Update the table
    updateTable();
    
    console.log('🚀 === FORCE UPDATE COMPLETE ===');
}

window.forceUpdateExtraValueArray = forceUpdateExtraValueArray;

/**
 * Quick debug to check current input values
 */
function checkCurrentInputValues() {
    console.log('🔍 === CHECKING CURRENT INPUT VALUES ===');
    
    const columnInputs = document.querySelectorAll('input[placeholder="Add Column Name"]');
    const selectorInputs = document.querySelectorAll('input[placeholder="Selector Value"]');
    
    console.log('Column inputs found:', columnInputs.length);
    columnInputs.forEach((input, i) => {
        console.log(`Column input ${i}:`, {
            value: `"${input.value}"`,
            length: input.value.length,
            element: input
        });
    });
    
    console.log('Selector inputs found:', selectorInputs.length);
    selectorInputs.forEach((input, i) => {
        console.log(`Selector input ${i}:`, {
            value: `"${input.value}"`,
            length: input.value.length,
            element: input
        });
    });
    
    console.log('Current extraValueArray:', extraValueArray);
    console.log('🔍 === END CHECK ===');
}

window.checkCurrentInputValues = checkCurrentInputValues;

/**
 * Function to get value from HTML using selector
 */
function getValueFromSelector(selector) {
    // Try iframe first
    const iframe = document.getElementById('html-content-iframe');
    if (iframe && iframe.contentDocument && iframe.contentDocument.body) {
        try {
            // Use the universal selector function that handles both CSS and XPath
            const elements = getArticleElementsBySelector(selector, iframe.contentDocument);
            return elements.length > 0 ? elements[0].textContent.trim() : '';
        } catch (error) {
            console.error('Error getting value from iframe selector:', error);
            return '';
        }
    }
    
    // Fallback to div content
    const contentDiv = document.getElementById('html-content-div');
    if (contentDiv) {
        try {
            // Use the universal selector function that handles both CSS and XPath
            const elements = getArticleElementsBySelector(selector, contentDiv);
            return elements.length > 0 ? elements[0].textContent.trim() : '';
        } catch (error) {
            console.error('Error getting value from div selector:', error);
            return '';
        }
    }
    
    return '';
}

/**
 * Updated function to update the table with values from the extraValueArray
 */
function updateTable() {
    const container = document.getElementById('extra_value_tbody_article');
    if (!container) return;
    
    container.innerHTML = '';
    container.className = 'extra-value-cards';

    if (!extraValueArray || extraValueArray.length === 0) {
        container.innerHTML = `
            <div class="text-center text-gray-500 py-8">
                <svg class="w-12 h-12 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <p class="text-sm">No extra values added yet</p>
                <p class="text-xs text-gray-400 mt-1">Click "Content" button, toggle "Add extra value" ON, then add column names and selectors</p>
            </div>
        `;
        return;
    }

    // Create cards for each extra value
    extraValueArray.forEach((entry) => {
        const card = document.createElement('div');
        card.className = 'bg-white rounded-lg border border-l-4 border-l-indigo-500 p-4 mb-4 space-y-3';

        const actualValue = getValueFromSelector(entry.selector_value);

        card.innerHTML = `
            <div class="flex">
                <span class="w-20 text-gray-600 font-medium">Column:</span>
                <span class="text-gray-800">${entry.column_name || 'Unnamed'}</span>
            </div>
            <div class="flex">
                <span class="w-20 text-gray-600 font-medium">Selector:</span>
                <code class="text-sm bg-gray-100 px-2 py-1 rounded">${entry.selector_value}</code>
            </div>
            <div class="flex">
                <span class="w-20 text-gray-600 font-medium">Value:</span>
                <div class="flex-1 bg-gray-50 rounded p-2 text-sm text-gray-800 max-h-20 overflow-y-auto">
                    ${actualValue || '<span class="text-gray-400 italic">No content found</span>'}
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}



/**
 * Update remove content array (from original code)
 */
function updateRemoveContentArray() {
    const removeContentInputs = document.querySelectorAll('#remove-content-container input');

    // Clear the existing array
    removeContentArray = [];

    // Loop through all inputs and append their values to the array
    removeContentInputs.forEach(input => {
        const contentId = input.value.trim();

        // Only add to the array if the input field is filled
        if (contentId) {
            removeContentArray.push(contentId);
        }
    });

    // Log the updated array (for debugging purposes)
    console.log('Updated Remove Content Array:', removeContentArray);
}

/**
 * Update preview content (updated for iframe)
 */
function updatePreviewContent(selectorData) {
    const processedContentDiv = document.getElementById('processed-content-article');
    if (!processedContentDiv) return;

    // Clear previous content
    processedContentDiv.innerHTML = '';

    // Update preview if selector exists
    if (selectorData && selectorData.selector) {
        let htmlContainer = null;
        
        // Try iframe first
        const iframe = document.getElementById('html-content-iframe');
        if (iframe && iframe.contentDocument) {
            htmlContainer = iframe.contentDocument;
        } else {
            // Fallback to div
            const contentDiv = document.getElementById('html-content-div');
            if (contentDiv) {
                htmlContainer = contentDiv;
            }
        }

        if (htmlContainer) {
            try {
                // Use the universal selector function that handles both CSS and XPath
                const selectedElements = getArticleElementsBySelector(selectorData.selector, htmlContainer);
                let hasContent = false;
                
                // Show selector type in console
                const selectorType = isArticleXPathSelector(selectorData.selector) ? 'XPath' : 'CSS';
                console.log('ARTICLE: Preview using', selectorType, 'selector:', selectorData.selector);

        if (selectedElements && selectedElements.length > 0) {
            // Create preview container
            const previewContainer = document.createElement('div');
            previewContainer.className = 'space-y-2';

            // Add each found element to preview
            selectedElements.forEach((element, index) => {
                const value = selectorData.attribute ?
                    element.getAttribute(selectorData.attribute) :
                    element.textContent.trim();

                if (value) {
                    hasContent = true;
                    const valueDiv = document.createElement('div');
                    valueDiv.className = 'p-2 bg-white rounded border';

                    // Add match number if multiple matches found
                    if (selectedElements.length > 1) {
                        valueDiv.innerHTML = `<div class="text-xs text-indigo-600 mb-1">Match ${index + 1} of ${selectedElements.length}</div>`;
                    }

                    // Add the actual content
                    const contentDiv = document.createElement('div');
                    contentDiv.textContent = value;
                    valueDiv.appendChild(contentDiv);

                    previewContainer.appendChild(valueDiv);
                }
            });

            if (hasContent) {
                processedContentDiv.appendChild(previewContainer);
                // Add success message with selector type
                const successMessage = document.createElement('div');
                successMessage.className = 'mt-2 text-sm text-green-600';
                successMessage.textContent = ` ${selectorType} Selector: Found ${selectedElements.length} match${selectedElements.length > 1 ? 'es' : ''}`;
                processedContentDiv.insertBefore(successMessage, previewContainer);
            } else {
                showNoContentMessage(processedContentDiv, ` ${selectorType} Selector: No content found (empty elements)`);
            }
        } else {
            showNoContentMessage(processedContentDiv, ` ${selectorType} Selector: No elements found matching this selector`);
                }
            } catch (error) {
                const selectorTypeMsg = isArticleXPathSelector(selectorData.selector) ? 'XPath' : 'CSS';
                showNoContentMessage(processedContentDiv, `Invalid ${selectorTypeMsg} Selector: ${error.message}`);
            }
        }
    } else {
        showNoContentMessage(processedContentDiv, "Please enter a valid selector");
    }
}

/**
 * Show no content message (from original code)
 */
function showNoContentMessage(container, message) {
    const noContentDiv = document.createElement('div');
    noContentDiv.className = 'p-4 bg-gray-50 rounded border border-gray-200 text-gray-600 text-center';
    noContentDiv.innerHTML = `
        <svg class="w-6 h-6 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <div class="text-sm">${message}</div>
    `;
    container.appendChild(noContentDiv);
}

/**
 * Update selector status (from original code)
 */
function updateSelectorStatus(foundSelectors, input = null) {
    const selectors = ['title', 'tags', 'category', 'author', 'date', 'image', 'content', 'seo'];

    function createStatusElement(isSuccess) {
        if (isSuccess) {
            return `<img src="/static/frontendApp/assets/images/check.png" alt="✔" class="w-5 h-5 inline-block ml-4" style="filter: invert(58%) sepia(14%) saturate(3166%) hue-rotate(100deg) brightness(95%) contrast(80%);" />`;
        } else {
            return 'X';
        }
    }

    if (input) {
        const selectorKey = input.closest('.input-section')?.id;
        if (!selectorKey) return;

        const statusSpan = document.getElementById(`${selectorKey}-status`);
        if (!statusSpan) return;

        const hasValue = input.value.trim() !== '';

        // Update status with image or X and make sure it's visible
        statusSpan.innerHTML = createStatusElement(hasValue);
        statusSpan.classList.remove('hidden');

        // Update color (X will be red, checkmark doesn't need color)
        statusSpan.classList.remove('text-green-500', 'text-red-500');
        if (!hasValue) {
            statusSpan.classList.add('text-red-500');
        }

        return;
    }

    // Bulk update (on initial load)
    selectors.forEach(selector => {
        const statusSpan = document.getElementById(`${selector}-status`);
        if (statusSpan) {
            const isFound = foundSelectors.includes(selector);

            // Always show the status
            statusSpan.classList.remove('hidden');

            // Update status with image or X
            statusSpan.innerHTML = createStatusElement(isFound);

            // Update color (only for X)
            statusSpan.classList.remove('text-green-500', 'text-red-500');
            if (!isFound) {
                statusSpan.classList.add('text-red-500');
            }
        }
    });
}

/**
 * Add click and hover interactivity to HTML elements in iframe
 */
function addHtmlInteractivity() {
    const iframe = document.getElementById('html-content-iframe');
    if (!iframe || !iframe.contentDocument) {
        console.error("HTML iframe or content document not found");
        return;
    }

    const iframeDocument = iframe.contentDocument;

    // Add click event delegation
    iframeDocument.addEventListener('click', (event) => {
        event.preventDefault();
        if (event.target && event.target !== iframeDocument) {
            handleElementClick(event.target);
        }
    });

    // Add hover effects
    iframeDocument.addEventListener('mouseover', (event) => {
        if (event.target && event.target !== iframeDocument) {
            event.target.style.backgroundColor = 'rgba(134, 126, 255, 0.3)';
            event.target.style.cursor = 'pointer';
        }
    });

    iframeDocument.addEventListener('mouseout', (event) => {
        if (event.target && event.target !== iframeDocument && !event.target.classList.contains('selected')) {
            event.target.style.backgroundColor = '';
            event.target.style.cursor = '';
        }
    });
}

/**
 * Add click and hover interactivity to HTML elements in fallback div
 */
function addHtmlInteractivityFallback() {
    const contentDiv = document.getElementById('html-content-div');
    if (!contentDiv) {
        console.error("HTML content div not found");
        return;
    }

    // Add click event delegation
    contentDiv.addEventListener('click', (event) => {
        event.preventDefault();
        if (event.target && event.target !== contentDiv) {
            handleElementClick(event.target);
        }
    });

    // Add hover effects
    contentDiv.addEventListener('mouseover', (event) => {
        if (event.target && event.target !== contentDiv) {
            event.target.style.backgroundColor = 'rgba(134, 126, 255, 0.3)';
            event.target.style.cursor = 'pointer';
        }
    });

    contentDiv.addEventListener('mouseout', (event) => {
        if (event.target && event.target !== contentDiv && !event.target.classList.contains('selected')) {
            event.target.style.backgroundColor = '';
            event.target.style.cursor = '';
        }
    });
}

/**
 * Handle click on HTML elements
 */
function handleElementClick(element) {
    const selector = generateElementSelector(element);
    
    if (selector) {
        // Update visual selection
        updateElementSelection(element);
        
        // Update input field if exists
        updateSelectorInput(selector);
        
        // Update preview content with simple element display (old code style)
        updateProcessedContent(element);
        
        console.log('Selected element with selector:', selector);
    }
}

/**
 * Generate a specific CSS selector for an element
 */
function generateElementSelector(element) {
    if (element.id) {
        return `#${element.id}`;
    }
    
    let selector = element.tagName.toLowerCase();
    
    if (element.className) {
        const classes = element.className.split(' ').filter(cls => cls.trim());
        if (classes.length > 0) {
            selector += '.' + classes.join('.');
        }
    }
    
    // Add nth-child if needed for specificity
    const siblings = Array.from(element.parentElement?.children || [])
        .filter(sibling => sibling.tagName === element.tagName);
    
    if (siblings.length > 1) {
        const index = siblings.indexOf(element) + 1;
        selector += `:nth-child(${index})`;
    }
    
    return selector;
}

/**
 * Update visual selection of elements
 */
function updateElementSelection(element) {
    // Try iframe first
    const iframe = document.getElementById('html-content-iframe');
    if (iframe && iframe.contentDocument) {
        // Remove previous selections in iframe
        iframe.contentDocument.querySelectorAll('.selected').forEach(el => {
            el.classList.remove('selected');
            el.style.backgroundColor = '';
        });
    } else {
        // Fallback to div
        const contentDiv = document.getElementById('html-content-div');
        if (contentDiv) {
            // Remove previous selections in div
            contentDiv.querySelectorAll('.selected').forEach(el => {
                el.classList.remove('selected');
                el.style.backgroundColor = '';
            });
        }
    }

    // Select new element
    element.classList.add('selected');
    element.style.backgroundColor = 'rgba(79, 70, 229, 0.5)';
    
    selectedElement = element;
}

/**
 * Update the selector input field
 */
function updateSelectorInput(selector) {
    const selectorInput = document.querySelector('input[name="selector_value"]');
    if (selectorInput) {
        selectorInput.value = selector;
        selectorInput.dispatchEvent(new Event('input'));
    }
}

/**
 * Initialize the selector interface with default state
 */
function initializeSelectorInterface() {
    // Always initialize interface, even if no selector data
    if (!currentSelectorData || Object.keys(currentSelectorData).length === 0) {
        console.warn('No selector data available from API - showing empty interface.');
        show_toast("warning", "No selector data available from API");
    } else {
        console.log('Available selectors:', Object.keys(currentSelectorData));
    }
    
    // Don't auto-initialize title here - will be done after API success
    
    // Update selector status indicators
    updateSelectorStatusIndicators();
}

/**
 * Initialize default title button highlighting after successful API load
 */
function initializeDefaultTitleButton() {
    console.log('Initializing default title button after API success...');
    
    // First call the JavaScript function to load title content
    if (typeof handleSelectorButtonClick === 'function') {
        handleSelectorButtonClick('title-btn');
    } else if (typeof initializeTitleInput === 'function') {
        initializeTitleInput();
        updateButtonActiveStates('title-btn');
    }
    
    // Then trigger the visual highlighting in HTML
    const titleBtn = document.getElementById('title-btn');
    if (titleBtn) {
        // Trigger the click event to activate the visual highlighting
        titleBtn.click();
        console.log('Title button highlighted and content loaded');
    }
}



/**
 * Check if HTML content is loaded and ready for interaction
 */
function isHtmlContentReady() {
    // Try iframe first
    const iframe = document.getElementById('html-content-iframe');
    if (iframe && iframe.contentDocument && iframe.contentDocument.body && iframe.contentDocument.body.innerHTML.trim() !== '') {
        return true;
    }
    
    // Fallback to div
    const contentDiv = document.getElementById('html-content-div');
    if (contentDiv && contentDiv.innerHTML.trim() !== '') {
        return true;
    }
    
    return false;
}

/**
 * Update button active states - make clicked button active, others inactive
 */
function updateButtonActiveStates(activeButtonId) {
    const selectorButtons = [
        'title-btn', 'tag-btn', 'category-btn', 'author-btn', 
        'date-btn', 'image-btn', 'content-btn', 'seo-btn'
    ];

    selectorButtons.forEach(buttonId => {
        const button = document.getElementById(buttonId);
        if (button) {
            // Reset all buttons to inactive state
            button.classList.remove('bg-indigo-50', 'border-indigo-600', 'text-indigo-700');
            button.classList.add('bg-white', 'text-gray-700', 'border-gray-300');
            
            // Make the clicked button active
            if (buttonId === activeButtonId) {
                button.classList.remove('bg-white', 'text-gray-700', 'border-gray-300');
                button.classList.add('bg-indigo-50', 'text-indigo-700', 'border-indigo-600');
            }
        }
    });
    
    console.log(`Button ${activeButtonId} is now active`);
}

/**
 * Handle selector button clicks
 */
function handleSelectorButtonClick(buttonId) {
    const inputFieldsContainer = document.getElementById('input-fields-container');
    if (!inputFieldsContainer) {
        console.error('Input fields container not found');
        return;
    }

    // Update button active states
    updateButtonActiveStates(buttonId);

    // Clear existing inputs
    inputFieldsContainer.innerHTML = '';

    // Define selector mapping with source_ prefix for API
    const selectorMapping = {
        'title-btn': 'source_title',
        'tag-btn': 'source_tags',
        'category-btn': 'source_categories',
        'author-btn': 'source_author',
        'date-btn': 'source_published_date',
        'image-btn': 'source_featured_image',
        'content-btn': 'source_content',
        'seo-btn': 'seo'
    };

    const selectorKey = selectorMapping[buttonId];
    if (!selectorKey) {
        console.warn('Invalid selector key for button:', buttonId);
        return;
    }

    // Get selector data from current data
    const selectorData = getSelectorData(selectorKey);

    // Render appropriate input type - use original design for content
    if (selectorKey === 'source_content') {
        addContentInputs(inputFieldsContainer, selectorKey, selectorData);
    } else if (selectorKey === 'seo') {
        addStandardInputs(inputFieldsContainer, selectorKey, selectorData);
    } else {
        addStandardInputs(inputFieldsContainer, selectorKey, selectorData);
    }

    // Update preview if selector exists
    if (selectorData?.selector) {
        updatePreviewContent(selectorData);
    }

    // Focus on selector input
    const selectorInput = inputFieldsContainer.querySelector('input[name="selector_value"]');
    if (selectorInput) {
        setTimeout(() => {
            selectorInput.focus();
            selectorInput.select();
        }, 0);
    }
}

/**
 * Get selector data for a given key from API response only
 */
function getSelectorData(selectorKey) {
    // Only use data from API response
    if (currentSelectorData && currentSelectorData[selectorKey]) {
        return {
            selector: currentSelectorData[selectorKey].selector || '',
            attribute: currentSelectorData[selectorKey].attribute || '',
            multiple: currentSelectorData[selectorKey].multiple || false,
            remove_selectors: currentSelectorData[selectorKey].remove_selectors || []
        };
    }

    // Return null if no API data available - no fallback
    return null;
}

/**
 * Render standard input fields
 */
function renderStandardInputs(container, selectorKey, selectorData) {
    const formattedData = formatSelectorData(selectorData);
    const isDataAvailable = selectorData !== null;
    
    // Simple text warning if no data available
    const errorMessage = !isDataAvailable ? 
        `<div class="text-yellow-600 text-sm mt-2">No ${capitalizeFirst(selectorKey)} Selector Available</div>` : '';

    container.innerHTML = `
        <div id="${selectorKey}" class="w-full md:w-1/2 input-section">
            <label class="block font-semibold text-gray-700 mb-2">
                ${capitalizeFirst(selectorKey)}
            </label>
            <div class="relative w-full md:w-1/2">
                <input type="text" 
                    placeholder="${isDataAvailable ? 'CSS selector from API' : 'Enter CSS selector manually'}"
                    name="selector_value" 
                    value="${formattedData.css_selector}" 
                    class="w-full p-2 pr-12 border rounded-lg">
                <button type="button" 
                    class="search-icon absolute inset-y-0 right-0 flex items-center px-3 bg-indigo-100 hover:bg-indigo-200 rounded-r-lg border-l transition-colors">
                    <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                </button>
            </div>
            ${errorMessage}
            
            <div class="flex items-center mt-2 border md:w-1/2 p-2 w-full rounded-lg">
                <input type="checkbox" 
                    id="multiple" 
                    name="is_multiple" 
                    class="mr-2" 
                    ${formattedData.multiple ? 'checked' : ''}>
                <label for="multiple">Multiple Elements</label>
            </div>

            <div class="flex items-center mt-2 border md:w-1/2 p-2 w-full rounded-lg">
                <div class="flex items-center border p-2 rounded-lg w-full">
                    <input type="checkbox" 
                        id="attribute" 
                        name="is_attribute" 
                        class="mr-2 p-2 border rounded-lg" 
                        ${formattedData.attribute ? 'checked' : ''}>
                    <label for="attribute">Attribute</label>
                </div>
                <input type="text" 
                    name="attribute_value" 
                    placeholder="SRC, HREF" 
                    class="w-full p-2 border rounded-lg" 
                    value="${formattedData.attribute || ''}">
            </div>

            <input type="hidden" name="selector_key" value="${selectorKey}">
        </div>
    `;

    // Add event listeners
    addStandardInputEventListeners(container);
}

/**
 * Render content-specific inputs with advanced options
 */
function renderContentInputs(container, selectorKey, selectorData) {
    const formattedData = formatSelectorData(selectorData);
    const isDataAvailable = selectorData !== null;

    // Simple text warning if no data available  
    const errorMessage = !isDataAvailable ? 
        `<div class="text-yellow-600 text-sm mt-2">No Content Selector Available</div>` : '';

    container.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div id="add-content" class="input-section">
                <label class="block font-semibold text-gray-700 mb-3">Add Content Selector</label>
                
                <div class="space-y-4">
                    <div class="relative">
                        <input type="text" 
                            placeholder="${isDataAvailable ? 'Content selector from API' : 'Enter content selector manually'}" 
                            name="selector_value" 
                            value="${formattedData.css_selector}" 
                            class="w-full p-3 pr-12 border rounded-lg focus:ring-2 focus:ring-indigo-500">
                        <button type="button" class="search-icon absolute inset-y-0 right-0 flex items-center px-3 bg-indigo-100 hover:bg-indigo-200 rounded-r-lg border-l transition-colors">
                            <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                            </svg>
                        </button>
                    </div>
                    ${errorMessage}

                    <div class="flex items-center space-x-4">
                        <label class="flex items-center">
                            <input type="checkbox" 
                                id="multiple" 
                                name="is_multiple" 
                                class="mr-2" 
                                ${formattedData.multiple ? 'checked' : ''}>
                            <span>Multiple Elements</span>
                        </label>
                    </div>

                    <div class="flex items-center space-x-2">
                        <label class="flex items-center">
                            <input type="checkbox" 
                                id="attribute" 
                                name="is_attribute" 
                                class="mr-2" 
                                ${formattedData.attribute ? 'checked' : ''}>
                            <span>Use Attribute</span>
                        </label>
                        <input type="text" 
                            name="attribute_value" 
                            placeholder="Attribute name" 
                            class="flex-1 p-2 border rounded-lg" 
                            value="${formattedData.attribute || ''}">
                    </div>

                                <!-- Add Extra Value Toggle Section -->
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; border: 1px solid #d1d5db; border-radius: 8px; width: 100%; max-width: 50%;">
                <label style="color: #374151;">Add extra value</label>
                <label style="position: relative; display: inline-flex; align-items: center; cursor: pointer;">
                    <input type="checkbox" id="extra-value-toggle" style="display: none;">
                    <div style="width: 44px; height: 24px; background-color: #d1d5db; border-radius: 12px; position: relative; transition: all 0.3s ease;" class="toggle-switch">
                        <div style="width: 20px; height: 20px; background-color: white; border-radius: 50%; position: absolute; top: 2px; left: 2px; transition: all 0.3s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.2);" class="toggle-dot"></div>
                    </div>
                </label>
            </div>

            <div id="extra-values-container" class="mt-4"></div>
                </div>

                <input type="hidden" name="selector_key" value="${selectorKey}">
            </div>

            <div id="remove-content" class="input-section">
                <label class="block font-semibold text-gray-700 mb-3">Remove Content Selectors</label>
                
                <div class="space-y-4">
                    <div id="remove-content-container" class="space-y-2">
                        <!-- Dynamic remove content inputs -->
                    </div>

                    <!-- Add Extra Value Toggle Section For Remove Content-->
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; border: 1px solid #d1d5db; border-radius: 8px; width: 100%; max-width: 50%; margin-top: 8px;">
                        <label style="color: #374151;">Add extra value</label>
                        <label style="position: relative; display: inline-flex; align-items: center; cursor: pointer;">
                            <input type="checkbox" id="remove-extra-value-toggle" style="display: none;">
                            <div style="width: 44px; height: 24px; background-color: #d1d5db; border-radius: 12px; position: relative; transition: all 0.3s ease;" class="toggle-switch">
                                <div style="width: 20px; height: 20px; background-color: white; border-radius: 50%; position: absolute; top: 2px; left: 2px; transition: all 0.3s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.2);" class="toggle-dot"></div>
                            </div>
                        </label>
                    </div>

                    <div id="remove-content-checkboxes-container" class="mt-4"></div>
                </div>
            </div>
        </div>
    `;

    // Initialize remove content inputs
    initializeRemoveContentInputs(formattedData.remove_selectors);
    
    // Add event listeners
    addContentInputEventListeners();
}

/**
 * Render SEO-specific inputs
 */
function renderSeoInputs(container, selectorKey, selectorData) {
    // SEO is configuration-based, not selector-based, so we always show it
    container.innerHTML = `
        <div id="seo" class="w-full md:w-1/2 input-section">
            <label class="block font-semibold text-gray-700 mb-3">SEO Configuration</label>
            
            <div class="space-y-3">
                <label class="flex items-center p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                    <input type="checkbox" id="set_metatitle" name="set_metatitle" class="mr-3">
                    <div>
                        <div class="font-medium">Meta Title</div>
                        <div class="text-sm text-gray-600">Generate meta title from content</div>
                    </div>
                </label>

                <label class="flex items-center p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                    <input type="checkbox" id="set_metakeywords" name="set_metakeywords" class="mr-3">
                    <div>
                        <div class="font-medium">Meta Keywords</div>
                        <div class="text-sm text-gray-600">Extract and set meta keywords</div>
                    </div>
                </label>

                <label class="flex items-center p-3 border rounded-lg hover:bg-gray-50 cursor-pointer">
                    <input type="checkbox" id="set_desc" name="set_desc" class="mr-3">
                    <div>
                        <div class="font-medium">Meta Description</div>
                        <div class="text-sm text-gray-600">Generate meta description from content</div>
                    </div>
                </label>
            </div>

            <input type="hidden" name="selector_key" value="${selectorKey}">
        </div>
    `;
}

/**
 * Update processed content (simple old code style)
 */
function updateProcessedContent(tag) {
    const processedContentDiv = document.getElementById('processed-content-article');
    
    if (!processedContentDiv) {
        console.error("Processed content div not found");
        return;
    }
    
    console.log(processedContentDiv, 'processedContentDiv')
    // Clone the tag to remove inline styles before displaying it
    let clonedTag = tag.cloneNode(true);
    clonedTag.style.backgroundColor = ''; // Remove background color
    console.log(clonedTag, 'clonedTag')
    processedContentDiv.innerHTML = clonedTag.outerHTML;
}

/**
 * Add tag interactivity (updated for iframe)
 */
function addTagInteractivity() {
    // Try iframe first
    const iframe = document.getElementById('html-content-iframe');
    if (iframe && iframe.contentDocument) {
        console.log('Setting up interactivity for iframe');
        setupHtmlInteractivity(iframe.contentDocument);
        initializeTitleInput();
        return;
    }

    // Fallback to div
    const contentDiv = document.getElementById('html-content-div');
    if (contentDiv) {
        console.log('Setting up interactivity for div');
        setupHtmlInteractivity(contentDiv);
        initializeTitleInput();
        return;
    }

    console.error("Neither iframe nor content div found");
}

/**
 * Setup HTML interactivity for iframe or div
 */
function setupHtmlInteractivity(htmlContent) {
    // Use event delegation for better performance
    htmlContent.addEventListener('click', (e) => {
        // Allow any tag to be selected (p, div, a, img, etc.)
        if (e.target && e.target !== htmlContent) {
            e.preventDefault(); // Prevent default action for any tag

            // Get the most specific selector for the clicked element
            const selector = getSpecificSelector(e.target);

            if (selector) {
                // Toggle selection (select/deselect the clicked tag)
                toggleTagSelection(e.target);

                console.log('Selected element with selector:', selector);

                // Determine which input to update based on placeholder or data attribute
                let targetInput = null;
                
                // First check if we have a specific extra value input focused
                if (selectedInput && selectedInput.getAttribute('data-extra-value-input') === 'true') {
                    targetInput = selectedInput;
                    console.log('Updating extra value input (via data attribute) with selector:', selector);
                } 
                // If no specific input, check if focused input is a selector value input by placeholder
                else if (selectedInput && selectedInput.placeholder === 'Selector Value') {
                    targetInput = selectedInput;
                    console.log('Updating selector value input (via placeholder) with selector:', selector);
                }
                // Fallback to main selector input
                else {
                    targetInput = document.querySelector('input[name="selector_value"]');
                    console.log('Updating main selector input with selector:', selector);
                }
                
                // Update the target input
                if (targetInput) {
                    console.log('Setting value on input:', targetInput);
                    console.log('Value before setting:', targetInput.value);
                    targetInput.value = selector;
                    console.log('Value after setting:', targetInput.value);
                    targetInput.dispatchEvent(new Event('input'));
                    
                    // If it's an extra value input, update the table
                    if (targetInput.placeholder === 'Selector Value' || targetInput.getAttribute('data-extra-value-input') === 'true') {
                        console.log('Triggering extra value array update...');
                        
                        // Add a small delay to ensure the value is properly set in DOM
                        setTimeout(() => {
                            console.log('Delayed check - Value in input now:', targetInput.value);
                            // Use the fixed main function
                            updateExtraValueArray();
                        }, 10);
                    }
                } else {
                    console.log(' No target input found for selector:', selector);
                }
            }
        }
    });

    // Optional: Add hover effect to show where the user is pointing
    htmlContent.addEventListener('mouseover', (e) => {
        if (e.target && e.target !== htmlContent) {
            e.target.style.backgroundColor = 'rgb(134, 126, 255)';  // Light highlight on hover
        }
    });

    // Remove hover effect when mouse leaves the tag
    htmlContent.addEventListener('mouseout', (e) => {
        if (e.target && e.target !== htmlContent) {
            e.target.style.backgroundColor = '';  // Reset background color when mouse leaves
        }
    });
}

/**
 * Toggle tag selection (updated for iframe)
 */
function toggleTagSelection(tag) {
    let htmlContainer = null;

    // Try iframe first
    const iframe = document.getElementById('html-content-iframe');
    if (iframe && iframe.contentDocument) {
        htmlContainer = iframe.contentDocument;
    } else {
        // Fallback to div
        const contentDiv = document.getElementById('html-content-div');
        if (contentDiv) {
            htmlContainer = contentDiv;
        }
    }

    if (!htmlContainer) {
        console.error("HTML container not found");
        return;
    }

    // Remove selection from any previously selected tags
    htmlContainer.querySelectorAll('.selected').forEach(selectedTag => {
        selectedTag.classList.remove('selected');
        selectedTag.style.backgroundColor = ''; // Reset background
    });

    // Select the new tag
    tag.classList.add('selected');
    tag.style.backgroundColor = 'rgb(79, 70, 229)'; // Highlight selected tag

    // Store the selected element
    selectedElement = tag;

    // Update the preview content (simple style)
    updateProcessedContent(tag);
}

/**
 * Get specific selector (from old code)
 */
function getSpecificSelector(element) {
    if (element.id) {
        return `#${element.id}`;
    }
    
    let selector = element.tagName.toLowerCase();
    
    if (element.className) {
        const classes = element.className.split(' ').filter(cls => cls.trim());
        if (classes.length > 0) {
            selector += '.' + classes.join('.');
        }
    }
    
    // Add nth-child if needed for specificity
    const siblings = Array.from(element.parentElement?.children || [])
        .filter(sibling => sibling.tagName === element.tagName);
    
    if (siblings.length > 1) {
        const index = siblings.indexOf(element) + 1;
        selector += `:nth-child(${index})`;
    }
    
    return selector;
}

/**
 * Update preview display based on selector (updated for iframe)
 */
function updatePreviewDisplay(selector, attribute = null) {
    const processedContentDiv = document.getElementById('processed-content-article');
    if (!processedContentDiv) return;

    processedContentDiv.innerHTML = '';

    if (!selector) {
        showNoContentMessage(processedContentDiv, "No selector provided");
        return;
    }

    let htmlContainer = null;
        
        // Try iframe first
        const iframe = document.getElementById('html-content-iframe');
        if (iframe && iframe.contentDocument) {
        htmlContainer = iframe.contentDocument;
        } else {
            // Fallback to div
            const contentDiv = document.getElementById('html-content-div');
            if (contentDiv) {
            htmlContainer = contentDiv;
        }
    }

    if (!htmlContainer) {
        showNoContentMessage(processedContentDiv, "HTML content not loaded. Please load content first.");
        return;
    }

    try {
        // Use the universal selector function that handles both CSS and XPath
        const elements = getArticleElementsBySelector(selector, htmlContainer);
        
        // Show selector type in console
        const selectorType = isArticleXPathSelector(selector) ? 'XPath' : 'CSS';
        console.log('ARTICLE: Testing', selectorType, 'selector:', selector);
        
        if (!elements || elements.length === 0) {
            showNoContentMessage(processedContentDiv, ` ${selectorType} Selector: No elements found with this selector`);
            return;
        }

        // Use simple approach - show first element directly (old code style)
        if (elements.length > 0) {
            const firstElement = elements[0];
            let clonedElement = firstElement.cloneNode(true);
            clonedElement.style.backgroundColor = ''; // Remove background color
            processedContentDiv.innerHTML = clonedElement.outerHTML;
        }
        
    } catch (error) {
        const selectorTypeMsg = isArticleXPathSelector(selector) ? 'XPath' : 'CSS';
        showNoContentMessage(processedContentDiv, `Invalid ${selectorTypeMsg} Selector: ${error.message}`);
    }
}

/**
 * Render preview content for found elements
 */
function renderPreviewContent(container, elements, attribute) {
    const previewContainer = document.createElement('div');
    previewContainer.className = 'space-y-3';

    // Add success header
    const header = document.createElement('div');
    header.className = 'flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded-lg';
    header.innerHTML = `
        <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <span class="text-green-800 font-medium">Found ${elements.length} element${elements.length > 1 ? 's' : ''}</span>
        </div>
    `;
    previewContainer.appendChild(header);

    // Add preview for each element
    elements.forEach((element, index) => {
        const value = attribute ? 
            element.getAttribute(attribute) : 
            element.textContent.trim();

        if (value) {
            const elementPreview = document.createElement('div');
            elementPreview.className = 'p-3 bg-white border rounded-lg';
            
            if (elements.length > 1) {
                const indexLabel = document.createElement('div');
                indexLabel.className = 'text-xs text-indigo-600 font-medium mb-2';
                indexLabel.textContent = `Element ${index + 1} of ${elements.length}`;
                elementPreview.appendChild(indexLabel);
            }

            const content = document.createElement('div');
            content.className = 'text-gray-800 break-words';
            content.textContent = value.length > 200 ? value.substring(0, 200) + '...' : value;
            elementPreview.appendChild(content);

            previewContainer.appendChild(elementPreview);
        }
    });

    container.appendChild(previewContainer);
}

/**
 * Show preview message with different types
 */
function showPreviewMessage(container, message, type = "info") {
    const colors = {
        info: { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-800', icon: 'text-blue-600' },
        warning: { bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-800', icon: 'text-yellow-600' },
        error: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-800', icon: 'text-red-600' }
    };

    const color = colors[type] || colors.info;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `p-4 ${color.bg} ${color.border} border rounded-lg`;
    messageDiv.innerHTML = `
        <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 ${color.icon}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="${color.text}">${message}</span>
        </div>
    `;
    
    container.appendChild(messageDiv);
}

/**
 * Update selector status indicators based on API data only
 */
function updateSelectorStatusIndicators() {
    if (!currentSelectorData) return;

    // Only check for selectors that are actually available from the API
    const availableSelectors = Object.keys(currentSelectorData);
    console.log('Updating status for API selectors:', availableSelectors);
    
    // Map display keys to API keys with source_ prefix
    const selectorKeyMapping = {
        'title': 'source_title',
        'tag': 'source_tags', 
        'category': 'source_categories',
        'author': 'source_author',
        'date': 'source_published_date',
        'image': 'source_featured_image',
        'content': 'source_content',
        'seo': 'seo'
    };
    
    Object.keys(selectorKeyMapping).forEach(displayKey => {
        const apiKey = selectorKeyMapping[displayKey];
        const statusElement = document.getElementById(`${displayKey}-status`);
        if (statusElement) {
            const hasSelector = currentSelectorData[apiKey]?.selector;
            updateStatusElement(statusElement, hasSelector);
        }
    });
}

/**
 * Update individual status element
 */
function updateStatusElement(element, hasValue) {
    element.classList.remove('hidden');
    
    if (hasValue) {
        element.innerHTML = '✓';
        element.className = element.className.replace(/text-\w+-\d+/g, '') + ' text-green-600';
    } else {
        element.innerHTML = 'X';
        element.className = element.className.replace(/text-\w+-\d+/g, '') + ' text-red-600';
    }
}

// Utility functions
function formatSelectorData(selectorData) {
    return {
        css_selector: selectorData?.selector || '',
        attribute: selectorData?.attribute || '',
        multiple: selectorData?.multiple || false,
        remove_selectors: selectorData?.remove_selectors || []
    };
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function forceToggleUpdate(toggleInput) {
    // Force update toggle appearance using simple design
    const toggleContainer = toggleInput.closest('label');
    const toggleSwitch = toggleContainer?.querySelector('.toggle-switch');
    const toggleDot = toggleContainer?.querySelector('.toggle-dot');
    
    if (!toggleSwitch || !toggleDot) return;
    
    if (toggleInput.checked) {
        // ON state: blue background, dot moves right
        toggleSwitch.style.backgroundColor = '#3b82f6'; // blue
        toggleDot.style.left = '22px'; // move right
    } else {
        // OFF state: gray background, dot moves left  
        toggleSwitch.style.backgroundColor = '#d1d5db'; // gray
        toggleDot.style.left = '2px'; // move left
    }
}

function focusSelectorInput(container) {
    const selectorInput = container.querySelector('input[name="selector_value"]');
    if (selectorInput) {
        setTimeout(() => {
            selectorInput.focus();
            selectorInput.select();
        }, 100);
    }
}

// Event listener functions
function addStandardInputEventListeners(container) {
    const searchIcon = container.querySelector('.search-icon');
    if (searchIcon) {
        searchIcon.addEventListener('click', function() {
            const input = container.querySelector('input[name="selector_value"]');
            const attributeInput = container.querySelector('input[name="attribute_value"]');
            const isAttribute = container.querySelector('input[name="is_attribute"]')?.checked;

            if (input?.value) {
                // Create selectorData object for proper preview
                const selectorData = {
                    selector: input.value,
                    attribute: isAttribute ? attributeInput?.value : null
                };
                updatePreviewContent(selectorData);
            }
        });
    }

    const selectorInput = container.querySelector('input[name="selector_value"]');
    if (selectorInput) {
        selectorInput.addEventListener('input', function() {
            // Optional: Real-time preview update
            // updatePreviewDisplay(this.value);
        });
    }
}

function addContentInputEventListeners() {
    // Extra value toggle for ADD section (left section)
    const extraToggle = document.getElementById('extra-value-toggle');
    if (extraToggle) {
        extraToggle.addEventListener('change', function() {
            const container = document.getElementById('extra-values-container');
            
            // Force visual update for old toggle design
            forceToggleUpdate(this);
            
            if (this.checked) {
                // Show inputs for ADD extra value section only
                addExtraValueInput();
            } else {
                // Hide inputs for ADD extra value section only
                container.innerHTML = '';
                extraValueArray = [];
            }
        });
        
        // Initialize toggle appearance
        forceToggleUpdate(extraToggle);
    }

    // Remove content toggle for REMOVE section (right section)
    const removeToggle = document.getElementById('remove-extra-value-toggle');
    if (removeToggle) {
        removeToggle.addEventListener('change', function() {
            const container = document.getElementById('remove-content-checkboxes-container');
            
            // Force visual update for old toggle design
            forceToggleUpdate(this);
            
            if (this.checked) {
                // Show inputs for REMOVE extra value section only
                addRemoveContentCheckboxes(container);
            } else {
                // Hide inputs for REMOVE extra value section only
                container.innerHTML = '';
            }
        });
        
        // Initialize toggle appearance
        forceToggleUpdate(removeToggle);
    }

    // Search icon for content
    const searchIcon = document.querySelector('#add-content .search-icon');
    if (searchIcon) {
        searchIcon.addEventListener('click', function() {
            const input = document.querySelector('input[name="selector_value"]');
            const attributeInput = document.querySelector('input[name="attribute_value"]');
            const isAttribute = document.querySelector('input[name="is_attribute"]')?.checked;

            if (input?.value) {
                // Create selectorData object for proper preview
                const selectorData = {
                    selector: input.value,
                    attribute: isAttribute ? attributeInput?.value : null
                };
                updatePreviewContent(selectorData);
            }
        });
    }
}

function initializeRemoveContentInputs(removeSelectors = []) {
    const container = document.getElementById('remove-content-container');
    if (!container) {
        console.error('Remove content container not found!');
        return;
    }

    console.log('Initializing remove content inputs...');
    container.innerHTML = '';
    
    if (removeSelectors.length > 0) {
        console.log('Adding inputs for selectors:', removeSelectors);
        removeSelectors.forEach(selector => {
            const inputElement = createRemoveContentInput(selector);
            container.appendChild(inputElement);
        });
        removeContentArray = [...removeSelectors];
    } else {
        console.log('Adding default empty input');
        const inputElement = createRemoveContentInput();
        container.appendChild(inputElement);
    }
    
    // Debug: check what's actually in the container
    console.log('Container after initialization:', container.innerHTML);
    console.log('Container children count:', container.children.length);
    
    // Force a small delay to check if buttons are visible
    setTimeout(() => {
        const buttons = container.querySelectorAll('button');
        console.log('Buttons found in container:', buttons.length);
        buttons.forEach((btn, index) => {
            console.log(`Button ${index}:`, btn.textContent, btn.className);
        });
    }, 100);
}



function addExtraValueInput() {
    const container = document.getElementById('extra-values-container');
    if (!container) return;

    const inputGroup = document.createElement('div');
    inputGroup.className = 'flex items-center space-x-2 mb-2';
    inputGroup.innerHTML = `
        <input type="text" 
            placeholder="Column name" 
            class="flex-1 p-2 border rounded-lg column-name">
        <input type="text" 
            placeholder="CSS selector" 
            class="flex-1 p-2 border rounded-lg selector-value">
        <button type="button" 
            class="add-btn px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">+</button>
        <button type="button" 
            class="remove-btn px-3 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500">−</button>
    `;

    // Add event listeners
    const addBtn = inputGroup.querySelector('.add-btn');
    const removeBtn = inputGroup.querySelector('.remove-btn');
    const inputs = inputGroup.querySelectorAll('input');

    addBtn.addEventListener('click', () => addExtraValueInput());
    removeBtn.addEventListener('click', () => {
        inputGroup.remove();
        updateExtraValueArray();
    });
    
    inputs.forEach(input => {
        input.addEventListener('input', updateExtraValueArray);
    });

    container.appendChild(inputGroup);
}

function addRemovalOptionsCheckboxes() {
    const container = document.getElementById('remove-content-checkboxes-container');
    if (!container) return;

    const options = [
        { name: 'remove_blocker_images', label: 'Remove Blocker Images' },
        { name: 'remove_google_analytics', label: 'Remove Google Analytics' },
        { name: 'remove_google_advanced', label: 'Remove Google Advanced' },
        { name: 'remove_script', label: 'Remove Scripts' },
        { name: 'remove_404_internal_links', label: 'Remove 404 Internal Links' }
    ];

    options.forEach(option => {
        const checkboxDiv = document.createElement('div');
        checkboxDiv.className = 'flex items-center p-2 border rounded-lg hover:bg-gray-50';
        checkboxDiv.innerHTML = `
            <input type="checkbox" 
                id="${option.name}" 
                name="${option.name}" 
                class="mr-3">
            <label for="${option.name}" class="cursor-pointer">${option.label}</label>
        `;
        
        container.appendChild(checkboxDiv);
    });
}

function updateRemoveContentArray() {
    const inputs = document.querySelectorAll('#remove-content-container input');
    removeContentArray = Array.from(inputs)
        .map(input => input.value.trim())
        .filter(value => value);
    
    console.log('Updated remove content array:', removeContentArray);
}

function updateExtraValueArray() {
    const columnInputs = document.querySelectorAll('input[placeholder="Add Column Name"]');
    const selectorInputs = document.querySelectorAll('input[placeholder="Selector Value"]');
    
    extraValueArray = [];
    
    for (let i = 0; i < Math.min(columnInputs.length, selectorInputs.length); i++) {
        const colVal = columnInputs[i].value.trim();
        const selVal = selectorInputs[i].value.trim();
        
        if (colVal && selVal) {
            extraValueArray.push({ column_name: colVal, selector_value: selVal });
        }
    }
    
    updateTable();
}

/**
 * Save selector configuration via API
 */
async function saveSelectorConfiguration() {
    // Validate required data
    if (!isHtmlContentReady()) {
        show_toast("error", "Please load HTML content first before saving selectors.");
        return;
    }

    const selectorValue = document.querySelector('[name="selector_value"]')?.value;
    const selectorKey = document.querySelector('[name="selector_key"]')?.value;
    
    if (!selectorValue || !selectorKey) {
        show_toast("error", "Please select a valid selector and key before saving.");
        return;
    }

    const attributeValue = document.querySelector('[name="attribute_value"]')?.value;
    const isMultiple = document.querySelector('[name="is_multiple"]')?.checked || false;
    const isAttribute = document.querySelector('[name="is_attribute"]')?.checked || false;

    // SEO options
    const setMetatitle = document.querySelector('[name="set_metatitle"]')?.checked || false;
    const setMetakeywords = document.querySelector('[name="set_metakeywords"]')?.checked || false;
    const setDesc = document.querySelector('[name="set_desc"]')?.checked || false;

    // Get selected removal options
    const selectedRemoveOptions = Array.from(
        document.querySelectorAll('#remove-content-checkboxes-container input[type="checkbox"]:checked')
    ).map(checkbox => checkbox.name);

    // Update arrays
    updateRemoveContentArray();
    updateExtraValueArray();

    // Prepare form data
    const formData = new FormData();
    formData.append("selector_value", selectorValue || '');
    formData.append("selector_key", selectorKey || '');
    formData.append("attribute_value", attributeValue || '');
    formData.append("is_multiple", isMultiple);
    formData.append("is_attribute", isAttribute);
    
    // Domain and user data
    formData.append("domain_id", sessionStorage.getItem('domain_id') || '');
    formData.append("user_detail_id", sessionStorage.getItem('user_detail_id') || '');
    
    // Use the competitor_domain_mapping_id from the loaded data
    const competitorId = window.competitor_domain_mapping_id || 
                        localStorage.getItem('competitor_domain_mapping_slug_id') || '';
    formData.append("competitor_domain_mapping_id", competitorId);

    // SEO options
    if (setMetatitle) formData.append("set_metatitle", true);
    if (setMetakeywords) formData.append("set_metakeywords", true);
    if (setDesc) formData.append("set_desc", true);

    // Arrays as JSON
    formData.append("remove_checkboxes", JSON.stringify(selectedRemoveOptions));
    formData.append("add_extra_value", JSON.stringify(extraValueArray));
    formData.append("remove_content_ids", JSON.stringify(removeContentArray));

    try {
        const responseData = await add_api(add_selector_url, formData, null);
        console.log('Selector saved successfully:', responseData);
        
        if (responseData.status === 'success') {
            show_toast("success", "Selector configuration saved successfully");
        } else {
            show_toast("error", responseData.message || "Failed to save configuration");
        }
        
        return responseData;
    } catch (error) {
        console.error('Error saving selector:', error);
        show_toast("error", "Network error. Please try again.");
        throw error;
    }
}

/**
 * Test a CSS selector against the loaded HTML content
 */
function testSelector(selector, attribute = null) {
    if (!isHtmlContentReady()) {
        console.warn('HTML content not ready for testing');
        return null;
    }

    const shadowRoot = document.getElementById('html-container-article').shadowRoot;
    try {
        // Use the universal selector function that handles both CSS and XPath
        const elements = getArticleElementsBySelector(selector, shadowRoot);
        const results = elements.map(el => {
            return attribute ? el.getAttribute(attribute) : el.textContent.trim();
        }).filter(content => content);
        
        // Show selector type in console
        const selectorType = isArticleXPathSelector(selector) ? 'XPath' : 'CSS';
        console.log(`API ${selectorType} Selector "${selector}" found ${elements.length} elements with ${results.length} valid results:`, results);
        return { elements: elements.length, validResults: results };
    } catch (error) {
        const selectorTypeMsg = isArticleXPathSelector(selector) ? 'XPath' : 'CSS';
        console.error(`Error testing API ${selectorTypeMsg} selector "${selector}":`, error);
        return null;
    }
}

// Initialize event listeners
function initializeEventListeners() {
    // Selector button event listeners
    const selectorButtons = [
        'title-btn', 'tag-btn', 'category-btn', 'author-btn', 
        'date-btn', 'image-btn', 'content-btn', 'seo-btn'
    ];

    selectorButtons.forEach(buttonId => {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener('click', () => handleSelectorButtonClick(buttonId));
        }
    });

    // Focus tracking for inputs
    document.addEventListener('focusin', (event) => {
        if (event.target.tagName === 'INPUT') {
            selectedInput = event.target;
            console.log('Input focused:', event.target.placeholder || event.target.name, 'Extra value input:', event.target.getAttribute('data-extra-value-input'));
        }
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeEventListeners);
} else {
    initializeEventListeners();
}

/**
 * Function to be called when step 4 is shown to ensure proper initialization
 */
function initializeStep4() {
    console.log('Initializing Step 4...');
    
    // Load HTML content first
    get_html_content().then(() => {
        console.log('HTML content loaded, initializing interface...');
        // Small delay to ensure everything is rendered
        setTimeout(() => {
            // Trigger title button click to highlight it and show title input
            if (typeof handleSelectorButtonClick === 'function') {
                handleSelectorButtonClick('title-btn');
            }
        }, 100);
    }).catch(error => {
        console.error('Error loading HTML content:', error);
        // Still initialize interface even if HTML loading fails
        setTimeout(() => {
            if (typeof handleSelectorButtonClick === 'function') {
                handleSelectorButtonClick('title-btn');
            }
        }, 100);
    });
}

// Expose the function globally so it can be called from HTML
window.initializeStep4 = initializeStep4;

// Legacy function for backward compatibility
function add_selector_api() {
    return add_article_url_selector_api();
}

// Expose key functions to global scope for external use if needed
window.checkArticleFunctions = {
    saveSelectorConfiguration,
    testSelector,
    get_html_content,
    handleSelectorButtonClick,
    isHtmlContentReady: () => isHtmlContentReady(),
    // Legacy support - use correct function
    add_selector_api: add_article_url_selector_api,
    add_article_url_selector_api: add_article_url_selector_api
};

/**
 * Save selector data to article_url_selector API
 */
async function add_article_url_selector_api() {
    try {
        // Get current selector configuration
        const selector_value = document.querySelector('[name="selector_value"]')?.value;
        const selector_key = document.querySelector('[name="selector_key"]')?.value;
        const attribute_value = document.querySelector('[name="attribute_value"]')?.value;
        const is_multiple = document.querySelector('[name="is_multiple"]')?.checked || false;
        const is_attribute = document.querySelector('[name="is_attribute"]')?.checked || false;

        if (!selector_value || !selector_key) {
            show_toast("error", "Please select a valid selector and key before saving.");
            return;
        }

        // Update arrays
        updateRemoveContentArray();
        updateExtraValueArray();

        // Get required IDs from current context
        const competitor_article_url_slug_id = localStorage.getItem('competitor_article_url_slug_id');
        const competitor_selected_url_slug_id = localStorage.getItem('competitor_selected_url_slug_id');
        const user_detail_id = sessionStorage.getItem('user_detail_id');

        if (!competitor_article_url_slug_id || !competitor_selected_url_slug_id) {
            show_toast("error", "Missing required article URL or selected URL IDs.");
            return;
        }

        // Use selector_key directly as it already has the correct source_ prefix
        // that matches the Django model field names
        const validSelectorKeys = [
            'source_title',
            'source_content', 
            'source_featured_image',
            'source_author',
            'source_published_date',
            'source_categories',
            'source_tags',
            'source_meta_title',
            'source_meta_description',
            'source_meta_keywords',
            'source_outline',
            'source_internal_links',
            'source_external_links',
            'source_faqs'
        ];

        if (!validSelectorKeys.includes(selector_key)) {
            show_toast("error", `Invalid selector key: ${selector_key}`);
            return;
        }

        const apiField = selector_key; // Use selector_key directly

        // Build selector data structure exactly as required
        const selectorData = {
            selector: selector_value,
            attribute: (is_attribute && attribute_value) ? attribute_value : "",
            multiple: is_multiple,
            remove_selectors: removeContentArray.length > 0 ? removeContentArray : []
        };

        // Add extra values if they exist
        if (extraValueArray.length > 0) {
            selectorData.extra_values = extraValueArray;
        }

        // Build simplified FormData with only essential fields
        let data = new FormData();
        
        // Required ID fields
        data.append("competitor_article_url_slug_id", competitor_article_url_slug_id);
        data.append("competitor_selected_url_slug_id", competitor_selected_url_slug_id);
        data.append("user_detail_id", user_detail_id || "");
        
        // Verification fields
        data.append("is_verified", false);
        data.append("verified_by", user_detail_id || "");
        
        // Add the selector field data as JSON string (this is the main data)
        data.append(apiField, JSON.stringify(selectorData));
        
        console.log(`Setting field '${apiField}' with data:`, selectorData);

        // Debug: Log all FormData entries
        console.log('API FormData entries:');
        for (let [key, value] of data.entries()) {
            console.log(`${key}: ${value}`);
        }

        // Send data to API
        const response_data = await add_api(add_article_url_selector_url, data, null);

        console.log("API Response - Article URL Selector:", response_data);

        


    } catch (error) {
        console.error('Error saving selector:', error);
        
    }
}

/**
 * Update all button status indicators based on available selector data
 */
function updateAllButtonStatus() {
    const buttonMapping = {
        'title-btn': 'source_title',
        'tag-btn': 'source_tags', 
        'category-btn': 'source_categories',
        'author-btn': 'source_author',
        'date-btn': 'source_published_date',
        'image-btn': 'source_featured_image',
        'content-btn': 'source_content',
        'seo-btn': 'seo'
    };

    Object.keys(buttonMapping).forEach(buttonId => {
        const selectorKey = buttonMapping[buttonId];
        const hasValue = checkSelectorHasValue(selectorKey);
        updateButtonStatusIndicator(buttonId, hasValue);
        selectorStatus[selectorKey] = hasValue;
    });

    console.log('Updated all button statuses:', selectorStatus);
}

/**
 * Check if a selector has a value
 */
function checkSelectorHasValue(selectorKey) {
    if (!currentSelectorData) return false;
    
    // For SEO, we don't check for selector value since it's configuration-based
    if (selectorKey === 'seo') {
        return true; // SEO is always available
    }
    
    const selectorData = currentSelectorData[selectorKey];
    return selectorData && selectorData.selector && selectorData.selector.trim() !== '';
}

/**
 * Update status indicator in button
 */
function updateButtonStatusIndicator(buttonId, hasValue) {
    const button = document.getElementById(buttonId);
    if (!button) return;

    // Remove existing status indicators
    const existingIndicator = button.querySelector('.status-indicator');
    if (existingIndicator) {
        existingIndicator.remove();
    }

    // Ensure button has consistent flex styling with proper spacing
    button.classList.remove('justify-start'); // Remove old justify
    button.classList.add('flex', 'items-center'); // Simple flex layout
    
    // Ensure button has minimum width for consistency  
    if (!button.style.minWidth) {
        button.style.minWidth = '90px';
    }

    // Create status indicator element with balanced positioning
    const indicator = document.createElement('span');
    indicator.className = 'status-indicator flex-shrink-0 ml-2';
    indicator.style.marginLeft = '6px'; // Balanced gap from text
    
    if (hasValue) {
        indicator.innerHTML = `<img src="/static/frontendApp/assets/images/check.png" alt="✔" class="w-4 h-4" style="filter: invert(58%) sepia(14%) saturate(3166%) hue-rotate(100deg) brightness(95%) contrast(80%);" />`;
    } else {
        indicator.innerHTML = '<span class="text-red-600  text-sm">X</span>';
    }

    // Append indicator to the end of button (right end)
    button.appendChild(indicator);
}

/**
 * Update button status when input changes
 */
function updateButtonStatusFromInput(selectorKey, inputValue) {
    const buttonMapping = {
        'source_title': 'title-btn',
        'source_tags': 'tag-btn', 
        'source_categories': 'category-btn',
        'source_author': 'author-btn',
        'source_published_date': 'date-btn',
        'source_featured_image': 'image-btn',
        'source_content': 'content-btn',
        'seo': 'seo-btn'
    };

    const buttonId = buttonMapping[selectorKey];
    if (buttonId) {
        const hasValue = inputValue && inputValue.trim() !== '';
        updateButtonStatusIndicator(buttonId, hasValue);
        selectorStatus[selectorKey] = hasValue;
        console.log(`Updated ${buttonId} status:`, hasValue);
    }
}

// Expose functions globally for external use with proper namespace
window.articleHtmlFunctions = {
    get_html_content,
    add_article_url_selector_api,
    updatePreviewContent,
    generateElementSelector,
    handleElementClick,
    updateSelectorInput
};

// Also expose the main functions directly to global scope for backward compatibility
window.get_html_content = get_html_content;
window.add_article_url_selector_api = add_article_url_selector_api;

/**
 * Detect if selector is XPath or CSS - NEW FUNCTION FOR XPATH SUPPORT
 */
function isArticleXPathSelector(selector) {
    // XPath expressions typically start with / or // or contain XPath-specific syntax
    return selector.startsWith('/') || 
           selector.startsWith('//') || 
           selector.includes('::') ||
           selector.includes('[text()') ||
           selector.includes('[contains(') ||
           selector.includes('ancestor::') ||
           selector.includes('descendant::') ||
           selector.includes('following::') ||
           selector.includes('preceding::');
}

/**
 * Execute XPath query on document - NEW FUNCTION FOR XPATH SUPPORT
 */
function executeArticleXPath(xpath, document) {
    try {
        const result = document.evaluate(
            xpath,
            document,
            null,
            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
            null
        );
        
        const elements = [];
        for (let i = 0; i < result.snapshotLength; i++) {
            elements.push(result.snapshotItem(i));
        }
        
        console.log('ARTICLE: XPath query executed successfully:', xpath, 'Found elements:', elements.length);
        return elements;
    } catch (error) {
        console.error('ARTICLE: XPath execution error:', error);
        return [];
    }
}

/**
 * Get elements using either CSS selector or XPath - UNIVERSAL SELECTOR FUNCTION
 */
function getArticleElementsBySelector(selector, document) {
    if (!selector || !selector.trim()) {
        console.warn('ARTICLE: Empty selector provided');
        return [];
    }
    
    const cleanSelector = selector.trim();
    
    if (isArticleXPathSelector(cleanSelector)) {
        console.log('ARTICLE: Using XPath selector:', cleanSelector);
        return executeArticleXPath(cleanSelector, document);
    } else {
        console.log('ARTICLE: Using CSS selector:', cleanSelector);
        try {
            return Array.from(document.querySelectorAll(cleanSelector));
        } catch (error) {
            console.error('ARTICLE: CSS selector error:', error);
            return [];
        }
    }
}

function show_list_competitor(){
    
    if (list_competitor_page_url) {
                setTimeout(() => {
                    window.location.href = list_competitor_page_url;
                }, 1000);
            }
}