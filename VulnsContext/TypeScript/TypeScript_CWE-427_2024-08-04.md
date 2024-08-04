# Uncontrolled Search Path Element (CWE-427) in TypeScript

###### Uncontrolled Search Path Element in TypeScript and Popular Frameworks

#### Definition and Explanation

An "Uncontrolled Search Path Element" vulnerability occurs when an application includes a path that is influenced by a user without proper validation or sanitization. This can lead to the inclusion of unintended directories containing malicious code, resulting in unintended command execution or exposure of sensitive data.

#### Explanation for SAST Tool Rule Author

To write effective SAST detection rules for "Uncontrolled Search Path Element" vulnerabilities in TypeScript, it’s crucial to understand the contexts and patterns in which these vulnerabilities typically appear. It's essential to understand how file paths and environment variable manipulations are handled across different frameworks.

### Examples in TypeScript

Below are illustrative examples in TypeScript that demonstrate various implementations and frameworks where uncontrolled search path element vulnerabilities might manifest. 

1. **Node.js with General Path Manipulation**
    ```typescript
    import fs from 'fs';
    import path from 'path';

    const readUserFile = (userProvidedPath: string) => {
        const fullPath = path.join(__dirname, userProvidedPath);
        fs.readFile(fullPath, 'utf8', (err, data) => {
            if (err) {
                console.error(err);
            } else {
                console.log(data);
            }
        });
    }

    // User provides a path like "../etc/passwd"
    readUserFile("../etc/passwd");
    ```
    Here, the `path.join` function combines the `__dirname` with a user-provided path, which could potentially give access to sensitive files.

2. **Express Framework**
    ```typescript
    import express from 'express';
    import path from 'path';

    const app = express();

    app.get('/view', (req, res) => {
        const filePath = path.join(__dirname, req.query.page as string);
        res.sendFile(filePath);
    });

    app.listen(3000, () => {
        console.log('Server is running on port 3000');
    });
    ```
    In this instance, an attacker might manipulate the `page` query parameter to read sensitive files from the server.

3. **Electron Framework**
    ```typescript
    import { app, BrowserWindow } from 'electron';
    import path from 'path';

    let mainWindow: BrowserWindow;

    const createWindow = () => {
        mainWindow = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                preload: path.join(__dirname, process.env.PRELOAD_SCRIPT || 'default-preload.js')
            }
        });

        mainWindow.loadFile('index.html');
    }

    app.on('ready', createWindow);
    ```
    Here, the `process.env.PRELOAD_SCRIPT` is user-controllable, potentially leading to the execution of arbitrary scripts.

### SAST Rule Suggestions

To detect these patterns effectively, the following rule details would be necessary:

1. **Path Manipulation Operations**:
    - Identify the use of `path.join`, `path.resolve`, etc., where one or more arguments are dynamically influenced by user input or environment variables.

2. **Unsanitized and Unvalidated Input**:
    - Trace the sources of inputs (e.g., request parameters, environment variables) to see if they are used directly in path operations without validation.
    - Regular expressions or Abstract Syntax Tree (AST) parsing can be used to identify patterns where inputs are concatenated or joined in paths.

3. **Framework-Specific Patterns**:
    - For `express`, track usage in `req.query`, `req.params`, or `req.body` in path construction.
    - For `electron`, check `webPreferences.preload`, `app.getPath()`, `BrowserWindow.loadFile`, etc., for unvalidated dynamic inputs.

### Mitigations and Best Practices

1. **Input Validation and Sanitization**:
    - Use rigorous validation to ensure that only expected and safe values are processed.
    - Consider using a whitelist approach where only pre-approved paths or filenames are accepted.

2. **Library or Utility Functions**:
    - Where possible, use library functions designed to securely handle paths, such as those validating and sanitizing path inputs.

3. **Environment Variable Controls**:
    - Avoid using environment variables directly in paths. If necessary, ensure they are validated against expected safe values.

4. **Applying Permissions and Discovery Mechanisms**:
    - Apply appropriate file system permissions to ensure restrictive access.
    - Implement file discovery mechanisms that reduce the chance of exploration or enumeration beyond intended directories.

By focusing on these aspects, a SAST tool can be fine-tuned to minimize false positives and false negatives, providing robust detection for "Uncontrolled Search Path Element" vulnerabilities in TypeScript applications across various frameworks.