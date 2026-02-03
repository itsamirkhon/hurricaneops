document.addEventListener('DOMContentLoaded', () => {
    loadAnalytics();
});

async function loadAnalytics() {
    try {
        const response = await fetch('/api/analytics/dashboard');
        const data = await response.json();

        updateKPIs(data);
        renderCharts(data);
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

function updateKPIs(data) {
    document.getElementById('total-incidents').textContent = data.incidents.total;
    document.getElementById('active-incidents').textContent = `${data.incidents.active} Active`;
    document.getElementById('avg-resolution').textContent = data.incidents.avg_resolution_time_mins;
    document.getElementById('utilization-rate').textContent = `${data.assets.utilization_rate}%`;
    document.getElementById('deployed-count').textContent = `${data.assets.deployed} Deployed`;
}

function renderCharts(data) {
    // 1. Incidents by Type (Doughnut)
    const typeCtx = document.getElementById('typeChart').getContext('2d');
    const typeLabels = Object.keys(data.incidents.by_type);
    const typeValues = Object.values(data.incidents.by_type);

    new Chart(typeCtx, {
        type: 'doughnut',
        data: {
            labels: typeLabels.map(l => l.replace('_', ' ').toUpperCase()),
            datasets: [{
                data: typeValues,
                backgroundColor: [
                    '#ef4444', '#f97316', '#eab308', '#3b82f6', '#8b5cf6', '#ec4899'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { color: '#9ca3af' } }
            }
        }
    });

    // 2. Resource vs Needs (Bar - Mocked for demo visualization of potential vs actual)
    const resCtx = document.getElementById('resourceChart').getContext('2d');
    new Chart(resCtx, {
        type: 'bar',
        data: {
            labels: ['Rescue', 'Medical', 'Transport', 'Logistics'],
            datasets: [
                {
                    label: 'Deployed',
                    data: [data.assets.deployed, Math.floor(data.assets.deployed * 0.5), Math.floor(data.assets.deployed * 0.3), 2],
                    backgroundColor: '#3b82f6'
                },
                {
                    label: 'Available',
                    data: [data.assets.total - data.assets.deployed, 5, 8, 3],
                    backgroundColor: '#22c55e'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: '#374151' }, ticks: { color: '#9ca3af' } },
                x: { grid: { display: false }, ticks: { color: '#9ca3af' } }
            },
            plugins: {
                legend: { labels: { color: '#9ca3af' } }
            }
        }
    });
}
