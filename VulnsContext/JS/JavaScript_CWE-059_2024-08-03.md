# Improper Link Resolution Before File Access ('Link Following') (CWE-059) in JavaScript

###### Explanation of Improper Link Resolution Before File Access ('Link Following')

**Improper Link Resolution Before File Access (Link Following)** is a vulnerability where an application follows file system links (symlinks or hard links) improperly. This can lead to unauthorized file access, data leakage, or system compromise. The vulnerability occurs because the application may access the target of the link without correctly verifying the resolution path, which an attacker can manipulate to access unintended files.

For example, if an application resolves a path `/data/uploads` and the attacker creates a symlink from `/data/uploads` to `/etc/passwd`, the application inadvertently accesses `/etc/passwd` instead of a user-uploaded file.

### Common Variations in JavaScript (Especially in Popular Frameworks)

Improper Link Resolution can manifest in various ways across JavaScript, and popular frameworks can be susceptible if not properly handled. Below are several examples to help detect such cases in SAST (Static Application Security Testing) tools.

#### 1. Node.js with `fs` Module
The `fs` module provides a filesystem API that can be used to perform operations like reading, writing, and resolving paths.

Example:
```javascript
const fs = require('fs');

// Vulnerable code
fs.readFile('/user/uploads/file.txt', (err, data) => {
  if (err) throw err;
  console.log(data);
});
```
If `/user/uploads/file.txt` is a symlink to `/etc/passwd`, the program may read sensitive system files.

#### 2. Express.js Middleware for File Upload
Example:
```javascript
const express = require('express');
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const app = express();

app.post('/upload', upload.single('file'), (req, res) => {
  const filePath = req.file.path;
  fs.readFile(filePath, (err, data) => {
    if (err) throw err;
    res.send('File uploaded successfully');
  });
});

app.listen(3000);
```
An attacker could create a symbolic link in the `uploads` directory leading to the access of unintended files.

#### 3. Using Path Resolution with Potential Links
Example:
```javascript
const path = require('path');
const fs = require('fs');

const filePath = path.resolve('/uploads', userInput);
fs.readFile(filePath, (err, data) => {
  if (err) throw err;
  console.log(data);
});
```
Here, `userInput` can be manipulated to point to unintended files if proper validation is not implemented.

### More Examples for Detection

#### Read Symbolic Link Before Accessing
Detect when symbolic links are read without proper validation.
```javascript
const fs = require('fs');

fs.readlink('/path/to/link', (err, linkString) => {
  if (err) throw err;
  fs.readFile(linkString, (err, data) => {
    if (err) throw err;
    console.log(data);
  });
});
```

#### Path traversal to access sensitive files
```javascript
const express = require('express');
const app = express();

app.get('/view-file', (req, res) => {
  const filePath = path.join('/secure/path', req.query.filename);
  fs.readFile(filePath, (err, data) => {
    if (err) throw err;
    res.send(data);
  });
});

app.listen(3000);
```
This example allows path traversal attacks. If `req.query.filename` is set to `../../etc/passwd`, it can grant unauthorized file access.

### Recommendations for SAST Rule Implementation

To detect these vulnerabilities, SAST tools can target several patterns:

1. **Direct filesystem access:** 
   - Detect `fs.readFile`, `fs.readlink`, `fs.writeFile`, etc.
   - Detect if these functions are used with user-controllable inputs.

2. **Path resolution with user input:**
   - Look for usage of `path.resolve`, `path.join` with user inputs.
   - Ensure resolved paths are validated against expected directories.

3. **Symbolic link handling:**
   - Identify where symbolic links are accessed.
   - Validate the target of symlinks before file operations.

4. **Express.js and Middleware Patterns:**
   - Monitor for file operations within routes and middleware.
   - Ensure application logic validates file paths and prevents directory traversal.

Implementing these checks in a SAST tool can help detect and mitigate Improper Link Resolution vulnerabilities effectively.

### References

To further understand Improper Link Resolution Before File Access, refer to the following:

- CWE-59 Improper Link Resolution Before File Access ('Link Following')【4:0†source】
  
Each of these references discusses detailed mechanisms and countermeasures to address this kind of vulnerability.