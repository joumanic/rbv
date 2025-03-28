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
    email: '',
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
    preRecord: null,
    guests: [],
    isHostingGuest: false,
  });
  
  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);
  
  const handleFileChange = (event) => {
    const file = event.target.files[0]; // Get the selected file
    const { name } = event.target; // Get the input field's name attribute
  
    if (file) {
      setFormData((prev) => ({
        ...prev,
        [name]: file, // Dynamically update either showImage or preRecord based on input name
      }));
    }
  };
  
  const handleFormDataChange = (name) => (event) => {
    let value;
  
    // Check if the name is related to the showDate
    if (name === 'showDate') {
      value = format(event, 'yyyy-MM-dd');
    } 
    // If it's a URL (like the show image), handle it as a URL
    else if (name === 'showImage') {
      value = event.target.value; // Treat the value as the URL string
    }
    // Handle all other inputs as normal text input
    else {
      value = event.target.value;
    }
  
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
    // First, check if an image is selected
    if (!formData.showImage) {
      console.error("No image selected.");
      return;
    }
  
    // Create FormData for the radio show and the image
    const formDataToSubmit = new FormData();
    formDataToSubmit.append('email', formData.email);
    formDataToSubmit.append('host_name', formData.hostName);
    formDataToSubmit.append('show_name', formData.showName);
    formDataToSubmit.append('genre1', formData.genres.genre1);
    formDataToSubmit.append('genre2', formData.genres.genre2);
    formDataToSubmit.append('genre3', formData.genres.genre3);
    formDataToSubmit.append('socials', formData.socials);
    formDataToSubmit.append('show_date', formData.showDate);
    formDataToSubmit.append('show_image_url', formData.showImage);
    formDataToSubmit.append('pre_record_url', formData.preRecord);  // Append the image file directly
  
    // Handle guests if needed
    formData.guests.forEach((guest, index) => {
      formDataToSubmit.append(`guest${index + 1}`, guest);
    });
  
    // Now send the form data to create the radio show
    axios.post(`${process.env.REACT_APP_API_BASE_URL_RENDER}/api/radio-show/`, formDataToSubmit)
      .then(response => {
        console.log("Success:", response);
        nextStep(); // Go to the next step
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
          handleFileChange={handleFileChange}
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
