# Unrestricted Upload of File with Dangerous Type (CWE-434) in JavaScript

###### Understanding Unrestricted Upload of File with Dangerous Type Vulnerability

#### Definition
The **Unrestricted Upload of File with Dangerous Type** vulnerability occurs when a web application allows file uploads without proper validation. This can enable attackers to upload malicious files that can exploit vulnerabilities in the system or gain unauthorized access【4:0†source】 .

#### Impact
Malicious uploads can lead to a variety of attacks, including:
1. **Remote Code Execution:** By uploading a file with server-executable code (e.g., a PHP file disguised as an image).
2. **Cross-Site Scripting (XSS):** Uploading a file with client-side scripts (e.g., JavaScript) which may get executed on other users’ browsers.
3. **Denial of Service (DoS):** Uploading large files or ZIP bombs to exhaust server resources.
4. **Phishing or Data Leaks:** Uploading files that can be used for phishing or exposing sensitive information.

### Variations in JavaScript Frameworks
Here are some specific examples of how this vulnerability can occur in JavaScript, especially within popular frameworks. 

#### Vanilla JavaScript / Node.js
```javascript
const express = require('express');
const fileUpload = require('express-fileupload');
const app = express();

app.use(fileUpload());

app.post('/upload', function(req, res) {
  let file = req.files.sampleFile;
  file.mv('/uploaded_files/' + file.name, function(err) {
    if (err)
      return res.status(500).send(err);
    res.send('File uploaded!');
  });
});
```
**Issue:** The code above does not validate the file type, size, or name. Attackers can upload any file type which could be harmful.

#### Example 1: Express Framework
```javascript
const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('file'), function(req, res) {
  res.send('File uploaded!');
});

```
**Issue:** There is no validation on the uploaded files, the file name and type are not checked. An attacker can upload an executable file.

#### Example 2: Sails.js
```javascript
const SkipperDisk = require('skipper-disk');
const upload = new SkipperDisk();

module.exports = {
  upload: function(req, res) {
    req.file('file').upload({
      dirname: require('path').resolve(sails.config.appPath, 'assets/images')
    }, function(err, uploadedFiles) {
      if (err) return res.send(500, err);
      return res.json({
        message: uploadedFiles.length + ' file(s) uploaded successfully!'
      });
    });
  }
};
```
**Issue:** Similar to Express, no validation on the type and name of the file. Any files, including scripts or executables, can be uploaded.

#### Example 3: Meteor.js
```javascript
if (Meteor.isServer) {
  Meteor.methods({
    'uploadFile': function(fileInfo) {
      fs.writeFile('/uploads/' + fileInfo.name, fileInfo.data, function(err) {
        if (err) throw new Meteor.Error(500, 'Error while uploading file');
      });
    }
  });
}
```
**Issue:** Writing files directly without validation enables potential execution of harmful scripts.

### Recommendations for Detection Rules
To address and mitigate the above vulnerabilities in these frameworks, consider the following detection rules for a Static Application Security Testing (SAST) tool:

1. **File Extension Validation:**
   - Ensure that only permitted file extensions are allowed.
   - Example Rule: Detect if the code does not validate the file extension against a whitelist.

2. **Content-Type Validation:**
   - Validate the MIME type of the file.
   - Example Rule: Detect missing validation or usage of `req.file.type` without validation.

3. **File Size Validation:**
   - Limit the size of uploaded files to prevent DoS attacks.
   - Example Rule: Check for the absence of file size validation mechanisms.

4. **Filename Sanitization:**
   - Ensure filenames are sanitized to prevent directory traversal attacks.
   - Example Rule: Identify improper handling of filenames using user-supplied values directly.

5. **File Signature Validation:**
   - Validate the file's signature to ensure it matches its purported type.
   - Example Rule: Flag occurrences where files are saved without verifying their signatures.

6. **Remote File Handling:**
   - Ensure that files are stored outside of the webroot.
   - Example Rule: Identify if the file storage location is accessible directly via URL.

### Example SAST Implementation

For a SAST tool to detect these vulnerabilities, it might look for specific patterns in code:

```regex
// Example pattern to detect uploads without validation
/\brequire\((['"])skipper-disk\1\)/  // for ‘Skipper Disk’ in Sails.js
|\brequire\((['"])express-fileupload\1\)  // for ‘express-fileupload’
// Check for multer without file type validation
|\bmulter\s*\(\{[^)]*\}\)  // for ‘multer’ in Express.js
// Look for unfiltered file writes
|\bfs.writeFile\s*\([\s\S]*\)  // for 'fs' in Node.js

// Extend the logic for more specific detections tailored to frameworks and their methods
```

By implementing these detection rules, a SAST tool can help identify and report instances where the secure handling of file uploads is not enforced, aiding developers in securing their JavaScript applications.

For further details, you may refer to sources documenting these secure practices and vulnerability definitions such as from OWASP   .