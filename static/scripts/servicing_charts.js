// servicing_charts.js

// Function to load bar plots
function loadBarPlots(servicingData) {
    servicingData.forEach(function(data, index) {
        var divId = 'servicing_graph-container' + (index + 1);
        var div = document.getElementById(divId);
        Plotly.newPlot(div, JSON.parse(data));
    });
}

function updateChartSize() {
    const graphContainers = document.querySelectorAll('.graph-container');

    for (const container of graphContainers) {
        const chartId = container.id; // Get the chart container ID
        const chart = document.getElementById(chartId); // Find the chart element

        // Set chart width to occupy full width of the container
        const containerWidth = container.clientWidth;
        Plotly.relayout(chart, { width: containerWidth });
    }
}

// Initial call to set correct width on page load
updateChartSize();

// Update chart size on window resize
window.addEventListener('resize', updateChartSize);
