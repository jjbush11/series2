import React, { useState } from 'react';
import TreeMap from './TreeMap';
import SortedBarChart from './SortedBarChart';
import ImpactScore from './ImpactScore';
import sharedClones from '../testData/shared_clones'

export default function Dashboard() {
  const [selectedCloneClass, setSelectedCloneClass] = useState(null);

  const handleBarClick = (classID) => {
    setSelectedCloneClass(sharedClones[classID]);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <h1>Clone Detection Dashboard</h1>
      <TreeMap selectedCloneClass={selectedCloneClass} />
      <div className="side-by-side-container">
        <SortedBarChart onBarClick={handleBarClick} />
        <ImpactScore />
      </div>
      
    </div>
  );
}
