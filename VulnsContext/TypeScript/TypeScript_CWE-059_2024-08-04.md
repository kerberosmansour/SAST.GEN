# Improper Link Resolution Before File Access ('Link Following') (CWE-059) in TypeScript

###### Improper Link Resolution Before File Access ('Link Following') Vulnerability

**Definition:**
Improper Link Resolution Before File Access ('Link Following') is a vulnerability where an application resolves symbolic links, shortcuts, or other indirect references improperly before accessing files. This can allow attackers to manipulate these links to access unauthorized files or directories, potentially leading to information disclosure, data corruption, or other malicious outcomes.

**Relevant CWE:** [CWE-59](https://cwe.mitre.org/data/definitions/59.html)

### Types of Improper Link Resolution in TypeScript

To detect this type of vulnerability in TypeScript, especially within different popular frameworks, it's essential to understand various scenarios where file handling occurs. Below are some examples and contexts in which Improper Link Resolution might manifest:

1. **Node.js with the `fs` Module:**
   TypeScript applications often use the Node.js `fs` module to interact with the file system. An attacker could exploit improper resolution when symbolic links are not carefully managed.

   ```typescript
   import fs from 'fs';
   import path from 'path';

   const filePath = path.resolve('/user/data', '/symlink_to_sensitive_file');
   fs.readFile(filePath, 'utf8', (err, data) => {
      if (err) throw err;
      console.log(data);
   });
   ```
   In this example, the application resolves the symbolic link and reads the sensitive file, which might be unintended.

2. **Using Express.js to Serve Static Files:**
   Express.js applications often serve static files from a directory. If symbolic links are used within this directory, improper link resolution can expose sensitive files.

   ```typescript
   import express from 'express';

   const app = express();
   app.use('/public', express.static('/public'));
   app.listen(3000, () => console.log('Server running on port 3000'));
   ```

   Here, if `/public` contains a symlink to a sensitive file or directory, an attacker can potentially access it through HTTP requests.

3. **Handling File Uploads with Multer:**
   When handling file uploads in Express.js applications using Multer, files are often written to the file system.

   ```typescript
   import express from 'express';
   import multer from 'multer';

   const app = express();
   const upload = multer({ dest: 'uploads/' });

   app.post('/upload', upload.single('file'), (req, res) => {
      res.send('File uploaded!');
   });

   app.listen(3000, () => console.log('Server running on port 3000'));
   ```

   If `uploads/` contains symbolic links, an attacker might manipulate uploaded files to replace the symlinks and access unintended files.

4. **Electron.js Applications:**
   Electron.js apps often combine frontend and backend code, leading to potential security risks similar to those in traditional web applications.

   ```typescript
   const { app, ipcMain } = require('electron');
   const fs = require('fs');
   const path = require('path');

   ipcMain.on('read-file', (event, filePath) => {
      const resolvedPath = path.resolve(filePath);
      fs.readFile(resolvedPath, 'utf8', (err, data) => {
         if (err) {
            event.reply('read-file-reply', 'Error reading file');
         } else {
            event.reply('read-file-reply', data);
         }
      });
   });

   app.on('ready', () => {
      // app initialization code
   });
   ```

   Here, the application resolves the file path and reads the content. If the path leads to a symbolic link created by the attacker, it could result in the application reading unintended files.

### SAST Rule Definition

To detect Improper Link Resolution, a SAST rule should:
1. **Identify Functions:** Target specific functions that handle file paths and file operations, such as `fs.readFile`, `fs.readFileSync`, `express.static`, `path.resolve`, etc.
2. **Path Resolution Check:** Check if the resolved paths involve symbolic links. This often requires flagging `path.resolve` combined with `fs` operations.
3. **File Handling Context:** Identify contexts where file paths from user input or other untrusted sources are being resolved and used.

```json
{
  "id": "improper-link-resolution",
  "pattern": [
    {
      "type": "call_expression",
      "callee": {"type": "identifier", "name": "resolve"},
      "arguments": [
        {"type": "literal"}
      ]
    },
    {
      "type": "call_expression",
      "callee": {"type": "identifier", "name": {"matches": "readFile|readFileSync|stat|statSync"}},
      "arguments": [
        {"type": "identifier"}
      ]
    }
  ],
  "message": "Potential improper link resolution before file access. Ensure that symbolic links are handled securely.",
  "severity": "High"
}
```

This detection rule identifies calls to `path.resolve` followed by file operations like `fs.readFile` and suggests auditing these instances to check for symlink-related vulnerabilities.

Implementing fine-tuned rules that scrutinize the context and flow of data can help achieve high accuracy with minimal false positives and negatives【4:0†source】【4:1†source】【4:2†source】【4:3†source】【4:4†source】.

### Conclusion

To effectively create SAST rules for 'Improper Link Resolution Before File Access ('Link Following')' in TypeScript, one must understand how different frameworks handle file operations and path resolutions. By carefully analyzing the aforementioned examples and scenarios, a SAST tool can greatly enhance its ability to detect these vulnerabilities accurately.