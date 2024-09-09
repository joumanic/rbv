import React from 'react';

function Step2({ formData, handleFormDataChange, handleGuestChange, addGuest, nextStep, prevStep }) {
  return (
    <div>
      <h2>Fill in the Radio Show Details</h2>
      <label>
        Show Name:
        <input type="text" value={formData.showName} onChange={handleFormDataChange('showName')} />
      </label>
      <label>
        Host Name:
        <input type="text" value={formData.hostName} onChange={handleFormDataChange('hostName')} />
      </label>
      <label>
        Are you hosting a guest?
        <input type="checkbox" checked={formData.isHostingGuest} onChange={() => handleFormDataChange('isHostingGuest')(!formData.isHostingGuest)} />
      </label>

      {formData.isHostingGuest && (
        <>
          {formData.guests.map((guest, index) => (
            <div key={index}>
              <label>Guest Name:</label>
              <input type="text" value={guest} onChange={handleGuestChange(index)} />
            </div>
          ))}
          <button onClick={addGuest}>Add another guest</button>
        </>
      )}

      {/* Genre Inputs */}
      <label>Genre 1:
        <input type="text" value={formData.genres.genre1} onChange={handleFormDataChange('genres.genre1')} />
      </label>
      <label>Genre 2:
        <input type="text" value={formData.genres.genre2} onChange={handleFormDataChange('genres.genre2')} />
      </label>
      <label>Genre 3:
        <input type="text" value={formData.genres.genre3} onChange={handleFormDataChange('genres.genre3')} />
      </label>

      {/* Social URLs */}
      <label>
        Social URLs:
        <input type="text" value={formData.socialUrls} onChange={handleFormDataChange('socialUrls')} />
      </label>

      {/* Image Upload */}
      <label>Show Image:
        <input type="file" onChange={handleFormDataChange('showImage')} />
      </label>

      <button onClick={prevStep}>Back</button>
      <button onClick={nextStep}>Next</button>
    </div>
  );
}

export default Step2;
