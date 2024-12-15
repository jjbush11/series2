import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { darcula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import sharedClones from '../finalData/sharedClones.json';
import codeExamples from '../finalData/codeExample.json';
import barChart from '../finalData/barChart.json';

const ImpactScore = ({ selectedClone }) => {
  if (!selectedClone) {
    return (
      <div
        style={{
          backgroundColor: '#f4f4f4', // Match the grey background
          padding: '20px',
          borderRadius: '8px',
          border: '1px solid #ccc',
        }}
      >
        Select a clone to see its impact score.
      </div>
    );
  }

  // Find the cloneID from barChart.json
  const cloneData = barChart.find((item) => item.clone === selectedClone);
  const cloneID = cloneData ? cloneData.cloneID : null;

  // Find the paths from sharedClones.json
  const paths = sharedClones[selectedClone] || [];

  // Find the code example from codeExample.json
  const codeExample = codeExamples.find((item) => item.clone === selectedClone);

  return (
    <div
      style={{
        backgroundColor: '#f4f4f4', // Match the grey background
        padding: '20px',
        borderRadius: '8px',
        border: '1px solid #ccc',
        display: 'flex',
        gap: '20px',
      }}
    >
      <div style={{ flex: 1 }}>
        <h3>List of files with clone instances:</h3>
        <p>
          <strong>Clone ID:</strong> {cloneID}
        </p>
        <p>
          <strong>Paths:</strong>
        </p>
        <ul>
          {paths.map((path, index) => (
            <li key={index}>{path}</li>
          ))}
        </ul>
      </div>
      <div style={{ flex: 1 }}>
        <p>
          <strong>Code Snippet:</strong>
        </p>
        <div style={{ overflowX: 'auto' }}>
          <SyntaxHighlighter language="java" style={darcula}>
            {codeExample ? codeExample.example : 'No code snippet available'}
          </SyntaxHighlighter>
        </div>
      </div>
    </div>
  );
};

export default ImpactScore;
