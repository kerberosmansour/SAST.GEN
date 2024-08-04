# Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (CWE-022) in JavaScript

###### Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')

**Definition:**
Path traversal, also known as directory traversal, occurs when an attacker manipulates file paths in input data to access directories and files stored in server directories that they should not be able to access. This vulnerability can lead to unauthorized access to files containing sensitive information such as configuration files, passwords, and proprietary code.

**Impact:**
- Unauthorized access to sensitive files.
- Data theft or manipulation.
- Application compromise by executing unauthorized files.

**Variations in JavaScript:**
Path traversal vulnerabilities can occur in various JavaScript frameworks like Node.js, Express, and others typically used on the server-side.

**Examples in JavaScript:**

1. **Node.js Example:**
   ```javascript
   const http = require('http');
   const url = require('url');
   const fs = require('fs');
   const path = require('path');

   const server = http.createServer((req, res) => {
       const parsedUrl = url.parse(req.url);
       const pathname = `.${parsedUrl.pathname}`;

       fs.readFile(pathname, (err, data) => {
           if (err) {
               res.statusCode = 404;
               res.end(`File not found!`);
           } else {
               res.statusCode = 200;
               res.end(data);
           }
       });
   });

   server.listen(3000, () => {
       console.log('Server listening on port 3000');
   });
   ```
   **Vulnerable to Path Traversal:**
   This example does not sanitize the `pathname` input, allowing an attacker to request something like `http://example.com/../../etc/passwd`.

2. **Express.js Example (without proper path validation):**
   ```javascript
   const express = require('express');
   const app = express();
   const fs = require('fs');
   const path = require('path');

   app.get('/static/:fileName', (req, res) => {
       const filePath = path.join(__dirname, 'static', req.params.fileName);

       fs.readFile(filePath, (err, data) => {
           if (err) {
               res.status(404).send('File not found!');
           } else {
               res.status(200).send(data);
           }
       });
   });

   app.listen(3000, () => {
       console.log('Server running on port 3000');
   });
   ```
   **Vulnerable to Path Traversal:**
   Here, `req.params.fileName` is directly concatenated to the base path without validation, thus allowing path traversal attacks.

3. **Secure Example in Node.js:**
   ```javascript
   const http = require('http');
   const url = require('url');
   const fs = require('fs');
   const path = require('path');

   const server = http.createServer((req, res) => {
       const parsedUrl = url.parse(req.url);
       let pathname = `.${parsedUrl.pathname}`;

       const safeSuffix = path.normalize(pathname).replace(/^(\.\.(\/|\\|$))+/g, '');
       const safeFilePath = path.join(__dirname, safeSuffix);

       fs.readFile(safeFilePath, (err, data) => {
           if (err) {
               res.statusCode = 404;
               res.end(`File not found!`);
           } else {
               res.statusCode = 200;
               res.end(data);
           }
       });
   });

   server.listen(3000, () => {
       console.log('Server listening on port 3000');
   });
   ```
   **Properly Secured:**
   This example validates and normalizes the path, ensuring no directory traversal is possible.

4. **Secure Example in Express.js:**
   ```javascript
   const express = require('express');
   const app = express();
   const fs = require('fs');
   const path = require('path');

   app.get('/static/:fileName', (req, res) => {
       const filePath = path.join(__dirname, 'static', path.normalize(req.params.fileName).replace(/^(\.\.(\/|\\|$))+/g, ''));

       fs.readFile(filePath, (err, data) => {
           if (err) {
               res.status(404).send('File not found!');
           } else {
               res.status(200).send(data);
           }
       });
   });

   app.listen(3000, () => {
       console.log('Server running on port 3000');
   });
   ```
   **Properly Secured:**
   This example uses `path.normalize` and replaces any traversal sequences, thus mitigating the path traversal vulnerability.

**Writing SAST Rules:**
For writing SAST (Static Application Security Testing) rules to detect such path traversal vulnerabilities, you should look for patterns where incoming input (like from URLs or form fields) is directly concatenated with file paths without proper validation or normalization.

1. **Identify critical functions:**
   - `fs.readFile`
   - `fs.readFileSync`
   - `path.join`
   - File system methods in Node.js and similar methods in other frameworks.

2. **Pattern Detection:**
   - Identify direct concatenation of paths and input values.
   - Look for lack of `path.normalize` or improper validation.

3. **Data Flow Analysis:**
   - Track if user input reaches file system functions without sanitization.

By using the above patterns, you can identify potential path traversal vulnerabilities and generate alerts or code fixes accordingly.

For more detailed information on CWE-22 Improper Limitation of a Pathname to a Restricted Directory, refer to the CWE definition【4:0†source】.