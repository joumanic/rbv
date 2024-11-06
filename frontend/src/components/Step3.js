import React from 'react';

function Step3({ handleSubmit, prevStep }) {
  return (
    <div className="step-form">
      <h2 className="form-title">Thank You for Your Submission!</h2>
      <p className="form-description">You will receive a confirmation email shortly.</p>
      <div className="btn-container">
        <button className="btn" onClick={prevStep}>Back</button>
        <button className="btn" onClick={handleSubmit}>Submit</button>
      </div>
    </div>
  );
}

export default Step3;
