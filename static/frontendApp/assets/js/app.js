/*============Sidebar===========*/
const setup = () => {
  function getSidebarStateFromLocalStorage() {
    // if it already there, use it
    if (window.localStorage.getItem("isSidebarOpen")) {
      return JSON.parse(window.localStorage.getItem("isSidebarOpen"));
    }

    // else return the initial state you want
    return false;
  }

  function setSidebarStateToLocalStorage(value) {
    window.localStorage.setItem("isSidebarOpen", value);
  }

  return {
    loading: true,
    isSidebarOpen: getSidebarStateFromLocalStorage(),
    toggleSidbarMenu() {
      this.isSidebarOpen = !this.isSidebarOpen;
      setSidebarStateToLocalStorage(this.isSidebarOpen);
    },
    isSettingsPanelOpen: false,
    isSearchBoxOpen: false,
  };
};
/*============Dropdown===========*/
const dorpdrown = document.querySelector(".dropdown-toggle");
const dropsvg = document.querySelector(".dropdownsvg");

dorpdrown.addEventListener("click", function () {
  dorpdrown.classList.toggle("active");
});
const randomColor = "#" + ((1 << 24) * Math.random() | 0).toString(16);
document.documentElement.style.setProperty('--main-bg-color', randomColor);


/*============Charts===========*/

// index-page-chart 
var optionsindex = {
  colors: ["#1D4ED8", "#0EA5E9", "#FBBF24"],
  series: [
    {
      name: "PRODUCT A",
      data: [44, 55, 41, 67, 22, 43, 20],
    },
    {
      name: "PRODUCT B",
      data: [13, 23, 20, 8, 13, 27, 40],
    },
    {
      name: "PRODUCT C",
      data: [11, 17, 15, 15, 21, 14, 18],
    },
  ],
  chart: {
    type: "bar",
    width: '100%',
    height: '200',
    stacked: true,
    toolbar: {
      show: false,
    },
    zoom: {
      enabled: false,
    },
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        legend: {
          position: "bottom",
          offsetX: -10,
          offsetY: 0,
        },
      },
    },
  ],
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 10,
      dataLabels: {
        enabled: false,
      },
    },
  },
  dataLabels: {
    enabled: false,
  },
  grid: {
    show: false,
  },

  yaxis: {
    show: false,
  },
  xaxis: {
    type: "",
    labels: {
      style: {
        color: 'red',
        fontSize: '12px',
        fontWeight: 500,
      },
    },
    categories: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    axisTicks: {
      show: false,
    },
    axisBorder: {
      show: false,
    },
  },
  legend: {
    show: false,
  },
  fill: {
    colors: ['#1D4ED8', '#0EA5E9', '#FBBF24']
  }
};

// Check if the element with ID "index-chart" exists
var indexChartElement = document.querySelector("#index-chart");

if (indexChartElement) {
  // Proceed with rendering the chart if the element is found
  var chartindex = new ApexCharts(indexChartElement, optionsindex);
  chartindex.render();
}


//employee-page-charts

var optionsemp = {
  series: [

    {
      name: 'Employee',
      data: [20, 20, 25, 15, 35, 23, 30, 22, 25, 20, 15, 25],
    },
    {
      name: 'Intern',
      data: [38, 32, 32, 27, 32, 35, 38, 38, 40, 35, 38, 25],
    }
  ],
  chart: {
    type: 'area',
    width: '100%',
    height: '100%',
    stacked: true,
    foreColor: "#6B7280",
    toolbar: {
      show: false
    }
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        legend: {
          position: "bottom",
          offsetX: -10,
          offsetY: 0,
        },
      },
    },
  ],
  title: {
    text: 'Over all Employee Performance',
    align: 'left',
    margin: 0,
    offsetX: 0,
    offsetY: 0,
    floating: false,
    style: {
      fontSize: '16px',
      fontWeight: '600',
      fontFamily: 'inter',
      color: '#111827',
    },
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'straight',
    width: [0, 0],
  },
  colors: ['#0EA5E9', '#FBBF24'],
  fill: {
    type: 'solid',
    colors: ['#0EA5E9', '#FBBF24'],
  },
  legend: {
    position: 'top',
    horizontalAlign: 'right',
    markers: {
      width: 12,
      height: 12,
      radius: 4,
    },
    labels: {
      colors: "#111827",
      useSeriesColors: false
    },
    style: {
      position: 'absolute',
      top: '10px',
      right: '20px'
    }
  },
  xaxis: {
    categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    axisTicks: {
      show: false,
    }
  },
  yaxis: {
    min: 0,
    max: 70,
    tickAmount: 3,
    labels: {
      formatter: (value) => value.toFixed(0) + '%',
    },
  },
};

