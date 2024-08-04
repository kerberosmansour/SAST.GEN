# Unrestricted Upload of File with Dangerous Type (CWE-434) in TypeScript

****Unrestricted Upload of File with Dangerous Type**

An "Unrestricted Upload of File with Dangerous Type" vulnerability occurs when an application allows unfiltered and unsafe file types to be uploaded by users. This can lead to numerous security risks, including remote code execution, cross-site scripting (XSS), Denial-of-Service (DoS) attacks, and more. The primary causes of such vulnerabilities are inadequate validation of file types, extensions, MIME types, and content inspection mechanisms.

Here are some useful points to consider when writing detection rules for a SAST tool regarding this vulnerability:

1. **Validation Strategies:**
    - **Extension Validation:** Ensure the validation occurs after decoding the file name to avoid bypasses like double extensions (`.jpg.php`), null bytes (`.php%00.jpg`), or maliciously crafted names.
    - **MIME Type Validation:** Validate MIME types against a whitelist, but be aware that MIME types can be spoofed.
    - **File Signature Validation:** Check file signatures to verify that the content matches the expected file type.

2. **Validation Bypasses and Common Mistakes:**
    - Double extensions (e.g., `.jpg.php`)
    - Null byte injection (e.g., `.php%00.jpg`)
    - User-controlled file name constructs that lead to path traversal (`../evil.js`)

3. **Framework Specific Considerations (TypeScript Examples):**
    - **Express (Node.js)**
    - **NestJS**
    - **Angular**
    - **React/Next.js**
    - **Vue.js/Nuxt.js**

### Examples and Variations in TypeScript and Popular Frameworks

#### Express (Node.js)

1. **Basic Server-Side Validation**

   ```typescript
   import express, { Request, Response } from 'express';
   import multer from 'multer';

   const upload = multer({
     fileFilter: (req: Request, file: Express.Multer.File, cb) => {
       if (file.mimetype !== 'image/png' && file.mimetype !== 'image/jpeg') {
         return cb(new Error('Invalid file type'), false);
       }
       cb(null, true);
     },
   });

   const app = express();

   app.post('/upload', upload.single('file'), (req: Request, res: Response) => {
     res.send('File uploaded!');
   });

   app.listen(3000, () => console.log('Server started on port 3000'));
   ```

2. **Advanced Validation with File Extension and MIME-Type Check**

   ```typescript
   const allowedExtensions = /png|jpeg|jpg/;

   upload.use((req: Request, file: Express.Multer.File, cb) => {
     const extname = allowedExtensions.test(file.originalname.split('.').pop() || '');
     const mimetype = allowedExtensions.test(file.mimetype);
     
     if (extname && mimetype) {
       return cb(null, true);
     } else {
       return cb(new Error('File type not allowed'), false);
     }
   });
   ```

#### NestJS

1. **File Upload with Validation**

   ```typescript
   import { Controller, Post, UploadedFile, UseInterceptors } from '@nestjs/common';
   import { FileInterceptor } from '@nestjs/platform-express';
   import { diskStorage } from 'multer';

   const allowedMimeTypes = ['image/png', 'image/jpeg'];

   @Controller('upload')
   export class UploadController {
     @Post()
     @UseInterceptors(FileInterceptor('file', {
       storage: diskStorage({ destination: './uploads' }),
       fileFilter: (req, file, cb) => {
         if (allowedMimeTypes.includes(file.mimetype)) {
           cb(null, true);
         } else {
           cb(new Error('Invalid file type'), false);
         }
       },
     }))
     uploadFile(@UploadedFile() file) {
       return 'File uploaded!';
     }
   }
   ```

#### Angular

1. **Client-Side Only Validation (not secure by itself but adds a layer)**

   ```typescript
   import { Component } from '@angular/core';

   @Component({
     selector: 'app-upload',
     templateUrl: './upload.component.html'
   })
   export class UploadComponent {
     onFileChange(event: any) {
       const file = event.target.files[0];
       const allowedMimeTypes = ['image/png', 'image/jpeg', 'application/pdf'];

       if (file && allowedMimeTypes.includes(file.type)) {
         console.log('File is valid');
       } else {
         console.error('Invalid file type');
       }
     }
   }
   ```

#### React

1. **Client-Side File Type Checking**

   ```jsx
   import React from 'react';

   class FileUpload extends React.Component {
     handleFileChange = (event) => {
       const file = event.target.files[0];
       const allowedMimeTypes = ['image/png', 'image/jpeg'];

       if (file && allowedMimeTypes.includes(file.type)) {
         console.log('File is valid');
       } else {
         console.error('Invalid file type');
       }
     };

     render() {
       return (
         <input type="file" onChange={this.handleFileChange} />
       );
     }
   }

   export default FileUpload;
   ```

### Potential SAST Rules for Detection

1. **Detection of File Upload without Proper Validation**

   ```json
   {
     "patterns": [
       {
         "type": "regex",
         "pattern": "multer\\(.*\\)\\.single|multer\\(.*\\)\\.array",
         "message": "Potential file upload without proper file validation.",
         "severity": "high"
       }
     ]
   }
   ```

2. **Detection of File Type/MIME-Type Check Bypass**

   ```json
   {
     "patterns": [
       {
         "type": "regex",
         "pattern": "file\\.mimetype\\s*===\\s*.*",
         "message": "Check for MIME type validation. Ensure it is combined with file extension validation.",
         "severity": "medium"
       }
     ]
   }
   ```

By identifying and focusing on these various points, a SAST tool can provide more accurate detection of Unrestricted Upload of File with Dangerous Type vulnerabilities, reducing both false positives and negatives.

### References
【4:0†source】  