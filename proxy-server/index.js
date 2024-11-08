const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;

// Set CORS headers and handle OPTIONS preflight requests
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    // Respond to preflight request immediately
    return res.sendStatus(204);
  }
  
  next();
});

// Use JSON middleware for request parsing
app.use(express.json());

// Proxy requests to backend API
app.all('/api/*', async (req, res) => {
  const apiUrl = `https://rbv.onrender.com${req.originalUrl.replace('/api', '')}`;

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

// Start the proxy server
app.listen(PORT, () => {
  console.log(`Proxy server running on http://localhost:${PORT}`);
});
