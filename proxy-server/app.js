const express = require('express');
const app = express();
app.get('/', (req, res) => {
    res.set('Access-Control-Allow-Origin', '*');
    console.log("Received request at /");
    res.json({ message: 'Welcome to CORS server 😁'});
})
app.get('/cors', (req, res) => {
    res.set('Access-Control-Allow-Origin', '*');
    console.log("Received request at /cors");
    res.json({ message: "This has CORS enabled 🎈"});
})
app.listen(8000, () => {
    console.log('listening on port 8000')
})
