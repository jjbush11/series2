import React from 'react';
import TreeMap from './TreeMap';
import BarChart from './BarChart';
import SortedBarChart from './SortedBarChart';

export default function Dashboard() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <h1>Clone Detection Dashboard</h1>
      <TreeMap />
      <SortedBarChart />
    </div>
  );
}
