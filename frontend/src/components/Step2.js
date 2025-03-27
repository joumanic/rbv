import React from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

function Step2({ formData, handleFormDataChange, handleFileChange, handleGuestChange, addGuest, nextStep, prevStep }) {

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

      <label><b>Email:</b>
        <input 
          type="text" 
          value={formData.email} 
          onChange={handleFormDataChange('email')} 
        />
      </label>

      <label><b>Show Name:</b>
        <div class="small-text">(please write it exactly as you’d like it to appear
including capital letters and any symbols e.g “The Rise Up Show w/ Speedy” or
“DJ Uncomfortable” or “Gorbals After Hours”)</div>
        <input 
          type="text" 
          value={formData.showName} 
          onChange={handleFormDataChange('showName')} 
        />
      </label>

      <label><b>Host Name:</b>
        <input 
          type="text" 
          value={formData.hostName} 
          onChange={handleFormDataChange('hostName')} 
        />
      </label>

      <label><b>Are you hosting a guest?</b>
      <div class="small-text">(their names will be added after the above
show name and …..&amp; Guest name – e.g “The Rise Up Show w/ Speedy &amp; DJ
Breakfast Cereal”)</div>
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
      <label><b>GENRES: </b>we can add up to 3 music genres or describers to explain the
general vibe/style/theme of your show (e.g. amapiano, jazz, hip hop,
community, interview)</label>
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

      <label><b>Social URLs:</b>
      <div class="small-text">(please paste the actual URL link not
        just the name)</div>
        <input 
          type="text" 
          value={formData.socials} 
          onChange={handleFormDataChange('socials')} 
        />
      </label>

      <label><b>Show Date:</b>
      <DatePicker
        selected={formData.showDate ? new Date(formData.showDate) : null} // Convert to Date or null
        onChange={handleDateChange}
        dateFormat="yyyy-MM-dd"
        className="form-control"
        placeholderText="Select a date"
      /></label>
  
      <label><b>Show Image:</b>
        <input type="file" 
        accept="image/*" 
        name="showImage"
        onChange={handleFileChange} 
        />
      </label>

      <label><b>Pre-Record:</b>
        <input type="file" 
        accept="audio/*" 
        name="preRecord"
        onChange={handleFileChange} 
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
