import React, { useState, useEffect } from 'react';
import { Treemap, Tooltip, ResponsiveContainer } from 'recharts';
import { scaleLinear } from 'd3-scale';
import data from '../finalData/treeMap.json';

// Color scalers for heat map and depth with new palette
const colorScale = scaleLinear()
  .domain([0, 100])
  .range(['#f6e9d5', '#b33951']); // Beige to deep red

const colorScaleDepth = scaleLinear()
  .domain([0, 100])
  .range(['#e3dac9', '#586ba4']); // Light tan to muted blue

const TreeMap = ({ selectedCloneClass }) => {
  const [selectedNode, setSelectedNode] = useState(false);

  useEffect(() => {
    if (selectedCloneClass) {
      setSelectedNode({ related: selectedCloneClass });
    } else {
      setSelectedNode(false);
    }
  }, [selectedCloneClass]);

  const heatedCell = (props) => {
    const { x, y, width, height, name, poc, clones, children, path, depth } = props;
    const isSelected = selectedNode && selectedNode.name === name;
    const isRelated = selectedNode && selectedNode.related.includes(path);

    const fillColor = isSelected
      ? '#003f5c' // Highlight selected node with dark blue
      : isRelated
      ? '#ffa600' // Highlight related nodes with orange
      : depth === 1
      ? colorScaleDepth(poc) // Parent nodes
      : colorScale(poc); // Child nodes

    const borderColor = children ? '#000000' : '#ffffff';
    const borderWidth = children ? 2 : 1;

    return (
      <g
        onClick={(e) => {
          e.stopPropagation();
          if (isSelected) {
            setSelectedNode(false);
          } else {
            setSelectedNode({ name, related: clones || [] });
          }
        }}
      >
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
      </g>
    );
  };

  return (
    <div
      className="treemap-container"
      style={{
        border: '2px solid #ccc', // Thin border around the treemap
        borderRadius: '4px', // Slightly rounded corners
        padding: '10px', // Padding around the element
        background: '#f4f1ea', // Warm neutral background
        height: '100%', // Ensures it takes the full height of the parent
      }}
    >
      
      <ResponsiveContainer width="100%" height="100%">
        <Treemap
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
                  <div
                    style={{
                      backgroundColor: '#fff',
                      padding: '5px',
                      border: '1px solid #ccc',
                    }}
                  >
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
      </ResponsiveContainer>
    </div>
  );
};

export default TreeMap;
