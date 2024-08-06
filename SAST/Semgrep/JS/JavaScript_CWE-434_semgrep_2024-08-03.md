ToTo address the vulnerability "Unrestricted Upload of File with Dangerous Type (CWE-434) in JavaScript," we will create a set of Semgrep rules covering common patterns and frameworks. Below are Semgrep SAST rules to identify instances where such vulnerabilities might occur.

### General File Upload Vulnerability Pattern in JavaScript

```yaml
rules:
  - id: unrestricted-upload-of-file
    languages: [javascript]
    message: "Unrestricted Upload of File with Dangerous Type (CWE-434)"
    severity: ERROR
    pattern: | 
      const $VAR = req.files.$FILE;
      ...
      $VAR.mv(...);
    metadata:
      cwe: "CWE-434"
    examples:
      - code: |
          const file = req.files.uploadedFile;
          file.mv('/uploads/' + file.name);
        not-apply: true
      - code: |
          const secureFile = req.files.secureUpload;
          secureFile.mv('/uploads/' + secureFile.name);
        apply: true
```

This rule captures a typical scenario where files uploaded via `req.files` are processed without validation in Node.js.

### Express Framework Specific Rule

```yaml
rules:
  - id: express-unrestricted-file-upload
    languages: [javascript]
    message: "Unrestricted File Upload (CWE-434) in Express.js"
    severity: ERROR
    pattern: |
      app.post('/upload', (req, res) => {
        const $VAR = req.files.$FILE;
        ...
        $VAR.mv(...);
      });
    metadata:
      cwe: "CWE-434"
    examples:
      - code: |
          app.post('/upload', (req, res) => {
            const file = req.files.uploadedFile;
            file.mv(`/uploads/${file.name}`);
          });
        not-apply: true
      - code: |
          app.post('/upload', (req, res) => {
            const secureFile = req.files.secureUpload;
            secureFile.mv(`/uploads/${secureFile.name}`);
          });
        apply: true
```

This rule targets the Express framework by checking for file upload routes where file handling might not be secure.

### Handling File Type Verification

```yaml
rules:
  - id: file-upload-with-type-check
    languages: [javascript]
    message: "File upload without type check (CWE-434) in JavaScript"
    severity: ERROR
    pattern: |
      const $VAR = req.files.$FILE;
      if (!$VAR.mimetype.startsWith('image/')) {
        ...
      }
      $VAR.mv(...);
    metadata:
      cwe: "CWE-434"
    examples:
      - code: |
          const file = req.files.uploadedFile;
          if (!file.mimetype.startsWith('image/')) {
            return res.status(400).send('Invalid file type');
          }
          file.mv('/uploads/' + file.name);
        not-apply: true
      - code: |
          const secureFile = req.files.secureUpload;
          secureFile.mv('/uploads/' + secureFile.name);
        apply: true
```

This rule captures cases where the file's mimetype is checked before processing the upload, reducing the likelihood of CWE-434 vulnerability.

### Detailed Rule for Popular Libraries (e.g., Multer for handling files in Express)

```yaml
rules:
  - id: multer-unrestricted-file-upload
    languages: [javascript]
    message: "Unrestricted Upload with Multer (CWE-434)"
    severity: ERROR
    pattern: |
      const upload = multer({
        storage: multer.diskStorage({
          destination: (req, file, cb) => {
            cb(null, 'uploads/')
          },
          filename: (req, file, cb) => {
            cb(null, file.originalname)
          }
        }),
        fileFilter: (req, file, cb) => {
          ...
        }
      });
    metadata:
      cwe: "CWE-434"
    examples:
      - code: |
          const upload = multer({
            storage: multer.diskStorage({
              destination: (req, file, cb) => {
                cb(null, 'uploads/')
              },
              filename: (req, file, cb) => {
                cb(null, file.originalname)
              }
            })
          });
        not-apply: true
      - code: |
          const upload = multer({
            storage: multer.diskStorage({
              destination: (req, file, cb) => {
                cb(null, 'secure_uploads/')
              },
              filename: (req, file, cb) => {
                cb(null, file.originalname)
              }
            }),
            fileFilter: (req, file, cb) => {
              if (!file.mimetype.startsWith('image/')) {
                cb(null, false);
              } else {
                cb(null, true);
              }
            }
          });
        apply: true
```

This rule focuses on the Multer middleware for Express.js and ensures that file filters are in place to prevent unsafe files from being uploaded.

By using these rules, you can address various instances of the CWE-434 vulnerability in JavaScript applications, particularly in commonly used frameworks like Express.js. 

Note: Always test these rules extensively against your codebase and tune them as needed to minimize false positives and negatives.