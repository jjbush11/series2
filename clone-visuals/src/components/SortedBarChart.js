import React, { useState } from "react";
import { ResponsiveBar } from "@nivo/bar";
import rawData from "../finalData/barChart.json";

const SortedBarChart = ({ onBarClick }) => {
  const [selectedBar, setSelectedBar] = useState(null);

  // Sort data by locCloneProduct in descending order
  const sortedData = [...rawData].sort((a, b) => b.locCloneProduct - a.locCloneProduct);

  return (
    <div
      style={{
        width: "800px", // Fixed width
        margin: "0 auto", // Center horizontally
        height: "500px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "20px",
      }}
    >
      <h2>Sorted LOC Size x Clone Count</h2>
      <ResponsiveBar
        data={sortedData}
        keys={["locCloneProduct"]}
        indexBy="clone"
        margin={{ top: 50, right: 130, bottom: 130, left: 100 }} // Adjust margins for alignment
        padding={0.3}
        valueScale={{ type: "linear" }}
        indexScale={{ type: "band", round: true }}
        colors={({ data }) =>
          data.clone === selectedBar ? "rgb(255, 127, 14)" : "rgb(31, 119, 180)"
        } // Change bar color based on selection
        borderColor={{ from: "color", modifiers: [["darker", 1.6]] }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 90,
          legend: "Class ID",
          legendPosition: "middle",
          legendOffset: 40, // Adjust legend offset
        }}
        axisLeft={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
          legend: "LOC Size x Clone Count",
          legendPosition: "middle",
          legendOffset: -50, // Adjust legend offset
        }}
        tooltip={({ clone, value, data }) => (
          <div
            style={{
              padding: "10px",
              background: "white",
              border: "1px solid #ccc",
              borderRadius: "5px",
            }}
          >
            <strong>{`Class ID: ${data.clone}`}</strong>
            <br />
            {`LOC x Clones: ${value}`}
            <br />
            {`LOC Size: ${data.cloneSize}`}
            <br />
            {`Occurrences: ${data.occurrences}`}
          </div>
        )}
        theme={{
          tooltip: {
            container: {
              background: "#333",
              color: "#ddd",
              fontSize: "14px",
              borderRadius: "5px",
              boxShadow: "0px 3px 9px rgba(0, 0, 0, 0.5)",
            },
          },
        }}
        legends={[
          {
            dataFrom: "keys",
            anchor: "bottom-right",
            direction: "column",
            justify: false,
            translateX: 120,
            translateY: 0,
            itemsSpacing: 2,
            itemWidth: 100,
            itemHeight: 20,
            itemDirection: "left-to-right",
            itemOpacity: 0.85,
            symbolSize: 20,
            effects: [
              {
                on: "hover",
                style: {
                  itemOpacity: 1,
                },
              },
            ],
          },
        ]}
        animate={true}
        motionConfig="wobbly"
        role="application"
        ariaLabel="Bar chart showing LOC size x clone count"
        onClick={(data) => { 
          setSelectedBar(data.indexValue)
          onBarClick(data.indexValue)
        }} // Update selectedBar state on click
      />
    </div>
  );
};

export default SortedBarChart;