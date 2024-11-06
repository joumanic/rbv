const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000; // Proxy server port

// Middleware to set the CORS headers
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight requests for CORS
  if (req.method === 'OPTIONS') {
    return res.sendStatus(204); // No Content
  }

  next();
});

// Use JSON middleware to parse JSON bodies (required for POST/PUT requests)
app.use(express.json());

// Proxy any GET, POST, PUT, or DELETE requests to the external API
app.all('/api/*', async (req, res) => {
  const apiUrl = `https://rbv.onrender.com${req.originalUrl.replace('/api', '')}`;

  try {
    const response = await axios({
      method: req.method,
      url: apiUrl,
      data: req.body,
      headers: { ...req.headers, host: '' } // Remove host header to avoid host mismatch
    });

    // Set CORS headers on the proxy response
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    res.status(response.status).json(response.data); // Send back the response data
  } catch (error) {
    console.error("Proxy error:", error.message);

    // Send the error response with the same status and data, if available
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else {
      res.status(500).json({ message: "Internal Server Error" });
    }
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Proxy server running on http://localhost:${PORT}`);
});
