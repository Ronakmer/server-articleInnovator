


// article_clicks_chart chart
async function article_clicks_chart(article_console_data, slug_id) {
    article_console_data.then((response) => {

        if (response && response.metrics_data && response.metrics_data.aggregates) {
            const total_clickss = document.getElementById(`total_clicks_${slug_id}`);
            if(total_clickss){
                total_clickss.innerText = response.metrics_data.aggregates.total_clicks || '' ;
            }
        }


        // Check if metrics_by_date or clicks data is null or undefined, and return early if true
        if (!response || !response.metrics_data || !response.metrics_data.metrics_by_date || !response.metrics_data.metrics_by_date.clicks) {
            console.log("Skipping data due to missing metrics_by_date or clicks.");
            return; // Exit early if data is missing
        }


        if (response && response.metrics_data) {
            const percentageData = response.metrics_data.percentage_data || {};
            const clicksChange = percentageData.hasOwnProperty('clicks_change') ? percentageData.clicks_change : null;
        
            const value = clicksChange && typeof clicksChange.value === "number" ? clicksChange.value : 0.0;
            const trend = clicksChange && typeof clicksChange.trend === "string" ? clicksChange.trend : null;
        
            const percentageText = document.getElementById(`clicks_percentage_value_${slug_id}`);
            const percentageIcon = document.getElementById(`clicks_percentage_icon_${slug_id}`);
        
            if (percentageText) {
                percentageText.innerText = `${value.toFixed(1)}%`;
            }
        
            if (percentageIcon) {
                if (trend === 'up') {
                    percentageIcon.innerHTML = `
                        <svg width="10" height="10" viewBox="0 0 7 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M4.62402 6.10095C4.69941 6.02556 4.74559 5.9208 4.74544 5.80575V5.75511C4.74544 5.52471 4.55892 5.33819 4.32882 5.33848L2.05236 5.33848L5.90324 1.48761C6.06587 1.32497 6.06587 1.06099 5.90324 0.898351C5.7406 0.735716 5.47662 0.735716 5.31398 0.898351L1.4631 4.74923V2.47277C1.4631 2.24237 1.27659 2.05585 1.04648 2.05615H0.995843C0.765444 2.05615 0.578927 2.24266 0.579221 2.47277V5.80575C0.579221 6.03614 0.765739 6.22266 0.995843 6.22237H4.32882C4.44402 6.22237 4.54864 6.17634 4.62402 6.10095Z" fill="green"/>
                        </svg>
                    `;
                } else if (trend === 'down') {
                    percentageIcon.innerHTML = `
                        <svg width="10" height="10" viewBox="0 0 7 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M2.37598 0.899052C2.30059 0.974437 2.25441 1.0792 2.25456 1.19425V1.24489C2.25456 1.47529 2.44108 1.66181 2.67118 1.66152L4.94764 1.66152L1.09676 5.51239C0.934131 5.67503 0.934131 5.93901 1.09676 6.10165C1.2594 6.26428 1.52338 6.26428 1.68602 6.10165L5.5369 2.25077V4.52723C5.5369 4.75763 5.72341 4.94415 5.95352 4.94385H6.00416C6.23456 4.94385 6.42107 4.75734 6.42078 4.52723V1.19425C6.42078 0.963857 6.23426 0.777337 6.00416 0.777629H2.67118C2.55598 0.777629 2.45136 0.823661 2.37598 0.899052Z" fill="red"/>
                        </svg>
                    `;
                } else {
                    percentageIcon.innerHTML = ''; // no icon for neutral or missing trend
                }
            }
        }
        
        



        const chart_clicks = document.getElementById(`clicks_chart_${slug_id}`);
        if (chart_clicks) {
            // Extract dates and values from the clicks_by_date_dict
            const clicksDates = Object.keys(response.metrics_data.metrics_by_date.clicks); // Modify based on your actual data structure
            const clicksData = Object.values(response.metrics_data.metrics_by_date.clicks); // Modify based on your actual data structure

            // clicks Chart Configuration
            var clicksOptions = {
                series: [
                    {
                        data: clicksData, // Use actual data extracted from 
                    },
                ],
                chart: {
                    type: "area",
                    width: "100%", // Full width
                    height: 50,
                    background: "transparent",
                    sparkline: {
                        enabled: true,
                    },
                    dropShadow: {
                        enabled: true,
                        top: 1,
                        left: 1,
                        blur: 2,
                        // color: "#58BD7D", // Green shadow color
                        color: "#f97316", 
                        opacity: 0.7,
                    },
                    zoom: {
                        enabled: false,
                    },
                },
                dataLabels: {
                    enabled: false,
                },
                markers: {
                    colors: ["#FFFFFF"],
                },
                stroke: {
                    curve: "smooth",
                    width: 1,
                    // colors: ["#58BD7D"], // Green border color
                    colors: ["#f97316"], 
                },
                fill: {
                    type: "gradient",
                    gradient: {
                        shadeIntensity: 1,
                        type: "vertical",
                        colorStops: [
                            [
                                {
                                    offset: 0,
                                    // color: "#58BD7D", // Green gradient start
                                    color: "#f97316",
                                    opacity: 0.1,
                                },
                                {
                                    offset: 70,
                                    // color: "#58BD7D", // Green gradient mid
                                    color: "#f97316", 
                                    opacity: 0.05,
                                },
                                {
                                    offset: 97,
                                    // color: "#58BD7D", // Green gradient end
                                    // color: "#f97316", 
                                    opacity: 0.01,
                                },
                            ],
                        ],
                    },
                },
                xaxis: {
                    categories: clicksDates, // Use the dates for x-axis labels
                    axisBorder: {
                        show: false,
                    },
                    axisTicks: {
                        show: false,
                    },
                    labels: {
                        show: true, // Show x-axis labels if desired
                    },
                },
                yaxis: {
                    labels: {
                        show: true, // Show y-axis labels if desired
                    },
                },
                grid: {
                    padding: {
                        top: 0,
                        bottom: 0,
                        left: 0,
                        right: 0,
                    },
                },
                legend: {
                    show: false, // Hide legend for sparkline
                },
                theme: {
                    mode: "dark",
                },
            };

            // Initialize the chart (assuming you're using ApexCharts)
            const clicksCharts = new ApexCharts(chart_clicks, clicksOptions);
            clicksCharts.render();
        }
    })
    .catch(error => {
        console.error("Error fetching domain data for", error);
    });
}
