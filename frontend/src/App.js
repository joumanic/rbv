import './App.css';
import axios from 'axios';
import { useEffect, useState } from 'react';
import MultiStepForm from './components/MultiStepForm'; 

function App() {
  const makeAPICall = async () => {
    try {
      const response = await fetch('http://localhost:8000/cors', { mode: 'cors' });
      const data = await response.json();
      console.log({ data })
    }
    catch (e) {
      console.log(e)
    }
  }
  useEffect(() => {
    makeAPICall();
  }, [])
  return (
    <div className="App">
      <MultiStepForm/>
    </div>
  );
}
export default App;