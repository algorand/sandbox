const express = require("express"); // Import express for simplified routing
// const path = require("path");
const compression = require("compression");
const cors = require("cors"); // Setup cors for cross-origin requests for all routes

const app = express(); // Setup express
const port = 8000; // Setup port 8000 for Express server

app.use(cors()); // Enable cors
app.use(compression()); // Compress requests;

app.get('*', function(req, res) {
    const payload = {
        message: 'AlgoSearch disabled for this configuration.',
        timestamp: Date.now(),
    };
    res.status(400).send(payload);
});

app.listen(port); // Initialize server