// Check if the element with ID "emp-chart-1" exists
var empChartElement = document.querySelector("#emp-chart-1");

if (empChartElement) {
  // Proceed with rendering the chart if the element is found
  var chartemployee = new ApexCharts(empChartElement, optionsemp);
  chartemployee.render();
}

//horizontal bar chart-no-2
var optionsProgress1 = {
  chart: {
    height: 80,
    width: '100%',
    type: "bar",
    stacked: true,
    sparkline: {
      enabled: true
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: "20px",
      width: '100%',
      borderRadius: 5,
      colors: {
        backgroundBarColors: ["#C7D2FE"]
      }
    }
  },
  colors: ["#4F46E5"],
  series: [
    {
      name: "Process 1",
      data: [44]
    }
  ],
  title: {
    floating: true,
    offsetX: -10,
    offsetY: 5,
    text: "Floyd Miles",
    style: {
      fontSize: '12px',
      fontWeight: 'medium',
      fontFamily: 'inter',
      color: '#6B7280'
    },
  },

  tooltip: {
    enabled: false
  },
  xaxis: {
    categories: ["Floyd Miles"]
  },
  yaxis: {
    max: 100
  },
  fill: {
    opacity: 1
  }
};

// Check if the element with ID "progress1" exists
var progress1Element = document.querySelector("#progress1");

if (progress1Element) {
  // Proceed with rendering the chart if the element is found
  var chartProgress1 = new ApexCharts(progress1Element, optionsProgress1);
  chartProgress1.render();
}
var optionsProgress2 = {
  chart: {
    height: 80,
    width: '100%',
    type: "bar",
    stacked: true,
    sparkline: {
      enabled: true
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      barHeight: "20px",
      borderRadius: 5,
      colors: {
        backgroundBarColors: ["#C7D2FE"]
      }
    }
  },
  colors: ["#4F46E5"],

  series: [
    {
      name: "Savannah Nguyen",
      data: [80]
    }
  ],
  title: {
    floating: true,
    offsetX: -10,
    offsetY: 5,
    text: "Savannah Nguyen",
    style: {
      fontSize: '12px',
      fontWeight: 'medium',
      fontFamily: 'inter',
      color: '#6B7280'
    },
  },
  tooltip: {
    enabled: false
  },
  xaxis: {
    categories: ["Process 2"]
  },
  yaxis: {
    max: 100
  },
  fill: {
    opacity: 1,
  }
};

// Check if the element with ID "progress2" exists
var progress2Element = document.querySelector("#progress2");

if (progress2Element) {
  // Proceed with rendering the chart if the element is found
  var chartProgress2 = new ApexCharts(progress2Element, optionsProgress2);
  chartProgress2.render();
} 
var optionsProgress3 = {
  chart: {
    height: 80,
    width: '100%',
    type: "bar",
    stacked: true,
    sparkline: {
      enabled: true
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      width: '100%',
      barHeight: "20px",
      borderRadius: 5,
      colors: {
        backgroundBarColors: ["#C7D2FE"]
      }
    }
  },
  colors: ["#4F46E5"],
  stroke: {
    width: 0
  },
  series: [
    {
      name: "Cameron Williamson",
      data: [74]
    }
  ],
  fill: {
    opacity: 1,

  },
  title: {
    floating: true,
    offsetX: -10,
    offsetY: 5,
    text: "Cameron Williamson",
    style: {
      fontSize: '12px',
      fontWeight: 'medium',
      fontFamily: 'inter',
      color: '#6B7280'
    },
  },

  tooltip: {
    enabled: false
  },
  xaxis: {
    categories: ["Cameron Williamson"]
  },
  yaxis: {
    max: 100
  }
};
// Check if the element with ID "progress3" exists
var progress3Element = document.querySelector("#progress3");

if (progress3Element) {
  // Proceed with rendering the chart if the element is found
  var chartProgress3 = new ApexCharts(progress3Element, optionsProgress3);
  chartProgress3.render();
}

//Attendances page charts

