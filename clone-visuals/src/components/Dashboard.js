import React, { useState } from 'react';
import TreeMap from './TreeMap';
import SortedBarChart from './SortedBarChart';
import ImpactScore from './ImpactScore';
import sharedClones from '../finalData/sharedClones.json';

export default function Dashboard() {
  const [selectedClone, setSelectedClone] = useState(null);

  const handleBarClick = (clone) => {
    setSelectedClone(clone);
  };

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr', // Two main columns
        gridTemplateRows: 'auto 2fr 1fr', // Header, main content, footer
        gap: '20px',
        height: '100vh',
        padding: '20px',
        boxSizing: 'border-box', // Ensure padding doesn't affect layout
        backgroundColor: '#f4f4f4', // Neutral background
      }}
    >
      {/* Header */}
      <div
        style={{
          gridColumn: '1 / span 2', // Spans both columns
          textAlign: 'center',
          fontSize: '1.5rem',
          fontWeight: 'bold',
          color: '#333',
        }}
      >
        Code Clone Visualization Dashboard
      </div>

      {/* Sorted Bar Chart */}
      <div style={{ gridColumn: '1 / span 1', gridRow: '2 / span 1' }}>
        <SortedBarChart onBarClick={handleBarClick} />
        <div
        style={{
          gridColumn: '1 / span 2', // Spans both columns
          textAlign: 'center',
          fontSize: '1.5rem',
          fontWeight: 'normal',
          color: '#333',
        }}
      >
         Clone Impact per Class
         </div>  
      </div>

{/* TreeMap Visualization */}
<div
  style={{
    gridColumn: '2 / span 1',
    gridRow: '2 / span 1',
    height: '100%', // Ensure it fills the grid cell
    display: 'flex',
    flexDirection: 'column',
  }}
>

  <TreeMap selectedCloneClass={sharedClones[selectedClone]} />

  <div
        style={{
          gridColumn: '1 / span 2', // Spans both columns
          textAlign: 'center',
          fontSize: '1.5rem',
          fontWeight: 'normal',
          color: '#333',
        }}
      >
         TreeMap: Clone Dispersion and Density per file
         </div>   
</div>


      {/* Impact Score */}
      <div
        style={{
          gridColumn: '1 / span 2', // Spans both columns
          gridRow: '3 / span 1',
        }}
      >
        <ImpactScore selectedClone={selectedClone} />
      </div>
    </div>
  );
}
