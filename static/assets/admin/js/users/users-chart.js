const ctx = document.getElementById('users_chart');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: chartData.user_labels,   
        datasets: [{
            label: 'Users',
            data: chartData.user_counts,
            borderWidth: 1,
            backgroundColor: '#0A012E',
            borderColor: '#0A012E',
            barThickness: 60,
            maxBarThickness: 70,
        }]
    },
    options: {
        responsive: true,
        plugins: {
            datalabels: {
                anchor: 'center',
                align: 'center',
                color: '#fff',
                formatter: function(value) {
                    return value;
                },
                font: {
                    weight: 'bold'
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    },
    plugins: [ChartDataLabels]
});



const revenueCtx = document.getElementById('revenue_chart');

const allLabels = ['Daily', 'Weekly', 'Monthly'];
const allData   = [revenueData.daily, revenueData.weekly, revenueData.monthly];
const allColors = ['#0A012E', '#1a0f5e', '#2d1a8e'];

const filtered = allLabels.reduce((acc, label, i) => {
    if (allData[i] > 0) {
        acc.labels.push(label);
        acc.data.push(allData[i]);
        acc.colors.push(allColors[i]);
    }
    return acc;
}, { labels: [], data: [], colors: [] });

let revenueChart = new Chart(revenueCtx, {
    type: 'pie',
    data: {
        labels: filtered.labels,
        datasets: [{
            data: filtered.data,
            backgroundColor: filtered.colors,
            borderColor: ['#fff', '#fff', '#fff'],
            borderWidth: 2,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            datalabels: {
                color: '#fff',
                formatter: function(value, context) {
                    const label = context.chart.data.labels[context.dataIndex];
                    return label + '\n$' + value;
                },
                font: {
                    weight: 'bold'
                }
            },
            legend: {
                display: true,
                position: 'bottom'
            }
        }
    },
    plugins: [ChartDataLabels]
});