var optionsAttendance = {
  series: [
    {
      name: 'Actual',
      data: [
        {
          x: '9 AM',
          y: 45,
          goals: [
            {
              name: 'Expected',
              value: 45,
              strokeHeight: 2,
              strokeColor: "#4F46E5",
            }
          ]
        },

        {
          x: '10 AM',
          y: 50,
          goals: [
            {
              name: 'Expected',
              value: 50,
              strokeHeight: 2,
              strokeColor: '#4F46E5'
            }
          ]
        },
        {
          x: '11 AM',
          y: 39,
          goals: [
            {
              name: 'Expected',
              value: 39,
              strokeHeight: 2,
              strokeColor: '#4F46E5'
            }
          ]
        },
        {
          x: '12 PM',
          y: 73,
          goals: [
            {
              name: 'Expected',
              value: 73,
              strokeHeight: 2,
              strokeColor: '#4F46E5'
            }
          ]
        },
        {
          x: '1 PM',
          y: 69,
          goals: [
            {
              name: 'Expected',
              value: 69,
              strokeHeight: 2,
              strokeColor: '#4F46E5'
            }
          ]
        },
        {
          x: '2 PM',
          y: 74,
          goals: [
            {
              name: 'Expected',
              value: 74,
              strokeHeight: 2,
              strokeColor: '#4F46E5'
            }
          ]
        },
        {
          x: '3 PM',
          y: 62,
          goals: [
            {
              name: 'Expected',
              value: 62,
              strokeHeight: 2,
              strokeColor: '#4F46E5'
            }
          ]
        },
        {
          x: '4 PM',
          y: 78,
          goals: [
            {
              name: 'Expected',
              value: 78,
              strokeHeight: 2,
              strokeColor: '#4F46E5'
            }
          ]
        },
        {
          x: '5 PM',
          y: 62,
          goals: [
            {
              name: 'Expected',
              value: 62,
              strokeHeight: 2,
              strokeColor: '#4F46E5'
            }
          ]
        }
      ]
    }
  ],
  chart: {
    height: "100%",
    width: "100%",
    type: 'bar',
    toolbar: {
      show: false,
      tools: {
        download: false // <== line to add
      }
    },
  },
  title: {
    text: 'Employee Performance',
    align: 'left',
    margin: 0,
    offsetX: 0,
    offsetY: 0,
    floating: false,
    style: {
      fontSize: '16px',
      fontWeight: '600',
      fontFamily: 'inter',
      color: '#111827',
    },
  },
  plotOptions: {
    bar: {
      columnWidth: '100%'

    },
  },
  yaxis: {
    min: 0,
    max: 100,
    tickAmount: 3,
    labels: {
      formatter: (value) => value.toFixed(0) + '%',
    },
  },
  fill: {
    type: 'gradient',
    gradient: {
      shade: 'light',
      type: "vertical",
      shadeIntensity: 0.5,
      gradientToColors: undefined, // optional, if not defined - uses the shades of same color in series
      inverseColors: true,
      opacityFrom: 0.7,
      opacityTo: 0.3,
      stops: [5, 50, 100],
      colorStops: []
    }
  },
  colors: ['#4F46E5', '#EEF2FF'],
  dataLabels: {
    enabled: false
  },

  legend: {
    show: true,
    position: "top",
    horizontalAlign: 'right',
    showForSingleSeries: true,
    customLegendItems: ['Yesterday', 'Today'],
    markers: {
      fillColors: ['#C7D2FE', '#775DD0']
    }
  }

};

// Check if the element with ID "Attendances-chart-1" exists
var attendanceChartElement = document.querySelector("#Attendances-chart-1");

if (attendanceChartElement) {
  // Proceed with rendering the chart if the element is found
  var chartAtten = new ApexCharts(attendanceChartElement, optionsAttendance);
  chartAtten.render();
}
// chart-no-2

var options = {
  chart: {
    height: 280,
    type: "radialBar"

  },

  series: [67],
  plotOptions: {
    radialBar: {
      startAngle: -90,
      endAngle: 90,

      track: {
        background: "#EEF2FF",
        strokeWidth: '97%',
        margin: 15, // margin is in pixels

      },
      dataLabels: {
        showOn: "always",
        name: {
          offsetY: -10,
          show: true,
          color: "#111827",
          fontSize: "13px"
        },
        value: {
          color: "#111827",
          fontSize: "30px",
          show: true
        }
      }
    }
  },
  fill: {
    opacity: 1.5,
    colors: ['#4F46E5'],
    type: 'gradient',
    gradient: {
      gradientToColors: ['#4F46E5'],
      shadeIntensity: 1,
      opacityFrom: 1,
      opacityTo: 2,
      stops: [0, 50, 100],
      inverseColors: false
    },
  },

  stroke: {
    lineCap: "round",
  },
  labels: [""]
};

