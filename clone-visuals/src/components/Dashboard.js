import React, { useState } from 'react';
import TreeMap from './TreeMap';
import SortedBarChart from './SortedBarChart';
import ImpactScore from './ImpactScore';
import sharedClones from '../finalData/sharedClones.json'

export default function Dashboard() {
  const [selectedClone, setSelectedClone] = useState(null);

  const handleBarClick = (clone) => {
    setSelectedClone(clone);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <h1>Clone Detection Dashboard</h1>
      <TreeMap selectedCloneClass={sharedClones[selectedClone]} />
      {/* <div className="side-by-side-container"> */}
      <div>
        <SortedBarChart onBarClick={handleBarClick} />
        <ImpactScore selectedClone={selectedClone} />
        
      </div>
      
    </div>
  );
}
