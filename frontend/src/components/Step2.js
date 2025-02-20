import React from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

function Step2({ formData, handleFormDataChange, handleGuestChange, addGuest, nextStep, prevStep }) {
    const handleFileChange = (event) => {
      const file = event.target.files[0]; // Get the first selected file
      if (file) {
        handleFormDataChange('showImage')(file);  // Store the file object in state
      }
    };
    const handleDateChange = (date) => {
        try {
          // If the date is null or an invalid value, we prevent the error and reset to empty string
          if (!date || isNaN(date.getTime())) {
            handleFormDataChange('showDate')(''); // Clear the date field
          } else {
            handleFormDataChange('showDate')(date.toISOString().split('T')[0]); // Save valid date in YYYY-MM-DD format
          }
        } catch (error) {
          console.error('Error handling date:', error);
        }
      };
  return (
    <div className="step-form">
      <h2 className="form-title">Fill in the Radio Show Details</h2>

      <label>Show Name:
        <input 
          type="text" 
          value={formData.showName} 
          onChange={handleFormDataChange('showName')} 
        />
      </label>

      <label>Host Name:
        <input 
          type="text" 
          value={formData.hostName} 
          onChange={handleFormDataChange('hostName')} 
        />
      </label>

      <label>Are you hosting a guest?
        <input 
          type="checkbox" 
          checked={formData.isHostingGuest} 
          onChange={handleFormDataChange('isHostingGuest')} 
        />
      </label>

      {formData.isHostingGuest && (
        <>
          {formData.guests.map((guest, index) => (
            <div key={index}>
              <label>Guest Name:</label>
              <input 
                type="text" 
                value={guest} 
                onChange={handleGuestChange(index)} 
              />
            </div>
          ))}
          <button className="btn" onClick={addGuest}>Add Guest</button>
        </>
      )}

      <label>Genre 1:
        <input 
          type="text" 
          value={formData.genres.genre1} 
          onChange={handleFormDataChange('genres.genre1')} 
        />
      </label>
      <label>Genre 2:
        <input 
          type="text" 
          value={formData.genres.genre2} 
          onChange={handleFormDataChange('genres.genre2')} 
        />
      </label>
      <label>Genre 3:
        <input 
          type="text" 
          value={formData.genres.genre3} 
          onChange={handleFormDataChange('genres.genre3')} 
        />
      </label>

      <label>Social URLs:
        <input 
          type="text" 
          value={formData.socials} 
          onChange={handleFormDataChange('socials')} 
        />
      </label>

      <label>Show Date:</label>
      <DatePicker
        selected={formData.showDate ? new Date(formData.showDate) : null} // Convert to Date or null
        onChange={handleDateChange}
        dateFormat="yyyy-MM-dd"
        className="form-control"
        placeholderText="Select a date"
      />
      <label>Show Image:
        <input type="file" 
        accept="image/*" 
        onChange={handleFormDataChange('showImage')} 
        />
      </label>

      <div className="btn-container">
        <button className="btn" onClick={prevStep}>Back</button>
        <button className="btn" onClick={nextStep}>Submit</button>
      </div>
    </div>
  );
}

export default Step2;
