# Uncontrolled Resource Consumption (CWE-400) in JavaScript

###### Explanation of Uncontrolled Resource Consumption

**Uncontrolled Resource Consumption (URC)**, often related to Denial of Service (DoS) attacks, refers to the scenario where an application consumes excessive amounts of resources (CPU, memory, disk space, etc.), potentially leading to system instability or crashes. Essentially, URC vulnerabilities exist when an attacker can supply inputs that cause the application to allocate more resources than can be tolerated by the system, leading to performance degradation.

From the provided files, some common mitigation strategies for resource exhaustion include limiting file upload size, total request size, and session time; avoiding input-based resource allocation; and employing rate limiting mechanisms【4:0†source】【4:1†source】【4:2†source】.

### Uncontrolled Resource Consumption in JavaScript

Uncontrolled Resource Consumption in JavaScript can occur in various scenarios, particularly with popular frameworks like Node.js, Express, and others. Below are several examples:

1. **Memory Leaks**:
   - **Improper Looping**:
     ```javascript
     let data = [];
     while (true) {
       data.push(new Array(1000).fill('memory leak'));
     }
     // This loop will keep consuming memory until the system crashes.
     ```

2. **Unrestricted File Uploads**:
   - **File Upload without size limits**:
     ```javascript
     const express = require('express');
     const fileUpload = require('express-fileupload');
     const app = express();
     
     app.use(fileUpload());
     
     app.post('/upload', function(req, res) {
       if (!req.files) {
         return res.status(400).send('No files were uploaded.');
       }
     
       let sampleFile = req.files.sampleFile;
       sampleFile.mv('/somewhere/on/your/server/filename', function(err) {
         if (err)
           return res.status(500).send(err);
     
         res.send('File uploaded!');
       });
     });
     
     app.listen(3000);
     ```
     - Without file size limits, an attacker could upload extremely large files causing resource exhaustion【4:0†source】【4:1†source】.

3. **Infinite Recursion**:
   - **Recursive Function without base case**:
     ```javascript
     function recursiveFunction() {
       return recursiveFunction();
     }
     recursiveFunction();
     // This will eventually lead to a stack overflow.
     ```

4. **Unrestricted User Input Processing**:
   - **Complex Regex**:
     ```javascript
     function processData(input) {
       const regex = /(\w+)+/;
       let match;
       while ((match = regex.exec(input)) !== null) {
         console.log(match[1]);
       }
     }
     
     processData("This is a very long string created by an attacker...");
     // Complex regular expressions on long strings can lead to excessive CPU usage.
     ```

5. **Excessive Database Queries**:
   - **No Limit on Number of Results**:
     ```javascript
     app.get('/search', (req, res) => {
       const query = req.query.q;
       db.collection('documents').find({ $text: { $search: query } }).toArray((err, docs) => {
         if (err) return res.status(500).send(err);
         res.send(docs);
       });
     });
     // An attacker can use a search term that matches a large number of documents causing excessive data fetching, leading to high memory use.
     ```

6. **Non-throttled WebSocket Connections**:
   - **WebSocket without Limitations**:
     ```javascript
     const WebSocket = require('ws');
     const wss = new WebSocket.Server({ port: 8080 });
     
     wss.on('connection', function connection(ws) {
       ws.on('message', function incoming(message) {
         console.log('received: %s', message);
       });
     });
     // Without rate limiting or authentication, an attacker can open multiple concurrent WebSocket connections leading to resource exhaustion.
     ```

### Recommendations for SAST Rule Detection

To assist in the creation of SAST rules for detecting URC vulnerabilities, consider looking for:
1. **Unbounded Loops**: Detect while loops or recursive functions without proper termination conditions.
2. **File Uploads**: Flag code that handles file uploads without checking for size limits.
3. **Complexity in User Inputs**: Identify regex operations that can be CPU intensive when processing long or complex input.
4. **Database Query Limits**: Ensure that database queries impose limits on the number of results fetched.
5. **Resource Allocation Based on Input**: Detect operations where input directly affects memory or CPU allocation (e.g., `new Array(input).fill(0)`).
6. **WebSocket Connections**: Look for WebSocket server implementations that do not include mechanisms for rate limiting or connection caps.

Implementing these rules will help in identifying potential URC vulnerabilities during the software development lifecycle, thus mitigating the risk of resource exhaustion attacks.