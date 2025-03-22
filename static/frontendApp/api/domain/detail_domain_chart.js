


async function detail_domain_chart(domain_console_data, domain_analytics_data, domain_article_data, slug_id) {
    try {
        // 1. Resolve all promises in parallel for better performance
        const [consoleData, analyticsData, articleData] = await Promise.all([
            domain_console_data,
            domain_analytics_data,
            domain_article_data
        ]);

        // 2. Update DOM elements with a helper function to reduce repetition
        updateDomElement('total_impressions', consoleData?.metrics_data?.aggregates?.total_impressions);
        updateDomElement('total_click', consoleData?.metrics_data?.aggregates?.total_clicks);
        updateDomElement('total_ctr', consoleData?.metrics_data?.aggregates?.total_ctr);
        updateDomElement('total_position', consoleData?.metrics_data?.aggregates?.total_position);

        updateDomElement('total_traffic', analyticsData?.metrics_data?.aggregates?.total_traffics);
        updateDomElement('total_new_user', analyticsData?.metrics_data?.aggregates?.total_new_users);
        updateDomElement('total_average_time', analyticsData?.metrics_data?.aggregates?.total_average_time);
        
        updateDomElement('total_article', articleData?.metrics_data?.total_articles ?? 'N/A');

        // 3. Extract chart data with defensive programming
        const metricsByDate = consoleData?.metrics_data?.metrics_by_date || {};
        const dates = Object.keys(metricsByDate.clicks || {});
        const formattedDates = dates.map(date => new Date(date).toLocaleDateString('en-GB'));

        // 4. Create chart series array with helper function
        const chartSeries = [
            createSeries('Clicks', metricsByDate.clicks, '#FF6384'),
            createSeries('Impressions', metricsByDate.impressions, '#36A2EB'),
            createSeries('Traffics', analyticsData?.metrics_data?.traffics_by_date, '#4BC0C0'),
            createSeries('New Users', analyticsData?.metrics_data?.new_users_by_date, '#9966FF'),
            createSeries('CTR', metricsByDate.ctr, '#FFCE56'),
            createSeries('Position', metricsByDate.position, '#36A2EB'),
            createSeries('Average Time', analyticsData?.metrics_data?.average_time_by_date, '#FF9F40'),
            createSeries('Article', articleData?.metrics_data?.article_by_date_dict, '#AF9444')
        ];

        // 5. Configure and render chart
        const chart = new ApexCharts(
            document.querySelector("#detail_domain_chart"), 
            createChartOptions(chartSeries, formattedDates)
        );
        
        chart.render();
        
    } catch (error) {
        console.error('Error rendering domain chart:', error);
        // Optionally display error message to user
        document.querySelector("#detail_domain_chart").innerHTML = 
            '<div class="alert alert-danger">Failed to load chart data</div>';
    }
}

// Helper functions to improve code organization and reduce repetition
function updateDomElement(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.innerText = value ?? 'N/A';
    }
}

function createSeries(name, dataObj, color) {
    return {
        name,
        data: Object.values(dataObj || {}),
        color
    };
}

function createChartOptions(series, categories) {
    return {
        series,
        chart: {
            height: 400,
            type: 'line',
            zoom: { enabled: false },
            toolbar: { show: false }
        },
        dataLabels: { enabled: false },
        stroke: {
            curve: 'smooth',
            width: 3
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'],
                opacity: 0.5
            }
        },
        xaxis: { categories },
        yaxis: {
            min: 0,
            tickAmount: 5
        },
        legend: {
            position: 'top',
            horizontalAlign: 'left',
            offsetY: 0,
            itemMargin: { horizontal: 10 }
        }
    };
}