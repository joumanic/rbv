import React from 'react';

function Step3({ handleSubmit, prevStep }) {
  return (
    <div>
      <h2>Thank You for Your Submission!</h2>
      <p>You will receive a confirmation email shortly.</p>
      <button onClick={prevStep}>Back</button>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default Step3;