// var chart = new ApexCharts(document.querySelector("#Attendances-chart-2"), options); 
// chart.render();

// Leave page charts

var dataSet = [
  [
    [new Date("01/01/2014").getTime(), 200],
    [new Date("02/12/2014").getTime(), 270],
    [new Date("03/01/2014").getTime(), 330],
    [new Date("04/01/2014").getTime(), 390],
    [new Date("05/01/2014").getTime(), 420],
    [new Date("06/01/2014").getTime(), 510],
    [new Date("07/01/2014").getTime(), 580],
    [new Date("08/01/2014").getTime(), 670],
    [new Date("09/15/2014").getTime(), 740],
    [new Date("10/01/2014").getTime(), 790],
    [new Date("11/01/2014").getTime(), 820],
    [new Date("12/01/2014").getTime(), 880],
     [new Date("12/31/2014").getTime(), 880]
  ],
  [
    [new Date("01/01/2014").getTime(), 200],
    [new Date("02/10/2014").getTime(), 260],
    [new Date("03/01/2014").getTime(), 330],
    [new Date("04/01/2014").getTime(), 400],
    [new Date("05/01/2014").getTime(), 520],
    [new Date("06/01/2014").getTime(), 580],
    [new Date("07/01/2014").getTime(), 620],
    [new Date("08/01/2014").getTime(), 710],
    [new Date("09/01/2014").getTime(), 740]
  ]
];

// Define the chart options
var options = {
  series: [{
    name: 'Employee',
    data: dataSet[0],
    color: '#C7D2FE',
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        inverseColors: false,
        opacityFrom: 0.45,
        opacityTo: 0.95,
        stops: [20, 100, 100, 100]
      },
    },
  }, {
    name: 'Intern',
    data: dataSet[1],
    color: '#4F46E5'
  }],
  chart: {
    type: 'area',
    stacked: false,
    height: 350,
    zoom: {
      enabled: false
    },
     toolbar: {
      show: false,
     },
  },
  dataLabels: {
    enabled: false
  },
  markers: {
    size: 0,
  },
  yaxis: {
    labels: {
      style: {
        colors: '#8e8da4',
      },
      offsetX: 0,
      formatter: function(val) {
        return (val / 10).toFixed(0);
      },
    },
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false
    },
   
  },
  xaxis: {
    type: 'datetime',
    tickAmount: 12,
    min: new Date("01/01/2014").getTime(),
    max: new Date("12/31/2014").getTime(),
    labels: {
      rotate: -15,
      rotateAlways: true,
      formatter: function(val, timestamp) {
        return moment(new Date(timestamp)).format("MMM")
      }
    },
    
  },
  title: {
    text: '',
    align: 'left',
    offsetX: 14
  },
  tooltip: {
     enabled: false,
    shared: true,
  },
  legend: {
    position: 'top',
    horizontalAlign: 'right',
    offsetX: -10
  }
};

// Render the chart
// var chart = new ApexCharts(document.querySelector("#leave-chart"), options);
// chart.render();


// chart- no -2

var options = {
  colors: ["#f59e0b", "#4f46e5", "#22d3ee"],
  series: [
    {
      name: "Paid Leave",
      data: [44, 55, 41, 67, 22, 43, 20],
    },
    {
      name: "Sick Leave",
      data: [13, 23, 20, 8, 13, 27, 40],
    },
    {
      name: "Casual Leave",
      data: [11, 17, 15, 15, 21, 14, 18],
    },
  ],
  chart: {
    type: "bar",
    width: '100%',
    height: '300',
    stacked: true,
    toolbar: {
      show: false,
    },
    zoom: {
      enabled: false,
    },
  },
  responsive: [
    {
      breakpoint: 480,
      options: {
        legend: {
          position: "bottom",
          offsetX: -10,
          offsetY: 0,
         
        },
      },
    },
  ],
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 10,
      dataLabels: {
        enabled: false,
      },
    },
  },
  dataLabels: {
    enabled: false,
  },
  grid: {
    show: false,
  },

  yaxis: {
    show: false,
  },
  xaxis: {
    type: "",
    labels: {
      style: {
        color: 'red',
        fontSize: '12px',
        fontWeight: 500,
      },
    },
    categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
    axisTicks: {
      show: false,
    },
    axisBorder: {
      show: false,
    },
  },
  legend: {
    show: true,
  },
  fill: {
    opacity: 1,
  },
};

