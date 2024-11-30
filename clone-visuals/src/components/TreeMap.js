import React from 'react';
import { Treemap, Tooltip } from 'recharts';
import data from '../data/data.json';
import { scaleLinear } from 'd3-scale';



// Color scaler to give heat map effect
const colorScale = scaleLinear()
  .domain([0, 100])
  .range(['#ffffff', '#a80000'])

const heatedCell = (props) => {
  const { x, y, width, height, name, poc } = props;
  return (
    <g>
      <rect
        x = {x}
        y = {y}
        width = {width}
        height={height}
        style={{
          fill: colorScale(poc),
          stroke: '#fff',
        }}
        
      />
      {/* Center the text in the cell */}
      <text x={x + width / 2} y={y + height / 2} textAnchor="middle" fill="#000000" stroke="#000">
        {name}
      </text>
    </g>
  )
}

export default function TreeMap() {
  return (
    <Treemap
      width={500}
      height={300}
      data={data}
      dataKey="size"
      stroke="#fff"
      content={heatedCell}
    >
      <Tooltip
        content={({ payload }) => {
          if (payload && payload.length) {
            const { name, size, poc } = payload[0].payload;
            console.log(payload);
            return (
              <div style={{ backgroundColor: '#fff', padding: '5px', border: '1px solid #ccc' }}>
                <p>{`Size: ${size}`}</p>
                <p>{`Clones: ${poc}%`}</p>
              </div>
            );
          }
          return null;
        }}
      />
     </Treemap>
  );
}
