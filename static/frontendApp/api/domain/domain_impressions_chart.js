


// domain_impressions_chart chart
async function domain_impressions_chart(domain_console_data, slug_id) {
    
    domain_console_data.then((response) => {
        
        if (response && response.metrics_data && response.metrics_data.aggregates) {
            const total_impressionss = document.getElementById(`total_impressions_${slug_id}`);
            if(total_impressionss){
                total_impressionss.innerText = response.metrics_data.aggregates.total_impressions || '' ;
            }
        }


        // Check if metrics_by_date or clicks data is null or undefined, and return early if true
        if (!response || !response.metrics_data || !response.metrics_data.metrics_by_date || !response.metrics_data.metrics_by_date.clicks) {
            console.log("Skipping data due to missing metrics_by_date or clicks.");
            return; // Exit early if data is missing
        }

        const chart_impressions = document.getElementById(`impressions_chart_${slug_id}`);
        if (chart_impressions) {
            // Extract dates and values from the impressions_by_date_dict
            const impressionsDates = Object.keys(response.metrics_data.metrics_by_date.clicks); // Modify based on your actual data structure
            const impressionsData = Object.values(response.metrics_data.metrics_by_date.clicks); // Modify based on your actual data structure

            // impressions Chart Configuration
            var impressionsOptions = {
                series: [
                    {
                        data: impressionsData, // Use actual data extracted from 
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
                        color: "#58BD7D", // Green shadow color
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
                    colors: ["#58BD7D"], // Green border color
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
                                    color: "#58BD7D", // Green gradient start
                                    opacity: 0.1,
                                },
                                {
                                    offset: 70,
                                    color: "#58BD7D", // Green gradient mid
                                    opacity: 0.05,
                                },
                                {
                                    offset: 97,
                                    color: "#58BD7D", // Green gradient end
                                    opacity: 0.01,
                                },
                            ],
                        ],
                    },
                },
                xaxis: {
                    categories: impressionsDates, // Use the dates for x-axis labels
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
            const impressionsCharts = new ApexCharts(chart_impressions, impressionsOptions);
            impressionsCharts.render();
        }
    })
    .catch(error => {
        console.error("Error fetching domain data for", error);
    });
}
