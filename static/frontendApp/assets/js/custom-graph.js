// chart 1  Clicks
var options = {
  series: [
    {
      data: [10, 20, 15, 30, 35, 30, 45, 59, 30, 35, 25, 29, 15],
    },
  ],
  chart: {
    type: "area",
    // width: "100%",
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
      color: "#FF6838", // Orange shadow color
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
    colors: ["#FF6838"], // Orange border color
  },
  fill: {
    type: "gradient",
    gradient: {
      shadeIntensity: 1,
      type: "vertical",
      colorStops: [
        {
          offset: 0,
          color: "#FF6838", // Orange gradient start
          opacity: 0.1, // Low opacity at the top
        },
        {
          offset: 70,
          color: "#FF6838", // Orange gradient mid
          opacity: 0.05, // Slightly lower opacity as it goes down
        },
        {
          offset: 97,
          color: "#FF6838", // Orange gradient end
          opacity: 0.01, // Almost transparent at the bottom
        },
      ],
    },
  },
  xaxis: {
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
    labels: {
      style: {
        colors: "#aaa",
      },
    },
  },
  yaxis: {
    labels: {
      show: false,
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
    horizontalAlign: "left",
  },
  theme: {
    mode: "dark",
  },
};
// Select the chart container element
var chartElement = document.querySelector("#myChart");

// Example condition: Only render the chart if the element exists
if (chartElement) {
    var chart = new ApexCharts(chartElement, options);
    chart.render();
}




// Traffic Chart Configuration
var trafficOptions = {
  series: [
    {
      data: [20, 35, 25, 40, 50, 45, 60, 70, 55, 65, 50, 60, 40], // Sample data; replace with actual data as needed
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
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
    labels: {
      show: false, // Hide x-axis labels for a cleaner sparkline look
    },
  },
  yaxis: {
    labels: {
      show: false, // Hide y-axis labels
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

// Render the Traffic Chart

// var trafficChart = new ApexCharts(
//   document.querySelector("#Traffics"),
//   trafficOptions,
// );
// trafficChart.render();

// Check if the element with ID "Traffics" exists
var trafficElement = document.querySelector("#Traffics");

if (trafficElement) {
  // Proceed with rendering the chart if the element is found
  var trafficChart = new ApexCharts(trafficElement, trafficOptions);
  trafficChart.render();
}

// Check if the element with ID "Traffics2" exists
var trafficElement2 = document.querySelector("#Traffics2");

if (trafficElement2) {
  // Proceed with rendering the chart if the element is found
  var trafficChart2 = new ApexCharts(trafficElement2, trafficOptions);
  trafficChart2.render();
} 

// Impressions Chart Configuration
var impressionsOptions = {
  series: [
    {
      data: [15, 25, 20, 35, 40, 38, 50, 60, 45, 55, 42, 50, 30], // Sample data; replace with actual data as needed
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
      color: "#FF6838", // Orange shadow color
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
    colors: ["#FF6838"], // Orange border color
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
            color: "#FF6838", // Orange gradient start
            opacity: 0.1,
          },
          {
            offset: 70,
            color: "#FF6838", // Orange gradient mid
            opacity: 0.05,
          },
          {
            offset: 97,
            color: "#FF6838", // Orange gradient end
            opacity: 0.01,
          },
        ],
      ],
    },
  },
  xaxis: {
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
    labels: {
      show: false, // Hide x-axis labels for a cleaner sparkline look
    },
  },
  yaxis: {
    labels: {
      show: false, // Hide y-axis labels
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

// Check if the element with ID "Impressions" exists
var impressionsElement = document.querySelector("#Impressions");

if (impressionsElement) {
  // Proceed with rendering the chart if the element is found
  var impressionsChart = new ApexCharts(impressionsElement, impressionsOptions);
  impressionsChart.render();
}

// Check if the element with ID "myChart2" exists
var impressionsElement2 = document.querySelector("#myChart2");

if (impressionsElement2) {
  // Proceed with rendering the chart if the element is found
  var impressionsChart2 = new ApexCharts(impressionsElement2, impressionsOptions);
  impressionsChart2.render();
}

// Check if the element with ID "Impressions2" exists
var impressions2Element = document.querySelector("#Impressions2");

if (impressions2Element) {
  // Proceed with rendering the chart if the element is found
  var impressionsChart2 = new ApexCharts(impressions2Element, impressionsOptions);
  impressionsChart2.render();
}