import React, { useState } from 'react';
import { Treemap, Tooltip } from 'recharts';
import { scaleLinear } from 'd3-scale';
import data from '../data/connected_clones.json';

// Color scaler to give heat map effect
const colorScale = scaleLinear()
  .domain([0, 100])
  .range(['#ffffff', '#a80000']);

  const colorScaleDepth = scaleLinear()
  .domain([0, 100])
  .range(['#f169ff', '#55285a']);

const TreeMap = () => {
  // Keeps track of currently clicked on file and updates if its clicked on
  const [selectedNode, setSelectedNode] = useState(false);

  // Custom node rendering
  // Uused for the heat map effect on each file rectangle 
  const heatedCell = (props) => {
    const { x, y, width, height, name, poc, clones, depth } = props;
    // Check if current node and selected node are the same 
    console.log("selectedNode: ", selectedNode);
    const isSelected = selectedNode && selectedNode.name === name; 
    console.log("Related: ", selectedNode.related);
    console.log("Name ", name);
    const isRelated = selectedNode && selectedNode.related.includes(name);
    const fillColor = isSelected
      ? '#0000ff' // Blue for selected node
      : isRelated
      ? '#00a800' // Green for related nodes
      : colorScale(poc);

    return (
      // On first click make the rect the selected, on second click, unselect
      <g onClick={() =>  {
        if (isSelected) {
          setSelectedNode(false);
        } else {
          setSelectedNode({ name, related: clones || [] });
        }
      }}>
        <rect
          x={x}
          y={y}
          width={width}
          height={height}
          style={{
            fill: fillColor,
            stroke: colorScaleDepth(depth),
            cursor: 'pointer',
          }}
        />
        {width > 40 && height > 20 && (
          <text
            x={x + width / 2}
            y={y + height / 2}
            textAnchor="middle"
            fill="#000000" 
            stroke="#000"
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
      >
      <Tooltip
        content={({ payload }) => {
          if (payload && payload.length) {
            const { size, poc } = payload[0].payload;
            console.log(payload);
            return (
              <div style={{ backgroundColor: '#fff', padding: '5px', border: '1px solid #ccc' }}>
                <p>{`Size: ${size} LOC`}</p>
                <p>{`Clones: ${poc}%`}</p>
              </div>
            );
          }
          return null;
        }}
      />
      </Treemap>
    </div>
  );
};

export default TreeMap;
