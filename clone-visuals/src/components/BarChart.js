import React from 'react';
import { ResponsiveBar } from '@nivo/bar';

const data = [
  { cloneClass: 'Class A', priority: 8 },
  { cloneClass: 'Class B', priority: 5 },
  { cloneClass: 'Class C', priority: 3 },
];

export default function BarChart() {
  return (
    <div style={{ height: 400 }}>
      <ResponsiveBar
        data={data}
        keys={['priority']}
        indexBy="cloneClass"
        margin={{ top: 20, right: 20, bottom: 50, left: 50 }}
        padding={0.3}
        colors={{ scheme: 'nivo' }}
        borderColor={{ from: 'color', modifiers: [['darker', 1.6]] }}
      />
    </div>
  );
}
