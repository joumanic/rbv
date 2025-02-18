import React, { useState } from 'react';
import axios from 'axios';
import Step1 from './Step1';  // Import your step components
import Step2 from './Step2';
import Step3 from './Step3';
import '../styles/MultiStepForm.css';
import { format } from 'date-fns';


function MultiStepForm() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    hostName: '',
    showName: '',
    genres: {
      genre1: '',
      genre2: '',
      genre3: '',
    },
    socials: '',
    showDate: null, // Initialize as null or a default date
    showImage: null,
    guests: [],
    isHostingGuest: false,
  });
  
  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);
  
  const handleFormDataChange = (name) => (event) => {
    const value = name === 'showDate' ? format(event, 'yyyy-MM-dd') : event.target.value;
    if (name.includes('.')) {
      const [mainField, subField] = name.split('.');
      setFormData((prevFormData) => ({
        ...prevFormData,
        [mainField]: {
          ...prevFormData[mainField],
          [subField]: value,
        },
      }));
    } else {
      setFormData((prevFormData) => ({
        ...prevFormData,
        [name]: value,
      }));
    }
  };
  
  const handleGuestChange = (index) => (event) => {
    const newGuests = [...formData.guests];
    newGuests[index] = event.target.value;
    setFormData({
      ...formData,
      guests: newGuests
    });
  };

  const addGuest = () => {
    setFormData({
      ...formData,
      guests: [...formData.guests, '']  // Add empty string for new guest
    });
  };

  const handleSubmit = () => {
    const formDataToSubmit = new FormData();
    formDataToSubmit.append('host_name', formData.hostName);
    formDataToSubmit.append('show_name', formData.showName);
    formDataToSubmit.append('genre1', formData.genres.genre1);
    formDataToSubmit.append('genre2', formData.genres.genre2);
    formDataToSubmit.append('genre3', formData.genres.genre3);
    formDataToSubmit.append('socials', formData.socials);
    formDataToSubmit.append('show_date', formData.showDate);
    formDataToSubmit.append('show_image', formData.showImage);

    // If you are hosting guests, you may want to handle that too
    formData.guests.forEach((guest, index) => {
      formDataToSubmit.append(`guest${index + 1}`, guest); // Append each guest
    });

    axios.post(`${process.env.REACT_APP_API_BASE_URL_RENDER}/api/radio-show/`, formDataToSubmit)
    .then(response => {
      console.log("Success:", response);
      nextStep();
      // Handle success (e.g., navigate to a success page)
    })
    .catch(error => {
      console.error("Error:", error);
      // Handle error (e.g., show error message)
    });
  };

  switch (step) {
    case 1:
      return <Step1 nextStep={nextStep} />;
    case 2:
      return (
        <Step2
          formData={formData}
          handleFormDataChange={handleFormDataChange}
          handleGuestChange={handleGuestChange}
          addGuest={addGuest}
          nextStep={handleSubmit}
          prevStep={prevStep}
        />
      );
    case 3:
      return <Step3 />;
    default:
      return null;
  }
}

export default MultiStepForm;
