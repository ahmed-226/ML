const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Define the path to the index.html file
const filePath = path.join(__dirname, 'view', 'index.html');

// Create the HTTP server
const server = http.createServer((req, res) => {
    if (req.method === 'GET' && req.url === '/') {
        // Serve the index.html file
        fs.readFile(filePath, (err, content) => {
            if (err) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Server Error');
            } else {
                res.writeHead(200, { 'Content-Type': 'text/html' });
                res.end(content);
            }
        });
    } else if (req.method === 'POST' && req.url === '/predict') {
        // Handle form submission
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            try {
                const formData = JSON.parse(body);
                const { Open, High, Low, Volume } = formData;

                console.log('Received data:', formData);

                const pythonProcess = spawn('python', ['predict.py', Open, High, Low, Volume]);

                pythonProcess.stdout.on('data', (data) => {
                    const result = data.toString().trim();
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ prediction: result }));
                });

                pythonProcess.stderr.on('data', (data) => {
                    console.error(`stderr: ${data}`);
                    res.writeHead(500, { 'Content-Type': 'text/plain' });
                    res.end(data.toString());
                });

                pythonProcess.on('close', (code) => {
                    console.log(`child process exited with code ${code}`);
                });
            } catch (error) {
                console.error('Error parsing JSON:', error);
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Invalid JSON' }));
            }
        });
    } else if (req.method === 'GET' && req.url === '/predictions.js') {
        // Serve the predictions.js file
        const jsFilePath = path.join(__dirname, 'view', 'predictions.js');
        fs.readFile(jsFilePath, (err, content) => {
            if (err) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Server Error');
            } else {
                res.writeHead(200, { 'Content-Type': 'application/javascript' });
                res.end(content);
            }
        });
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
    }
});

// Define the port
const PORT = process.env.PORT || 3000;

// Start the server
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
