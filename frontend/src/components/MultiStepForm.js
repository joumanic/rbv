import React, { useState } from 'react';
import Step1 from './Step1';
import Step2 from './Step2';
import Step3 from './Step3';

function MultiStepForm() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    showName: '',
    hostName: '',
    isHostingGuest: false,
    guests: [''],
    genres: { genre1: '', genre2: '', genre3: '' },
    socialUrls: [],
    showImage: null
  });

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  const handleFormDataChange = (input) => (e) => {
    setFormData({ ...formData, [input]: e.target.value });
  };

  const handleGuestChange = (index) => (e) => {
    const updatedGuests = [...formData.guests];
    updatedGuests[index] = e.target.value;
    setFormData({ ...formData, guests: updatedGuests });
  };

  const addGuest = () => {
    setFormData({ ...formData, guests: [...formData.guests, ''] });
  };

  const handleSubmit = () => {
    // Make an API call to your backend here with formData using Axios
    axios.post('https://your-backend-url.com/api/radio-show/', formData)
      .then(response => {
        console.log("Success:", response);
      })
      .catch(error => {
        console.error("Error:", error);
      });
  };

  switch(step) {
    case 1:
      return <Step1 nextStep={nextStep} />;
    case 2:
      return <Step2 formData={formData} handleFormDataChange={handleFormDataChange} handleGuestChange={handleGuestChange} addGuest={addGuest} nextStep={nextStep} prevStep={prevStep} />;
    case 3:
      return <Step3 handleSubmit={handleSubmit} formData={formData} prevStep={prevStep} />;
    default:
      return null;
  }
}

export default MultiStepForm;
