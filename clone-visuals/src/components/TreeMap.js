import React, { useState } from 'react';
import { Treemap, Tooltip } from 'recharts';
import { scaleLinear } from 'd3-scale';
import data from '../data/data2.json';

// Color scaler to give heat map effect
const colorScale = scaleLinear()
  .domain([0, 100])
  .range(['#ffffff', '#a80000']);

const TreeMap = () => {
  // Keeps track of currently clicked on file and updates if its clicked on
  const [selectedNode, setSelectedNode] = useState(null);

  // Custom node rendering
  // Uused for the heat map effect on each file rectangle 
  const heatedCell = (props) => {
    console.log('heatedCell props:', props); // Add this line for debugging
    const { x, y, width, height, name, poc, clones } = props;
    const isSelected = selectedNode && selectedNode.name === name; // Check if current node and selected node are the same 
    const isRelated = selectedNode && selectedNode.related.includes(name);
    const fillColor = isSelected
      ? '#0000ff' // Blue for selected node
      : isRelated
      ? '#00a800' // Green for related nodes
      : colorScale(poc);

    return (
      <g onClick={() => setSelectedNode({ name, related: clones || [] })}>
        <rect
          x={x}
          y={y}
          width={width}
          height={height}
          style={{
            fill: fillColor,
            stroke: '#fff',
            cursor: 'pointer',
          }}
        />
        {width > 40 && height > 20 && (
          <text
            x={x + width / 2}
            y={y + height / 2}
            textAnchor="middle"
            fill="#000"
            fontSize={12}
          >
            {name}
          </text>
        )}
      </g>
    );
  };

  return (
    <div>
      <Treemap
        width={800}
        height={400}
        data={data}
        dataKey="size"
        stroke="#fff"
        content={heatedCell}
      />
      <Tooltip
        content={({ payload }) => {
          // if (!payload) {
          //   console.error('Payload is undefined:', props); // Add this line for debugging
          //   return null;
          // }
          if (payload && payload.length) {
            const { name, size, poc } = payload[0].payload;
            return (
              <div style={{ backgroundColor: '#fff', padding: '5px', border: '1px solid #ccc' }}>
                <p>{`Name: ${name}`}</p>
                <p>{`Size: ${size} LOC`}</p>
                <p>{`Clones: ${poc}%`}</p>
              </div>
            );
          }
          return null;
        }}
      />
    </div>
  );
};

export default TreeMap;
