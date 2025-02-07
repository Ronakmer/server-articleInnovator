async function detail_domain_chart(domain_console_data, domain_analytics_data, domain_article_data, slug_id) {

    const domain_console_data_obj = await domain_console_data; // Await the promise
    const domain_analytics_data_obj = await domain_analytics_data; // Await the promise
    const domain_article_data_obj = await domain_article_data; // Await the promise

    // domain_console total data 
    const total_impressionss = document.getElementById(`total_impressions`);
    const total_click = document.getElementById(`total_click`);
    const total_ctr = document.getElementById(`total_ctr`);
    const total_position = document.getElementById(`total_position`);

    total_impressionss.innerText = domain_console_data_obj.metrics_data.aggregates.total_impressions || '';
    total_click.innerText = domain_console_data_obj.metrics_data.aggregates.total_clicks || '';
    total_ctr.innerText = domain_console_data_obj.metrics_data.aggregates.total_ctr || '';
    total_position.innerText = domain_console_data_obj.metrics_data.aggregates.total_position || '';
    
    // domain_analytics total data 
    const total_traffic = document.getElementById(`total_traffic`);
    const total_new_user = document.getElementById(`total_new_user`);
    const total_average_time = document.getElementById(`total_average_time`);

    total_traffic.innerText = domain_analytics_data_obj.metrics_data.aggregates.total_traffics || '';
    total_new_user.innerText = domain_analytics_data_obj.metrics_data.aggregates.total_new_users || '';
    total_average_time.innerText = domain_analytics_data_obj.metrics_data.aggregates.total_average_time || '';
    
    //article_data
    const total_article = document.getElementById(`total_article`);
    total_article.innerText = domain_article_data_obj.metrics_data.total_articles || '';


    // Extract data from domain_console_data
    const consoleClicks = Object.values(domain_console_data_obj.metrics_data.metrics_by_date.clicks);
    const consoleImpressions = Object.values(domain_console_data_obj.metrics_data.metrics_by_date.impressions);
    const consoleCtr = Object.values(domain_console_data_obj.metrics_data.metrics_by_date.ctr);
    const consolePosition = Object.values(domain_console_data_obj.metrics_data.metrics_by_date.position);
    const consoleDates = Object.keys(domain_console_data_obj.metrics_data.metrics_by_date.clicks);
    
    // Extract data from domain_analytics_data
    const traffics = Object.values(domain_analytics_data_obj.metrics_data.traffics_by_date);
    const newUsers = Object.values(domain_analytics_data_obj.metrics_data.new_users_by_date);
    const averageTime = Object.values(domain_analytics_data_obj.metrics_data.average_time_by_date);
    
    const articleData = Object.values(domain_article_data_obj.metrics_data.article_by_date_dict);

    // Format dates for x-axis
    const formattedDates = consoleDates.map(date => new Date(date).toLocaleDateString('en-GB'));

    // Chart options
    const chartOptions = {
        series: [
            {
                name: 'Clicks',
                data: consoleClicks,
                color: '#FF6384'
            },
            {
                name: 'Impressions',
                data: consoleImpressions,
                color: '#36A2EB'
            },
            {
                name: 'Traffics',
                data: traffics,
                color: '#4BC0C0'
            },
            {
                name: 'New Users',
                data: newUsers,
                color: '#9966FF'
            },
            {
                name: 'CTR',
                data: consoleCtr,
                color: '#FFCE56'
            },
            {
                name: 'Position',
                data: consolePosition,
                color: '#36A2EB'
            },
            {
                name: 'Average Time',
                data: averageTime,
                color: '#FF9F40'
            },
            {
                name: 'Article',
                data: articleData,
                color: '#AF9444'
            }
        ],
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
            },
        },
        xaxis: {
            categories: formattedDates,
        },
        yaxis: {
            min: 0,
            tickAmount: 5
        },
        legend: {
            position: 'top',
            horizontalAlign: 'left',
            offsetY: 0,
            itemMargin: {
                horizontal: 10
            }
        }
    };

    // Render the chart
    const chart = new ApexCharts(document.querySelector("#detail_domain_chart"), chartOptions);
    chart.render();
}




