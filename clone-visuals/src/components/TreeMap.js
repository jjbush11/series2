import React, { useState, useEffect } from 'react';
import { Treemap, Tooltip } from 'recharts';
import { scaleLinear } from 'd3-scale';
import data from '../finalData/treeMap.json';

// Color scaler to give heat map effect
const colorScale = scaleLinear()
  .domain([0, 100])
  .range(['#ffffff', '#a80000']);

  const colorScaleDepth = scaleLinear()
  .domain([0, 100])
  .range(['#f169ff', '#ff6726']);

const TreeMap = ({ selectedCloneClass }) => {
  // Keeps track of currently clicked on file and updates if its clicked on
  const [selectedNode, setSelectedNode] = useState(false);

  useEffect(() => {
    if (selectedCloneClass) {
      setSelectedNode({ related: selectedCloneClass });
    } else {
      setSelectedNode(false);
    }
  }, [selectedCloneClass]);

  // Custom node rendering
  // Used for the heat map effect on each file rectangle 
  const heatedCell = (props) => {
    const { x, y, width, height, name, poc, clones, children, path } = props;
    // Check if current node and selected node are the same 
    const isSelected = selectedNode && selectedNode.name === name; 
    const isRelated = selectedNode && selectedNode.related.includes(path);
    const fillColor = isSelected
      ? '#0000ff' // Blue for selected node
      : isRelated
      ? '#00a800' // Green for related nodes
      : colorScale(poc);

    const borderColor = children ? '#000000' : '#ffffff'; //depth === 1 ? '#000000' : '#ffffff';
    const borderWidth = children ? 10 : 1; // Thicker border for parent nodes

    return (
      // On first click make the rect the selected, on second click, unselect
      <g onClick={(e) =>  {
        e.stopPropagation();
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
            stroke: borderColor,
            strokeWidth: borderWidth,
            cursor: 'pointer',
          }}
        />
        {/* {width > 40 && height > 20 && (
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
        )} */}
      </g>
    );
  };

  return (
    <div className='treemap-container'>
      <Treemap
        width={1000}
        height={600}
        data={data}
        dataKey="size"
        stroke="#000"
        content={heatedCell}
      >
      <Tooltip
        content={({ payload }) => {
          if (payload && payload.length) {
            const { name, size, poc, path } = payload[0].payload;
            return (
              <div style={{ backgroundColor: '#fff', padding: '5px', border: '1px solid #ccc' }}>
                <p>{`Name: ${name}`}</p>
                <p>{`Size: ${size} LOC`}</p>
                <p>{`Clones: ${poc.toFixed(2)}%`}</p>
                <p>{`Path: ${path}`}</p>
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
