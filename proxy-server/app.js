const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;

// Enable CORS
const allowedOrigins = ['https://rbv.vercel.app', 'http://localhost:3000'];
app.use(cors({
  origin: allowedOrigins,
  methods: 'GET,POST,PUT,DELETE,OPTIONS',
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Middleware
app.use(express.json());

// API Route Example
app.get('/', (req, res) => {
    console.log("Received request at /");
    res.json({ message: 'Welcome to the server 😁' });
});

// Proxy Endpoint (if needed)
app.all('/api/*', async (req, res) => {
  const apiUrl = `${process.env.REACT_APP_API_BASE_URL_RENDER}${req.originalUrl.replace('/api', '')}`;
  try {
    const response = await axios({
      method: req.method,
      url: apiUrl,
      data: req.body,
      headers: {
        'Content-Type': req.headers['content-type'],
        Authorization: req.headers.authorization,
      }
    });
    res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Proxy error:", error.message);
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      res.status(500).json({ message: "Internal Server Error" });
    }
  }
});

module.exports = app;