// var chart = new ApexCharts(
//   document.querySelector("#stack-bar-chart"),
//   options
// );
// chart.render();

var stack_bar_chart = document.querySelector("#stack-bar-chart")
if(stack_bar_chart){
  var chart = new ApexCharts(
    options
  );
  chart.render();
  
}


//payroll page charts

var options = {
  series: [15, 25, 60],
  labels: ['Pending', 'Unpaid', 'Successfully Paid'],
  colors: ['#F97316', '#F59E0B', '#6366F1'],
  dataLabels: {
    enabled: false,
  },
  chart: {
    type: 'donut',
    height: 270,
    labels: {
      show: false,
    }
  },
  legend: {
    show: false,
  },
  plotOptions: {
    pie: {
      donut: {
        background: '#FFF',
        size: '80%',
        labels: {
          show: true,
          name: 'aa',
          
        }
      }
    },
  },
};

// Check if the element exists before rendering the chart
var chartElement = document.querySelector("#stack-bar-chart");
if (chartElement) {
  var chart = new ApexCharts(chartElement, options);
  chart.render();
}

// payroll chart-no-2

var options = {
  series: [{
    name: 'Revenue',
    color: '#4F46E5',
    data: [70000, 63000, 60000, 65000, 78000, 66000, 52000, 59000]
  }, {
    name: 'Expenses',
    color: '#EF4444',
    data: [22000, 38000, 44000, 35000, 44000, 38000, 31000, 43000]
  }],
  chart: {
    type: 'line',
    height: 300,
    toolbar: {
      show: false,
    }
  },
  stroke: {
    curve: 'stepline',
  },
  dataLabels: {
    enabled: false
  },
  title: {
    text: 'Comparison',
    align: 'left'
  },
  markers: {
    hover: {
      sizeOffset: 4
    }
  },
  xaxis: {
    categories: [
      'Jan 21', 'Jan 22', 'Jan 23', 'Jan 24', 'Jan 25', 'Jan 26', 'Jan 27', 'Jan 28',
    ]
  },
  yaxis: {
    labels: {
      formatter: (val) => {
        return val / 1000 + 'K'
      }
    }
  },

  legend: {
    show: true,
    position: 'top',
    horizontalAlign: 'left',
    fontSize: '16px',
    fontFamily: 'inter',
    fontWeight: 600,
    inverseOrder: false,
    customLegendItems: [],
    offsetX: 0,
    offsetY: 0,
    labels: {
      useSeriesColors: true
    },
    markers: {
      width: 12,
      height: 12,
      strokeWidth: 0,
      strokeColor: '#fff',
      radius: 12,
      offsetX: 0,
      offsetY: 0
    },
    itemMargin: {
      horizontal: 5,
      vertical: 0
    },
    onItemClick: {
      toggleDataSeries: true
    },
    onItemHover: {
      highlightDataSeries: true
    },
  }

};
// Check if the element with id 'payroll-chart-2' exists
var chartElement = document.querySelector("#payroll-chart-2");
if (chartElement) {
  var chart = new ApexCharts(chartElement, options);
  chart.render();
}

// payroll chart-no-3

var options = {
  series: [
    {
      name: 'Employee',
      group: 'budget',
      data: [0.54, 0.68, 0.79, 0.43, 0.46, 0.65]
    },

    {
      name: 'Freelancer',
      group: 'budget',
      data: [0.58, 0.75, 0.90, 0.58, 0.55, 0.75, 0.30]
    },

  ],
  chart: {
    type: 'bar',
    height: 290,
    width: '100%',
    stacked: true,
    toolbar: {
      show: false,
    }
  },
  stroke: {
    width: 1,
    colors: ['#fff']
  },

  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 10,

    }
  },
  dataLabels: {
    enabled: false,
  },
  xaxis: {
    categories: [
      'mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  },
  yaxis: {
    min: 0.1,
    max: 0.9,
    tickAmount: 2,
    opposite: true,
    labels: {
      formatter: (val) => {
        return val / 1 + 'K'
      }
    }
  },
  fill: {
    opacity: 1,
  },
  colors: ['#22C55E', '#DCFCE7'],
  legend: {
    position: 'bottom',
    horizontalAlign: 'right'
  }
};

// Check if the element with id 'payroll-chart-3' exists
var chartElement = document.querySelector("#payroll-chart-3");
if (chartElement) {
  var chart = new ApexCharts(chartElement, options);
  chart.render();
} 