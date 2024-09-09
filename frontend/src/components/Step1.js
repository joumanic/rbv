import React from 'react';

function Step1({ nextStep }) {
  return (
    <div>
      <h1>Radio Show Hosting Information</h1>
      <p>Here’s some long text explaining the process...</p>
      <button onClick={nextStep}>Next</button>
    </div>
  );
}

export default Step1;
