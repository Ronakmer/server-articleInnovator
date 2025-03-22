












// Function to render dynamic 
function table_data_domain(tbody_name, response_data, delete_function_name, status_function_name, update_page_url, detail_domain_page_url) {


    const main_div_id = document.getElementById(tbody_name); 

    main_div_id.innerHTML = ''; 
    // const start_date = '2024-11-25';  // Replace with dynamic date if needed
    // const end_date = '2025-01-25';    // Replace with dynamic date if needed


    // Get the current date
    const end_date = new Date();

    // Get the date 7 days ago
    const start_date = new Date();
    start_date.setDate(end_date.getDate() - 7);

    // Format dates as 'YYYY-MM-DD'
    const formatDate = (date) => date.toISOString().split('T')[0];

    const start_date_str = formatDate(start_date);
    const end_date_str = formatDate(end_date);


    response_data.data.forEach((obj, index) => {
        const domain_console_data = domain_console_graph_api(domain_console_metrics_url, obj.slug_id, start_date_str, end_date_str);
        const domain_analytics_data = domain_analytics_graph_api(domain_analytics_metrics_url, obj.slug_id, start_date_str, end_date_str);
        const domain_article_data = domain_article_graph_api(domain_article_metrics_url, obj.slug_id, start_date_str, end_date_str);

        console.log(domain_article_data,'domain_article_data')

        domain_impressions_chart(domain_console_data, obj.slug_id)
        domain_traffic_chart(domain_analytics_data, obj.slug_id)
        domain_article_chart(domain_article_data, obj.slug_id)

        // manager image loop
        const managerUserDetails = obj.manager_id_data || [];  // Fallback to an empty array if not available
        let managerImageElements = '';
        managerUserDetails.forEach((user, idx) => {
            const imgSrc = user.profile_image || '/path/to/default/image.png';  // Use default if profile image is missing
            managerImageElements += `
                <img src="${imgSrc}" alt="Profile Picture ${idx + 1}" class="w-12 h-12 rounded-full border-2 border-white hover:scale-105 transition-transform duration-200">
            `;
        });

        
        // writer image loop
        const writerUserDetails = obj.writer_id_data || [];  // Fallback to an empty array if not available
        let writerImageElements = '';
        writerUserDetails.forEach((user, idx) => {
            const imgSrc = user.profile_image || '/path/to/default/image.png';  // Use default if profile image is missing
            writerImageElements += `
                <img src="${imgSrc}" alt="Profile Picture ${idx + 1}" class="w-12 h-12 rounded-full border-2 border-white hover:scale-105 transition-transform duration-200">
            `;
        });



        const div = document.createElement('div');
        div.classList.add('border-gray-200',  'mt-6', 'border',  'border-solid',  'rounded-xl');
        // alert(obj.slug_id)
        div.innerHTML = `
        <div class="mb-4 px-4">  

        <div class="flex md:flex-row flex-col md:space-x-4 space-y-4 md:space-y-0 w-full">
            <div class="w-full md:w-1/2">

                <!-- statr similar web part  -->
                <div
                    class="flex md:flex-row flex-col md:space-x-4 space-y-4 md:space-y-0 mt-4 w-full">
                    <div class="w-full md:w-[350px] 2xl:max-w-full">
                        <div
                            class="border-gray-200 bg-light-blue p-3 border rounded-xl max-md:w-full max-md:text-center">
                            <div class="flex max-md:flex-col-reverse items-center">
                                <div class="flex-1 max-md:flex-auto">
                                    <div class="text-gray-600 text-sm">Domain Name</div>
                                    <div class="text-gray-900 text-sm">
                                        ${obj.name}</div>
                                </div>
                                <div class="ml-2">
                                    <svg width="48" height="49" viewBox="0 0 48 49" fill="none"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <g filter="url(#filter0_d_221_15724)">
                                            <rect x="8" y="7" width="32" height="32" rx="10"
                                                fill="#4F46E5" shape-rendering="crispEdges"></rect>
                                            <path
                                                d="M23.9993 31.3334C28.6017 31.3334 32.3327 27.6024 32.3327 23C32.3327 18.3976 28.6017 14.6667 23.9993 14.6667C19.397 14.6667 15.666 18.3976 15.666 23C15.666 27.6024 19.397 31.3334 23.9993 31.3334Z"
                                                stroke="white" stroke-width="1.25"
                                                stroke-linecap="round" stroke-linejoin="round">
                                            </path>
                                            <path
                                                d="M20.6667 15.5H21.5C19.875 20.3667 19.875 25.6333 21.5 30.5H20.6667"
                                                stroke="white" stroke-width="1.25"
                                                stroke-linecap="round" stroke-linejoin="round">
                                            </path>
                                            <path
                                                d="M26.5 15.5C28.125 20.3667 28.125 25.6333 26.5 30.5"
                                                stroke="white" stroke-width="1.25"
                                                stroke-linecap="round" stroke-linejoin="round">
                                            </path>
                                            <path
                                                d="M16.5 26.3333V25.5C21.3667 27.125 26.6333 27.125 31.5 25.5V26.3333"
                                                stroke="white" stroke-width="1.25"
                                                stroke-linecap="round" stroke-linejoin="round">
                                            </path>
                                            <path
                                                d="M16.5 20.5C21.3667 18.875 26.6333 18.875 31.5 20.5"
                                                stroke="white" stroke-width="1.25"
                                                stroke-linecap="round" stroke-linejoin="round">
                                            </path>
                                        </g>
                                        <defs>
                                            <filter id="filter0_d_221_15724" x="0.302681"
                                                y="0.842145" width="47.3946" height="47.3946"
                                                filterUnits="userSpaceOnUse"
                                                color-interpolation-filters="sRGB">
                                                <feFlood flood-opacity="0"
                                                    result="BackgroundImageFix"></feFlood>
                                                <feColorMatrix in="SourceAlpha" type="matrix"
                                                    values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0"
                                                    result="hardAlpha"></feColorMatrix>
                                                <feOffset dy="1.53946"></feOffset>
                                                <feGaussianBlur stdDeviation="3.84866">
                                                </feGaussianBlur>
                                                <feComposite in2="hardAlpha" operator="out">
                                                </feComposite>
                                                <feColorMatrix type="matrix"
                                                    values="0 0 0 0 0.486275 0 0 0 0 0.552941 0 0 0 0 0.709804 0 0 0 0.12 0">
                                                </feColorMatrix>
                                                <feBlend mode="normal" in2="BackgroundImageFix"
                                                    result="effect1_dropShadow_221_15724"></feBlend>
                                                <feBlend mode="normal" in="SourceGraphic"
                                                    in2="effect1_dropShadow_221_15724"
                                                    result="shape"></feBlend>
                                            </filter>
                                        </defs>
                                    </svg>


                                </div>
                            </div>
                        </div>


                    </div>
                    <div class="w-full max-w-full md:max-w-[208px] 2xl:max-w-full ">

                        <div
                            class="flex flex-wrap justify-end max-md:justify-center items-center gap-4 max-md:w-full">
                            <div
                                class="gap-4 border-gray-200 grid grid-cols-2 max-md:grid-cols-1 p-3 max-md:p-2 border max-md:border-r-0 border-solid rounded-xl max-md:w-full font-poppins text-sm max-md:text-center">
                                <!-- Domain Type -->
                                <div
                                    class="flex max-md:flex-col justify-between max-md:justify-center items-center border-gray-200 pr-4 max-md:pb-2 border-r max-md:border-r-0 max-md:border-b border-solid">
                                    <div class="flex-1 max-md:flex-auto">
                                        <div class="font-medium">
                                            <div
                                                class="flex items-center bg-blue-100 mb-1.5 px-3 py-1 rounded-full font-poppins text-xs">

                                                <span class=" text-blue-600">Published</span>
                                            </div>
                                        </div>

                                    </div>
                                </div>

                                <!-- Anyalytic  -->
                                <div
                                    class="flex max-md:flex-col justify-between max-md:justify-center items-center border-gray-200 pr-1 pl-1">
                                    <div class="flex-1 max-md:flex-auto">
                                        <div class="flex items-center mb-1.5 font-medium">
                                            <span class="">Domain Rating</span>
                                        </div>
                                        <div class="flex items-center font-medium">


                                            <span class="">50</span>
                                        </div>
                                    </div>
                                </div>
                                <!-- end anyalytics -->
                            </div>
                        </div>
                    </div>
                </div>
                <!-- end similar part   -->


                <!-- grid section start  -->
                <div class="rounded-xl border mt-4 p-4 mb-4 border-solid border-gray-200">


                    <div
                        class="grid grid-cols-6 gap-4 font-poppins text-sm max-md:text-center  max-md:grid-cols-3 max-md:p-0">

                        <!-- Status -->

                        <div
                            class="flex max-md:flex-col items-center justify-between max-md:justify-center border-r border-solid border-gray-200  pr-1">
                            <div class="flex-1 max-md:flex-auto">
                                <div class=" text-black font-semibold">
                                    Published
                                </div>
                                <div class="text-gray-600 text-xs" id="total_publish_${obj.slug_id}">
                                </div>
                            </div>
                        </div>
                        <div
                            class="flex max-md:flex-col items-center justify-between max-md:justify-center border-r border-solid border-gray-200  pr-1">
                            <div class="flex-1 max-md:flex-auto">
                                <div class=" text-black font-semibold">
                                    Draft
                                </div>
                                <div class="text-gray-600 text-xs" id="total_draft_${obj.slug_id}" >
                                </div>
                            </div>
                        </div>
                        <div
                            class="flex max-md:flex-col items-center justify-between max-md:justify-center border-r border-solid border-gray-200  pr-1">
                            <div class="flex-1 max-md:flex-auto">
                                <div class=" text-black font-semibold">
                                    Rating
                                </div>
                                <div class="text-gray-600 text-xs">20
                                </div>
                            </div>
                        </div>

                        <div
                            class="flex max-md:flex-col items-center justify-between max-md:justify-center border-r border-solid border-gray-200  pr-1">
                            <div class="flex-1 max-md:flex-auto">
                                <div class=" text-black font-semibold">
                                    Scheduled
                                </div>
                                <div class="text-gray-600 text-xs" id="total_scheduled_${obj.slug_id}">
                                </div>
                            </div>
                        </div>
                        <div
                            class="flex max-md:flex-col items-center justify-between max-md:justify-center border-r border-solid border-gray-200  pr-1">
                            <div class="flex-1 max-md:flex-auto">
                                <div class=" text-black font-semibold">
                                    Authority
                                </div>
                                <div class="text-gray-600 text-xs">31
                                </div>
                            </div>
                        </div>
                        <!-- Status -->
                        <div
                            class="flex max-md:flex-col items-center justify-between max-md:justify-center  pr-1">
                            <div class="flex-1 max-md:flex-auto">
                                <div class=" text-black font-semibold">
                                    Score
                                </div>
                                <div class="text-gray-600 text-xs">60
                                </div>
                            </div>
                        </div>
                        <!-- Status -->

                    </div>

                </div>
                <!-- end grid section  -->

                <!-- Manager Start  -->
                <div
                    class="flex md:flex-row flex-col md:space-x-4 space-y-4 md:space-y-0 mt-4 w-full">
                    <div class="w-full md:w-[350px] 2xl:max-w-full">

                        <div class="rounded-xl border  p-4  border-solid border-gray-200">


                            <div
                                class="grid grid-cols-3 gap-4 font-poppins text-sm max-md:text-center  max-md:grid-cols-3 max-md:p-0">

                                <!-- Status -->

                                <div
                                    class="flex max-md:flex-col items-center justify-between max-md:justify-center border-r border-solid border-gray-200  pr-1">
                                    <div class="flex-1 max-md:flex-auto">
                                        <div class=" text-black font-semibold">
                                            Published
                                        </div>
                                        <div class="text-gray-600 text-xs">40
                                        </div>
                                    </div>
                                </div>
                                <div
                                    class="flex max-md:flex-col items-center justify-between max-md:justify-center border-r border-solid border-gray-200  pr-1">
                                    <div class="flex-1 max-md:flex-auto">
                                        <div class=" text-black font-semibold">
                                            Draft
                                        </div>
                                        <div class="text-gray-600 text-xs">30
                                        </div>
                                    </div>
                                </div>
                                <div
                                    class="flex max-md:flex-col items-center justify-between max-md:justify-center">
                                    <div class="flex-1 max-md:flex-auto">
                                        <div class=" text-black font-semibold">
                                            Rating
                                        </div>
                                        <div class="text-gray-600 text-xs">20
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>

                    </div>
                    <div class="w-full max-w-full md:max-w-[208px] 2xl:max-w-full ">

                        <div class="rounded-xl border  p-4 border-solid border-gray-200">
                            <div
                                class="grid grid-cols-2 gap-4 font-poppins text-sm max-md:text-center  max-md:grid-cols-1 max-md:p-0">
                                <div
                                    class="flex max-md:flex-col items-center justify-between max-md:justify-center">
                                    <div class="flex-1 max-md:flex-auto">
                                        <div class=" text-black font-semibold">
                                            Manager
                                        </div>
                                        <div class="text-gray-600 text-xs">
                                            <div class="flex items-center  2xl:pb-0 -space-x-3">
                                            ${managerImageElements}   
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div
                                    class="flex max-md:flex-col items-center justify-between max-md:justify-center">
                                    <div class="flex-1 max-md:flex-auto">
                                        <div class=" text-black font-semibold">
                                            Writer
                                        </div>
                                        <div class="text-gray-600 text-xs">
                                            <div class="flex items-center  2xl:pb-0 -space-x-3">
                                               ${writerImageElements}   
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>


                    </div>
                </div>
                <!-- End Manager  -->
            </div>
            <div class="w-full md:w-1/2 py-4">

                <div class="border-gray-200 p-4 border border-solid rounded-xl">

                    <div class="flex flex-col   lg:flex-row items-center justify-between gap-4 ">

                        <!-- Left Side: Title Section -->
                        <div>

                            <img src="${page_url}static/frontendApp/assets/images/webmaster-logo.png" alt="" srcset="">
                        </div>

                        <!-- Right Side: Buttons and Search -->
                        <div
                            class="flex  items-center gap-2 max-md:flex-wrap max-md:justify-center  ">
                            <!-- Add Article Button -->
                            <div class="flex font-poppins hidden" data-permission="update_domain, update_domain">
                               <!-- update -->
                                <a href="${update_page_url}${obj.slug_id}" class="mr-2 hidden" data-permission="update_domain" >
                                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <rect width="32" height="32" rx="16" fill="#EAECF0"></rect>
                                        <path
                                            d="M14.9533 20.2467C14.8533 20.2467 14.76 20.22 14.6733 20.16C14.5333 20.0667 14.4533 19.9133 14.4533 19.7467C14.4533 19.6467 14.4467 19.54 14.4333 19.4333C14.3733 18.96 14.16 18.5467 13.8 18.1867C13.44 17.8267 12.9933 17.6 12.5133 17.54C12.4333 17.5333 12.32 17.5267 12.2133 17.5333C12.04 17.5467 11.88 17.4733 11.78 17.3333C11.68 17.2 11.6533 17.02 11.7067 16.86C11.8067 16.5867 11.9533 16.34 12.1267 16.14L13.1533 14.8467C14.92 12.64 18.5 9.98667 21.12 8.93333C21.6733 8.72 22.2667 8.84667 22.6733 9.24667C23.0933 9.66667 23.22 10.2667 23 10.8133C21.9467 13.44 19.3 17.0133 17.0933 18.78L15.78 19.8333C15.5333 20.0133 15.3333 20.1267 15.1333 20.2067C15.08 20.2333 15.0133 20.2467 14.9533 20.2467ZM13.0267 16.6267C13.5867 16.7733 14.0867 17.0667 14.5067 17.4867C14.9267 17.9 15.2067 18.38 15.3467 18.9133L16.4733 18.0067C18.5667 16.3333 21.08 12.94 22.0733 10.4467C22.1733 10.2 22.0333 10.0267 21.9667 9.96667C21.92 9.92 21.7467 9.77333 21.48 9.87333C19 10.8733 15.6067 13.3867 13.9267 15.48L13.0267 16.6267Z"
                                            fill="#292D32"></path>
                                        <path
                                            d="M10.7206 23.1665C10.2206 23.1665 9.74056 22.9665 9.38056 22.6065C8.96723 22.1932 8.76723 21.6199 8.8339 21.0332L9.0139 19.3932C9.18723 17.7665 10.5206 16.5599 12.1739 16.5265C12.3006 16.5199 12.4672 16.5265 12.6206 16.5399C13.3472 16.6332 13.9939 16.9599 14.5139 17.4799C15.0272 17.9932 15.3339 18.6065 15.4272 19.2932C15.4472 19.4399 15.4606 19.5999 15.4606 19.7399C15.4606 20.6199 15.1206 21.4399 14.5072 22.0599C13.9939 22.5665 13.3339 22.8799 12.5872 22.9732L10.9406 23.1532C10.8672 23.1599 10.7939 23.1665 10.7206 23.1665ZM12.3006 17.5332C12.2739 17.5332 12.2406 17.5332 12.2139 17.5332C11.2072 17.5532 10.1406 18.2399 10.0072 19.5065L9.82723 21.1465C9.7939 21.4265 9.8939 21.6999 10.0872 21.8999C10.2806 22.0932 10.5539 22.1932 10.8272 22.1599L12.4672 21.9799C12.9806 21.9132 13.4406 21.6999 13.7872 21.3532C14.2139 20.9265 14.4539 20.3532 14.4539 19.7399C14.4539 19.6399 14.4472 19.5332 14.4339 19.4265C14.3739 18.9532 14.1606 18.5399 13.8006 18.1799C13.4406 17.8199 12.9939 17.5932 12.5139 17.5332C12.4606 17.5332 12.3806 17.5332 12.3006 17.5332Z"
                                            fill="#292D32"></path>
                                        <path
                                            d="M17.4933 18.1467C17.22 18.1467 16.9933 17.92 16.9933 17.6467C16.9933 16.18 15.8 14.9933 14.34 14.9933C14.0667 14.9933 13.84 14.7667 13.84 14.4933C13.84 14.22 14.06 13.9933 14.3333 13.9933C16.3467 13.9933 17.9867 15.6333 17.9867 17.6467C17.9933 17.9267 17.7667 18.1467 17.4933 18.1467Z"
                                            fill="#292D32"></path>
                                    </svg>
                                </a>
                                <!-- view -->
                                <a href="${detail_domain_page_url}${obj.slug_id}" class="mr-2 hidden" data-permission="detail_domain">
                                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <rect width="32" height="32" rx="16" fill="#EAECF0"></rect>
                                        <path
                                        d="M16 18.8867C14.4067 18.8867 13.1133 17.5933 13.1133 16C13.1133 14.4067 14.4067 13.1133 16 13.1133C17.5933 13.1133 18.8867 14.4067 18.8867 16C18.8867 17.5933 17.5933 18.8867 16 18.8867ZM16 14.1133C14.96 14.1133 14.1133 14.96 14.1133 16C14.1133 17.04 14.96 17.8867 16 17.8867C17.04 17.8867 17.8867 17.04 17.8867 16C17.8867 14.96 17.04 14.1133 16 14.1133Z"
                                        fill="#292D32"></path>
                                        <path
                                        d="M15.9997 22.0135C13.4931 22.0135 11.1264 20.5468 9.49973 18.0002C8.79306 16.9002 8.79306 15.1068 9.49973 14.0001C11.1331 11.4535 13.4997 9.98682 15.9997 9.98682C18.4997 9.98682 20.8664 11.4535 22.4931 14.0001C23.1997 15.1001 23.1997 16.8935 22.4931 18.0002C20.8664 20.5468 18.4997 22.0135 15.9997 22.0135ZM15.9997 10.9868C13.8464 10.9868 11.7864 12.2801 10.3464 14.5402C9.84639 15.3202 9.84639 16.6801 10.3464 17.4601C11.7864 19.7201 13.8464 21.0135 15.9997 21.0135C18.1531 21.0135 20.2131 19.7201 21.6531 17.4601C22.1531 16.6801 22.1531 15.3202 21.6531 14.5402C20.2131 12.2801 18.1531 10.9868 15.9997 10.9868Z"
                                        fill="#292D32"></path>
                                    </svg>                        
                                </a>
                                <!-- delete -->
                                <a href="#" class="mr-2 hidden" data-permission="delete_domain" onclick="${delete_function_name}('${obj.slug_id}')">
                                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <rect width="32" height="32" rx="16" fill="#EAECF0"></rect>
                                        <path
                                            d="M22 12.4867C21.9867 12.4867 21.9667 12.4867 21.9467 12.4867C18.42 12.1333 14.9 12 11.4133 12.3533L10.0533 12.4867C9.77334 12.5133 9.52667 12.3133 9.5 12.0333C9.47334 11.7533 9.67334 11.5133 9.94667 11.4867L11.3067 11.3533C14.8533 10.9933 18.4467 11.1333 22.0467 11.4867C22.32 11.5133 22.52 11.76 22.4933 12.0333C22.4733 12.2933 22.2533 12.4867 22 12.4867Z"
                                            fill="#E64646"></path>
                                        <path
                                            d="M13.6667 11.8133C13.64 11.8133 13.6133 11.8133 13.58 11.8067C13.3133 11.76 13.1267 11.5 13.1733 11.2333L13.32 10.36C13.4267 9.72 13.5733 8.83333 15.1267 8.83333H16.8733C18.4333 8.83333 18.58 9.75333 18.68 10.3667L18.8267 11.2333C18.8733 11.5067 18.6867 11.7667 18.42 11.8067C18.1467 11.8533 17.8867 11.6667 17.8467 11.4L17.7 10.5333C17.6067 9.95333 17.5867 9.84 16.88 9.84H15.1333C14.4267 9.84 14.4133 9.93333 14.3133 10.5267L14.16 11.3933C14.12 11.64 13.9067 11.8133 13.6667 11.8133Z"
                                            fill="#E64646"></path>
                                        <path
                                            d="M18.14 23.1667H13.86C11.5333 23.1667 11.44 21.88 11.3667 20.84L10.9333 14.1267C10.9133 13.8533 11.1267 13.6133 11.4 13.5933C11.68 13.58 11.9133 13.7867 11.9333 14.06L12.3667 20.7733C12.44 21.7867 12.4667 22.1667 13.86 22.1667H18.14C19.54 22.1667 19.5667 21.7867 19.6333 20.7733L20.0667 14.06C20.0867 13.7867 20.3267 13.58 20.6 13.5933C20.8733 13.6133 21.0867 13.8467 21.0667 14.1267L20.6333 20.84C20.56 21.88 20.4667 23.1667 18.14 23.1667Z"
                                            fill="#E64646"></path>
                                        <path
                                            d="M17.1067 19.5H14.8867C14.6133 19.5 14.3867 19.2733 14.3867 19C14.3867 18.7267 14.6133 18.5 14.8867 18.5H17.1067C17.38 18.5 17.6067 18.7267 17.6067 19C17.6067 19.2733 17.38 19.5 17.1067 19.5Z"
                                            fill="#E64646"></path>
                                        <path
                                            d="M17.6667 16.8333H14.3333C14.06 16.8333 13.8333 16.6067 13.8333 16.3333C13.8333 16.06 14.06 15.8333 14.3333 15.8333H17.6667C17.94 15.8333 18.1667 16.06 18.1667 16.3333C18.1667 16.6067 17.94 16.8333 17.6667 16.8333Z"
                                            fill="#E64646"></path>
                                    </svg>
                                </a>
                            </div>
                        </div>
                    </div>



                    <div class="relative mt-4 rounded-xl">
                        <div
                            class="flex md:flex-row flex-col gap-2 md:space-x-4 space-y-4 md:space-y-0 w-full">
                            <div class="w-full md:w-1/2">
                                <div class="bg-gray-50 p-4 rounded-lg">
                                    <div class="flex justify-between items-start">
                                        <div>
                                            <h6
                                                class="font-normal font-poppins text-gray-500 text-sm">
                                                Latest Traffic
                                            </h6>
                                            <h5
                                                class="font-semibold text-gray-900 text-xl leading-8" id="total_traffic_${obj.slug_id}">
                                                
                                            </h5>
                                        </div>
                                        <span
                                            class="hidden flex items-center px-2.5 py-1 rounded-full font-bold text-xs">
                                            <svg class="mr-1 w-2 h-2" viewBox="0 0 7 7" fill="none"
                                                xmlns="http://www.w3.org/2000/svg">
                                                <path
                                                    d="M4.62402 6.10095C4.69941 6.02556 4.74559 5.9208 4.74544 5.80575V5.75511C4.74544 5.52471 4.55892 5.33819 4.32882 5.33848L2.05236 5.33848L5.90324 1.48761C6.06587 1.32497 6.06587 1.06099 5.90324 0.898351C5.7406 0.735716 5.47662 0.735716 5.31398 0.898351L1.4631 4.74923V2.47277C1.4631 2.24237 1.27659 2.05585 1.04648 2.05615H0.995843C0.765444 2.05615 0.578927 2.24266 0.579221 2.47277V5.80575C0.579221 6.03614 0.765739 6.22266 0.995843 6.22237H4.32882C4.44402 6.22237 4.54864 6.17634 4.62402 6.10095Z"
                                                    fill="white" />
                                            </svg>
                                            May 2024
                                        </span>
                                    </div>
                                </div>

                                <div class="block bg-gray-50 p-4 rounded-lg w-chart w-full">
                                    <div class="!w-full" id="traffic_chart_${obj.slug_id}"></div>

                                </div>

                            </div>

                            <div class="w-full md:w-1/2">

                                <div
                                    class="flex justify-between items-start bg-gray-50 p-4 rounded-lg">
                                    <div>
                                        <h6 class="font-normal font-poppins text-gray-500 text-sm">
                                            Impressions
                                        </h6>
                                        <h5 class="font-semibold text-gray-900 text-xl leading-8" id="total_impressions_${obj.slug_id}">
                                            
                                        </h5>
                                    </div>
                                    <span
                                        class="flex hidden items-center px-2.5 py-1 rounded-full font-bold text-xs">
                                        <svg class="mr-1 w-2 h-2" viewBox="0 0 7 7" fill="none"
                                            xmlns="http://www.w3.org/2000/svg">
                                            <path
                                                d="M4.62402 6.10095C4.69941 6.02556 4.74559 5.9208 4.74544 5.80575V5.75511C4.74544 5.52471 4.55892 5.33819 4.32882 5.33848L2.05236 5.33848L5.90324 1.48761C6.06587 1.32497 6.06587 1.06099 5.90324 0.898351C5.7406 0.735716 5.47662 0.735716 5.31398 0.898351L1.4631 4.74923V2.47277C1.4631 2.24237 1.27659 2.05585 1.04648 2.05615H0.995843C0.765444 2.05615 0.578927 2.24266 0.579221 2.47277V5.80575C0.579221 6.03614 0.765739 6.22266 0.995843 6.22237H4.32882C4.44402 6.22237 4.54864 6.17634 4.62402 6.10095Z"
                                                fill="white" />
                                        </svg>
                                        May 2024
                                    </span>
                                </div>

                                <div class="block bg-gray-50 p-4 rounded-lg w-chart w-full">
                                    <div class="!w-full" id="impressions_chart_${obj.slug_id}"></div>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </div>
    </div>
        `;
        main_div_id.appendChild(div);
        
    });
handle_permissions();

}



