// Global variables for state management
let selectedElementCategory = null;
let selectedInputCategory = null;

async function get_category_html_content() {

    const competitor_domain_mapping_slug_id = localStorage.getItem('competitor_domain_mapping_slug_id');
    const access_token = localStorage.getItem("access_token");
    const params = new URLSearchParams();
    
    if (competitor_domain_mapping_slug_id) {
        params.append("competitor_domain_mapping_slug_id", competitor_domain_mapping_slug_id);
    }
    params.append("type", "category");
    
    // Show loader in HTML container
    showHtmlCategoryLoader();

    const full_url = `${scrap_html_content_url}?${params.toString()}`;

    try{
        const response = await fetch(full_url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${access_token}`
            }
        });

        const response_data = await response.json();
        console.log("CATEGORY API Response - HTML content and selectors:", response_data);
        
        if (response.ok && response_data.status === "success") {
            // Hide loader immediately when we get successful response
            hideHtmlCategoryLoader();
            
            // Store the competitor_selected_url_slug_id for later use
            if (response_data.data.competitor_selected_url_slug_id) {
                localStorage.setItem('category_competitor_selected_url_slug_id', response_data.data.competitor_selected_url_slug_id);
                console.log('CATEGORY: Stored category_competitor_selected_url_slug_id:', response_data.data.competitor_selected_url_slug_id);
            }
            
            // Display the HTML content in container - USE UNIQUE FUNCTION NAME
            displayCategoryHtmlContent(response_data.data.html_content);
            
            show_toast("success", response_data.data.message || "Category content loaded successfully");
        } else {
            show_toast("error", response_data.data.message || "Something went wrong");
            hideHtmlCategoryLoader();
        }
    }
    catch (error) {
        console.error('Error fetching category HTML content:', error);
        show_toast("error", "Network error. Please try again later.");
        hideHtmlCategoryLoader();
    }
}

// Expose main function immediately after definition
window.get_category_html_content = get_category_html_content;
console.log('get_category_html_content exposed immediately:', typeof window.get_category_html_content);

/**
 * Show simple loader in main HTML container
 */
function showHtmlCategoryLoader() {
    const htmlContainer = document.getElementById('html-container-category');
    if (!htmlContainer) {
        console.error("CATEGORY: HTML container not found");
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
function hideHtmlCategoryLoader() {
    const htmlContainer = document.getElementById('html-container-category');
    if (htmlContainer) {
        htmlContainer.innerHTML = '';
    }
}

/**
 * Display HTML content in an iframe for safe rendering - RENAMED TO BE UNIQUE
 */
function displayCategoryHtmlContent(htmlContent) {
    const htmlContainer = document.getElementById('html-container-category');
    if (!htmlContainer) {
        console.error("CATEGORY: HTML container not found");
        return;
    }

    console.log('CATEGORY: displayCategoryHtmlContent called with content length:', htmlContent.length);

    // Ensure loader is hidden (defensive programming)
    hideHtmlCategoryLoader();
    
    // Process HTML content to fix mixed content issues
    const processedHtml = fixCategoryMixedContentImages(htmlContent);
    console.log('CATEGORY: processed HTML length:', processedHtml.length);
    
    // Use proper iframe implementation with unique IDs to avoid conflicts
    console.log('CATEGORY: Creating proper iframe for category content');
    displayCategoryHtmlContentInIframe(processedHtml, htmlContainer);
}

/**
 * Display HTML content in proper iframe - FIXED TO MATCH ARTICLE APPROACH
 */
function displayCategoryHtmlContentInIframe(htmlContent, container) {
    console.log('CATEGORY: Setting up iframe to match parent div size exactly');
    container.innerHTML = '';
    
    // Create iframe to fill the parent container exactly - NO WRAPPER NEEDED
    const iframe = document.createElement('iframe');
    iframe.id = 'html-content-iframe-category-unique';
    
    // Make iframe inherit exact parent dimensions
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.minHeight = '600px'; // Fallback minimum height
    iframe.style.border = '1px solid #e5e7eb';
    iframe.style.borderRadius = '8px';
    iframe.style.margin = '0';
    iframe.style.padding = '0';
    iframe.style.display = 'block';
    iframe.style.boxSizing = 'border-box';
    
    // Use srcdoc for better content loading - SAME AS ARTICLE
    iframe.srcdoc = htmlContent;
    
    // Append directly to parent container to inherit its exact size
    container.appendChild(iframe);
    
    // Wait for iframe to load then add interactivity - SAME AS ARTICLE
    iframe.addEventListener('load', function() {
        console.log('CATEGORY: Iframe loaded successfully');
        setTimeout(() => {
            setupCategoryIframeInteractivity();
        }, 100);
    });
    
    // Fallback: if iframe doesn't load in 2 seconds, try direct content injection - SAME AS ARTICLE
    setTimeout(() => {
        if (!iframe.contentDocument || !iframe.contentDocument.body || iframe.contentDocument.body.innerHTML.trim() === '') {
            console.warn('CATEGORY: Iframe failed to load, trying direct content injection');
            try {
                iframe.contentDocument.open();
                iframe.contentDocument.write(htmlContent);
                iframe.contentDocument.close();
                setTimeout(() => {
                    setupCategoryIframeInteractivity();
                }, 100);
            } catch (error) {
                console.error('CATEGORY: Failed to inject content into iframe:', error);
                // Last resort: use div with innerHTML
                displayCategoryHtmlContentFallback(htmlContent, container);
            }
        }
    }, 2000);
}

/**
 * Setup interactivity for category iframe content - SAME AS ARTICLE BUT FOR CATEGORY
 */
function setupCategoryIframeInteractivity() {
    const iframe = document.getElementById('html-content-iframe-category-unique');
    if (!iframe) {
        console.error('CATEGORY: Iframe not found for interactivity setup');
        return;
    }
    
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    if (!iframeDoc) {
        console.error('CATEGORY: Cannot access iframe document for interactivity');
        return;
    }
    
    console.log('CATEGORY: Setting up iframe interactivity');
    
    // Add click event listener to iframe document
    iframeDoc.addEventListener('click', function(event) {
        event.preventDefault();
        console.log('CATEGORY: Click detected in iframe');
        
        if (event.target && event.target !== iframeDoc) {
            console.log('CATEGORY: Element clicked in iframe:', event.target.tagName, event.target.className);
            handleCategoryElementClick(event.target);
        }
    });
    
    // Add hover effects
    iframeDoc.addEventListener('mouseover', function(event) {
        if (event.target && event.target !== iframeDoc) {
            event.target.style.backgroundColor = 'rgba(134, 126, 255, 0.3)';
            event.target.style.cursor = 'pointer';
        }
    });
    
    iframeDoc.addEventListener('mouseout', function(event) {
        if (event.target && event.target !== iframeDoc && !event.target.classList.contains('selected')) {
            event.target.style.backgroundColor = '';
            event.target.style.cursor = '';
        }
    });
    
    console.log('CATEGORY: Iframe interactivity setup complete');
    
    // Test if we can see elements
    const allElements = iframeDoc.querySelectorAll('*');
    console.log('CATEGORY: Total elements found in iframe:', allElements.length);
    
    if (allElements.length > 5) {
        console.log('CATEGORY: First few iframe elements:', Array.from(allElements).slice(0, 5).map(el => ({
            tag: el.tagName,
            class: el.className,
            id: el.id
        })));
    }
}

/**
 * Fallback method to display HTML content using div with innerHTML - RENAMED TO BE UNIQUE
 */
function displayCategoryHtmlContentFallback(htmlContent, container) {
    console.log('CATEGORY: Using fallback method to display HTML content');
    container.innerHTML = '';
    
    const contentDiv = document.createElement('div');
    contentDiv.id = 'html-content-div-category-unique'; // UNIQUE ID
    contentDiv.style.width = '100%';
    contentDiv.style.height = '600px';
    contentDiv.style.border = '1px solid #e5e7eb';
    contentDiv.style.borderRadius = '8px';
    contentDiv.style.overflow = 'auto';
    contentDiv.style.padding = '10px';
    contentDiv.style.backgroundColor = '#fff';
    
    // Set the HTML content
    contentDiv.innerHTML = htmlContent;
    console.log('CATEGORY: HTML content set in div, content length:', htmlContent.length);
    console.log('CATEGORY: First 200 chars:', htmlContent.substring(0, 200));
    
    container.appendChild(contentDiv);
    console.log('CATEGORY: Content div appended to container');
    
    // Check if div was actually added and has content
    setTimeout(() => {
        const divInDom = document.getElementById('html-content-div-category-unique');
        console.log('CATEGORY: Div in DOM:', !!divInDom);
        if (divInDom) {
            console.log('CATEGORY: Div dimensions:', {
                width: divInDom.offsetWidth,
                height: divInDom.offsetHeight,
                innerHTML_length: divInDom.innerHTML.length,
                hasContent: divInDom.innerHTML.trim().length > 0
            });
            
            // Check if the content is actually visible
            const rect = divInDom.getBoundingClientRect();
            console.log('CATEGORY: Div position and visibility:', {
                top: rect.top,
                left: rect.left,
                width: rect.width,
                height: rect.height,
                display: window.getComputedStyle(divInDom).display,
                visibility: window.getComputedStyle(divInDom).visibility,
                opacity: window.getComputedStyle(divInDom).opacity
            });
        }
    }, 100);
    
    // Add interactivity to the HTML elements - FALLBACK DIV ONLY
    console.log('CATEGORY: Calling addCategoryHtmlInteractivityFallback for div fallback');
    setTimeout(() => {
    addCategoryHtmlInteractivityFallback();
    }, 200);
}

/**
 * Fix mixed content issues and remove advertising scripts - RENAMED TO BE UNIQUE
 */
function fixCategoryMixedContentImages(htmlContent) {
    // Create a temporary div to parse HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = htmlContent;
    
    // Remove Google AdSense and advertising-related scripts and elements
    removeCategoryAdvertisingContent(tempDiv);
    
    // Find all img elements and fix src attributes
    const images = tempDiv.querySelectorAll('img');
    images.forEach(img => {
        // Fix src attribute
        const src = img.getAttribute('src');
        if (src && src.startsWith('http://')) {
            const httpsUrl = src.replace('http://', 'https://');
            img.setAttribute('src', httpsUrl);
            console.log(`CATEGORY: Converted image URL: ${src} -> ${httpsUrl}`);
        }
        
        // Fix data-src for lazy loaded images
        const dataSrc = img.getAttribute('data-src');
        if (dataSrc && dataSrc.startsWith('http://')) {
            const httpsUrl = dataSrc.replace('http://', 'https://');
            img.setAttribute('data-src', httpsUrl);
            console.log(`CATEGORY: Converted data-src URL: ${dataSrc} -> ${httpsUrl}`);
        }
        
        // Fix srcset attribute
        const srcset = img.getAttribute('srcset');
        if (srcset && srcset.includes('http://')) {
            const httpsSrcset = srcset.replace(/http:\/\//g, 'https://');
            img.setAttribute('srcset', httpsSrcset);
            console.log('CATEGORY: Converted srcset URLs to HTTPS');
        }
    });
    
    // Fix link elements (CSS, favicons, etc.)
    const links = tempDiv.querySelectorAll('link[href^="http://"]');
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('http://')) {
            const httpsUrl = href.replace('http://', 'https://');
            link.setAttribute('href', httpsUrl);
            console.log(`CATEGORY: Converted link URL: ${href} -> ${httpsUrl}`);
        }
    });
    
    // Fix script sources (but only keep non-advertising scripts)
    const scripts = tempDiv.querySelectorAll('script[src^="http://"]');
    scripts.forEach(script => {
        const src = script.getAttribute('src');
        if (src && src.startsWith('http://')) {
            const httpsUrl = src.replace('http://', 'https://');
            script.setAttribute('src', httpsUrl);
            console.log(`CATEGORY: Converted script URL: ${src} -> ${httpsUrl}`);
        }
    });
    
    // Fix background images in style attributes
    const elementsWithStyle = tempDiv.querySelectorAll('[style*="background-image"]');
    elementsWithStyle.forEach(element => {
        let style = element.getAttribute('style');
        if (style && style.includes('http://')) {
            style = style.replace(/http:\/\//g, 'https://');
            element.setAttribute('style', style);
            console.log('CATEGORY: Converted background image URL in style attribute');
        }
    });
    
    // Fix CSS background images in style tags
    const styleTags = tempDiv.querySelectorAll('style');
    styleTags.forEach(styleTag => {
        let cssContent = styleTag.textContent;
        if (cssContent && cssContent.includes('http://')) {
            cssContent = cssContent.replace(/http:\/\//g, 'https://');
            styleTag.textContent = cssContent;
            console.log('CATEGORY: Converted background image URLs in CSS');
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
            
            console.log('CATEGORY: Added CSP meta tag and iframe fix styles to existing head');
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
            console.log('CATEGORY: Created new head with CSP meta tag and iframe fix styles');
        }
    }
    
    return tempDiv.innerHTML;
}

/**
 * Remove advertising content and scripts to prevent conflicts - RENAMED TO BE UNIQUE
 */
function removeCategoryAdvertisingContent(container) {
    // Remove Google AdSense elements
    const adElements = container.querySelectorAll('.adsbygoogle, ins.adsbygoogle, [class*="adsbygoogle"], [id*="google_ads"], [class*="google-ad"], [id*="div-gpt-ad"]');
    adElements.forEach(el => {
        console.log('CATEGORY: Removed AdSense element:', el.className || el.id);
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
            console.log('CATEGORY: Removed advertising script:', scriptSrc || 'inline script');
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
            console.log('CATEGORY: Removed advertising iframe:', src);
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
                console.log('CATEGORY: Removed ad-related element:', selector, el.className || el.id);
                el.remove();
            });
        } catch (error) {
            // Ignore selector errors
        }
    });
    
    console.log('CATEGORY: Advertising content cleanup completed');
}

/**
 * Add click and hover interactivity to HTML elements in fallback div
 */
function addCategoryHtmlInteractivityFallback() {
    console.log('CATEGORY: Starting addCategoryHtmlInteractivityFallback');
    
    const contentDiv = document.getElementById('html-content-div-category-unique');
    if (!contentDiv) {
        console.error("CATEGORY: HTML content div not found");
        return;
    }
    
    console.log('CATEGORY: Content div found, setting up event listeners');
    console.log('CATEGORY: Content div has content:', contentDiv.innerHTML.length > 0);
    console.log('CATEGORY: Content div visible:', window.getComputedStyle(contentDiv).display !== 'none');

    // Add click event delegation
    contentDiv.addEventListener('click', (event) => {
        event.preventDefault();
        console.log('CATEGORY: Click event on content div');
        if (event.target && event.target !== contentDiv) {
            console.log('CATEGORY: Element clicked:', event.target.tagName, event.target.className);
            handleCategoryElementClick(event.target);
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
    
    console.log('CATEGORY: Event listeners added successfully');
    
    // Test if we can see any HTML elements
    const allElements = contentDiv.querySelectorAll('*');
    console.log('CATEGORY: Total elements found in content:', allElements.length);
    
    if (allElements.length > 0) {
        console.log('CATEGORY: First few elements:', Array.from(allElements).slice(0, 5).map(el => ({
            tag: el.tagName,
            class: el.className,
            id: el.id,
            text: el.textContent?.substring(0, 50)
        })));
    }
}

/**
 * Handle click on HTML elements
 */
function handleCategoryElementClick(element) {
    const selector = generateCategoryElementSelector(element);
    
    if (selector) {
        // Update visual selection
        updateCategoryElementSelection(element);
        
        // Update input field if exists
        updateCategorySelectorInput(selector);
        
        // Update preview content
        updateCategoryPreviewContent(element, selector);
        
        console.log('CATEGORY: Selected element with selector:', selector);
    }
}

/**
 * Generate a specific CSS selector for an element
 */
function generateCategoryElementSelector(element) {
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

async function add_category_selector() {
    try {
        // Get selector value from input
        const selector_value = document.getElementById('category_selector_input')?.value;
        
        if (!selector_value) {
            show_toast("error", "Please enter a selector value.");
            return;
        }

        // Get selected radio button value
        const selectedRadio = document.querySelector('input[name="status"]:checked');
        const selector_name = selectedRadio ? selectedRadio.closest('label').textContent.trim().toLowerCase() : 'article';

        // Get URL ID
        const competitor_selected_url_slug_id = localStorage.getItem('category_competitor_selected_url_slug_id');

        let data = new FormData();

        data.append("competitor_selected_url_slug_id", competitor_selected_url_slug_id);
        data.append("selector_name", selector_name);
        data.append("selector", selector_value);

        const response_data = await add_api(add_category_url_selector_url, data);

        console.log(response_data,"response_data add_category_selector");

    } catch (error) {
        console.error('Error:', error);
        show_toast("error", "Network error occurred");
    }
}

async function show_article_url_step(){
    current_step = 2;
    showStep(current_step);
}

/**
 * Update visual selection of elements
 */
function updateCategoryElementSelection(element) {
    // Try iframe first - NOW USES PROPER IFRAME
    const iframe = document.getElementById('html-content-iframe-category-unique');
    if (iframe && iframe.contentDocument) {
        console.log('CATEGORY: Updating selection in iframe');
        // Remove previous selections in iframe
        iframe.contentDocument.querySelectorAll('.selected').forEach(el => {
            el.classList.remove('selected');
            el.style.backgroundColor = '';
        });
    } else {
        // Fallback to div - USE UNIQUE ID
        console.log('CATEGORY: Fallback to div for selection update');
        const contentDiv = document.getElementById('html-content-div-category-unique');
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
    
    selectedElementCategory = element;
    console.log('CATEGORY: Element selection updated');
}

/**
 * Update the selector input field (looks for focused input)
 */
function updateCategorySelectorInput(selector) {
    // First try to update the main category selector input
    const categorySelectorInput = document.getElementById('category_selector_input');
    if (categorySelectorInput) {
        categorySelectorInput.value = selector;
        categorySelectorInput.dispatchEvent(new Event('input'));
        console.log('CATEGORY: Updated category selector input with selector:', selector);
        
        // Auto-test the selector when it's set from element click
        if (selector.trim()) {
            testCategorySelector(selector.trim());
        }
        return;
    }

    // Update the focused input if available
    if (selectedInputCategory && selectedInputCategory.tagName === 'INPUT') {
        selectedInputCategory.value = selector;
        selectedInputCategory.dispatchEvent(new Event('input'));
        console.log('CATEGORY: Updated focused input with selector:', selector);
    } else {
        // Fallback to any visible selector input
        const selectorInput = document.querySelector('input[name="selector_value"]:not([style*="display: none"])') || 
                             document.querySelector('input[placeholder*="selector"]') ||
                             document.querySelector('input[type="text"]:focus');
        
        if (selectorInput) {
            selectorInput.value = selector;
            selectorInput.dispatchEvent(new Event('input'));
            console.log('CATEGORY: Updated fallback input with selector:', selector);
        }
    }
}

/**
 * Update preview content for category (matching check_article.js design)
 */
function updateCategoryPreviewContent(element, selector) {
    const processedContentDiv = document.getElementById('processed-content-category');
    if (!processedContentDiv) {
        console.warn("CATEGORY: Category preview container not found");
        return;
    }

    // Clear previous content
    processedContentDiv.innerHTML = '';
    
    // Create selectorData object for proper preview
    const selectorData = {
        selector: selector,
        attribute: null
    };
    
    // Update preview using the same logic as check_article.js
    updateCategoryPreviewContent_Internal(selectorData);
}

/**
 * Update preview content (same design as check_article.js) - RENAMED TO BE UNIQUE
 */
function updateCategoryPreviewContent_Internal(selectorData) {
    const processedContentDiv = document.getElementById('processed-content-category');
    if (!processedContentDiv) return;

    // Clear previous content
    processedContentDiv.innerHTML = '';

    // Update preview if selector exists
    if (selectorData && selectorData.selector) {
        let htmlContainer = null;
        
        // Try iframe first - PROPER IFRAME PRIORITY
        const iframe = document.getElementById('html-content-iframe-category-unique');
        if (iframe && iframe.contentDocument && iframe.contentDocument.body) {
            console.log('CATEGORY: Using iframe for preview content');
            htmlContainer = iframe.contentDocument;
        } else {
            // Fallback to div - USE UNIQUE ID
            console.log('CATEGORY: Using div fallback for preview content');
            const contentDiv = document.getElementById('html-content-div-category-unique');
            if (contentDiv) {
                htmlContainer = contentDiv;
            }
        }

        if (htmlContainer) {
            try {
                // Use the universal selector function that handles both CSS and XPath
                const selectedElements = getCategoryElementsBySelector(selectorData.selector, htmlContainer);
                let hasContent = false;
                
                // Show selector type in console
                const selectorType = isCategoryXPathSelector(selectorData.selector) ? 'XPath' : 'CSS';
                console.log('CATEGORY: Preview using', selectorType, 'selector:', selectorData.selector);

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
                        showCategoryNoContentMessage(processedContentDiv, ` ${selectorType} Selector: No content found (empty elements)`);
                    }
                } else {
                    showCategoryNoContentMessage(processedContentDiv, ` ${selectorType} Selector: No elements found matching this selector`);
                }
            } catch (error) {
                const selectorTypeMsg = isCategoryXPathSelector(selectorData.selector) ? 'XPath' : 'CSS';
                showCategoryNoContentMessage(processedContentDiv, ` Invalid ${selectorTypeMsg} Selector: ${error.message}`);
            }
        }
    } else {
        showCategoryNoContentMessage(processedContentDiv, "Please enter a valid selector");
    }
}

/**
 * Show no content message (same as check_article.js)
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

// Initialize event listeners for input focus tracking and search functionality
function initializeCategoryEventListeners() {
    // Focus tracking for inputs
    document.addEventListener('focusin', (event) => {
        if (event.target.tagName === 'INPUT') {
            selectedInputCategory = event.target;
            console.log('Category input focused:', event.target.placeholder || event.target.name);
        }
    });

    document.addEventListener('focusout', (event) => {
        if (event.target.tagName === 'INPUT') {
            // Keep the last focused input for a short time
            setTimeout(() => {
                if (document.activeElement.tagName !== 'INPUT') {
                    // Only clear if no other input is focused
                    console.log('Category input focus cleared');
                }
            }, 100);
        }
    });

    // Search button functionality
    const searchButton = document.getElementById('category_search_btn');
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            const input = document.getElementById('category_selector_input');
            if (input && input.value.trim()) {
                testCategorySelector(input.value.trim());
            } else {
                show_toast("warning", "Please enter a selector to test");
            }
        });
    }

    // Enter key functionality for category selector input
    const categorySelectorInput = document.getElementById('category_selector_input');
    if (categorySelectorInput) {
        categorySelectorInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                if (this.value.trim()) {
                    testCategorySelector(this.value.trim());
                }
            }
        });

        // Clear preview when input changes
        categorySelectorInput.addEventListener('input', function() {
            const previewDiv = document.getElementById('processed-content-category');
            if (previewDiv && this.value.trim() === '') {
                previewDiv.innerHTML = '';
            }
        });
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCategoryEventListeners);
} else {
    initializeCategoryEventListeners();
}

// Expose functions globally for external use with proper namespace
window.categoryHtmlFunctions = {
    get_category_html_content,
    handleCategoryElementClick,
    updateCategorySelectorInput,
    generateCategoryElementSelector,
    add_category_selector,
    testCategorySelector,
    showCategoryNoContentMessage
};

// Also expose the main functions directly to global scope for backward compatibility
window.add_category_selector = add_category_selector;
window.testCategorySelector = testCategorySelector;

/**
 * Test category selector and show preview results (similar to check_article.js)
 */
function testCategorySelector(selector) {
    const processedContentDiv = document.getElementById('processed-content-category');
    if (!processedContentDiv) {
        console.warn("Category preview container not found");
        return;
    }

    // Clear previous content
    processedContentDiv.innerHTML = '';

    if (!selector || !selector.trim()) {
        showCategoryNoContentMessage(processedContentDiv, "Please enter a valid selector");
        return;
    }

    let htmlContainer = null;
    
    // Try iframe first - PROPER IFRAME PRIORITY
    const iframe = document.getElementById('html-content-iframe-category-unique');
    if (iframe && iframe.contentDocument && iframe.contentDocument.body) {
        console.log('CATEGORY: Testing selector in iframe');
        htmlContainer = iframe.contentDocument;
    } else {
        // Fallback to div
        console.log('CATEGORY: Testing selector in div fallback');
        const contentDiv = document.getElementById('html-content-div-category-unique');
        if (contentDiv) {
            htmlContainer = contentDiv;
        }
    }

    if (!htmlContainer) {
        showCategoryNoContentMessage(processedContentDiv, "HTML content not loaded");
        return;
    }

    try {
        // Use the universal selector function that handles both CSS and XPath
        const selectedElements = getCategoryElementsBySelector(selector.trim(), htmlContainer);
        let hasContent = false;
        
        // Show selector type in console
        const selectorType = isCategoryXPathSelector(selector.trim()) ? 'XPath' : 'CSS';
        console.log('CATEGORY: Testing', selectorType, 'selector:', selector);

        if (selectedElements && selectedElements.length > 0) {
            // Create preview container
            const previewContainer = document.createElement('div');
            previewContainer.className = 'space-y-2';

            // Add each found element to preview
            selectedElements.forEach((element, index) => {
                const value = element.textContent.trim();

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

                // Show toast success
            } else {
                showCategoryNoContentMessage(processedContentDiv, ` ${selectorType} Selector: No content found (empty elements)`);
            }
        } else {
            showCategoryNoContentMessage(processedContentDiv, ` ${selectorType} Selector: No elements found matching this selector`);
        }
    } catch (error) {
        const selectorTypeMsg = isCategoryXPathSelector(selector.trim()) ? 'XPath' : 'CSS';
        showCategoryNoContentMessage(processedContentDiv, `Invalid ${selectorTypeMsg} Selector: ${error.message}`);
    }
}

/**
 * Show no content message for category preview (similar to check_article.js)
 */
function showCategoryNoContentMessage(container, message) {
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
 * Detect if selector is XPath or CSS - NEW FUNCTION FOR XPATH SUPPORT
 */
function isCategoryXPathSelector(selector) {
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
function executeCategoryXPath(xpath, document) {
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
        
        console.log('CATEGORY: XPath query executed successfully:', xpath, 'Found elements:', elements.length);
        return elements;
    } catch (error) {
        console.error('CATEGORY: XPath execution error:', error);
        return [];
    }
}

/**
 * Get elements using either CSS selector or XPath - UNIVERSAL SELECTOR FUNCTION
 */
function getCategoryElementsBySelector(selector, document) {
    if (!selector || !selector.trim()) {
        console.warn('CATEGORY: Empty selector provided');
        return [];
    }
    
    const cleanSelector = selector.trim();
    
    if (isCategoryXPathSelector(cleanSelector)) {
        console.log('CATEGORY: Using XPath selector:', cleanSelector);
        return executeCategoryXPath(cleanSelector, document);
    } else {
        console.log('CATEGORY: Using CSS selector:', cleanSelector);
        try {
            return Array.from(document.querySelectorAll(cleanSelector));
        } catch (error) {
            console.error('CATEGORY: CSS selector error:', error);
            return [];
        }
    }
}



