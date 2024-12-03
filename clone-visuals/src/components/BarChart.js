import React from "react";
import { Bar } from "react-chartjs-2";
import processedData from "/home/jan/Nextcloud/uni/SEvolution/series2_james/clone-visuals/src/data/data_for_bar_chart.json";

import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const BarChart = () => {
  const labels = processedData.map((item) => item.classID);
  const dataValues = processedData.map((item) => item.locCloneProduct);

  const chartData = {
    labels,
    datasets: [
      {
        label: "LOC Size x Clone Count",
        data: dataValues,
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: true, position: "top" },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            const index = tooltipItem.dataIndex;
            const details = processedData[index];
            return [
              `Class ID: ${details.classID}`,
              `LOC Size: ${details.locSize}`,
              `Occurrences: ${details.occurrences}`,
              `LOC x Clones: ${details.locCloneProduct}`
            ];
          },
        },
      },
    },
    scales: {
      x: { title: { display: true, text: "Class ID" } },
      y: { title: { display: true, text: "LOC Size x Clone Count" } },
    },
  };

  return (
    <div style={{ width: "600px", margin: "0 auto" }}>
      <h2>LOC Size x Clone Count</h2>
      <Bar data={chartData} options={chartOptions} />
    </div>
  );
};

export default BarChart;