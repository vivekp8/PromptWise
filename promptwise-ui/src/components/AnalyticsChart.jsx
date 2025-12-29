import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import axios from 'axios';

ChartJS.register(ArcElement, Tooltip, Legend);

function AnalyticsChart() {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/feedback/stats')
            .then(res => {
                const stats = res.data.label_distribution;
                const labels = Object.keys(stats);
                const data = Object.values(stats);

                setChartData({
                    labels: labels,
                    datasets: [
                        {
                            label: '# of Prompts',
                            data: data,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.4)',
                                'rgba(54, 162, 235, 0.4)',
                                'rgba(255, 206, 86, 0.4)',
                                'rgba(75, 192, 192, 0.4)',
                                'rgba(153, 102, 255, 0.4)',
                                'rgba(255, 159, 64, 0.4)',
                            ],
                            borderColor: [
                                'rgba(255, 99, 132, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)',
                            ],
                            borderWidth: 1,
                        },
                    ],
                });
            })
            .catch(err => console.error(err));
    }, []);

    if (!chartData) return <div style={{ color: 'gray' }}>Loading stats...</div>;

    return (
        <div className="card" style={{ maxWidth: '400px', margin: '2rem auto', textAlign: 'center' }}>
            <h3>📈 Label Distribution</h3>
            <Pie data={chartData} />
        </div>
    );
}

export default AnalyticsChart;
