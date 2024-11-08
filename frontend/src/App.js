import './App.css';
import axios from 'axios';
import { useEffect, useState } from 'react';
import MultiStepForm from './components/MultiStepForm';
 
function App() {
  useEffect(() => {
    axios.get(
      `${process.env.REACT_APP_API_BASE_URL_RENDER}`, {
        headers: {
          "Access-Control-Allow-Origin": true
        }
      }
    ) 
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.log('Error fetching data:', error);
      });
  }, []);


  return (
    <div className="App">
      <MultiStepForm/>
    </div>
  );
}

export default App;
