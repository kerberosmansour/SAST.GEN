# Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') (CWE-078) in JavaScript

###### Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')

OS Command Injection is a severe security vulnerability that occurs when an application constructs a system command using input from an external source. If this input is not correctly neutralized or sanitized, it allows attackers to inject malicious commands into the existing command string. This can lead to unauthorized commands being executed on the server, resulting in various types of attacks including data theft, privilege escalation, or complete system compromise.

For example, in a Windows environment:
```shell
calc
```
This commands the application to open the Calculator. However, if the input is tampered with:
```shell
calc & echo "test"
```
This altered input now performs two commands: it opens the Calculator and prints "test" to the terminal【4:0†source】.

### Variations of OS Command Injection in JavaScript

JavaScript applications, particularly those running on server-side environments like Node.js, are susceptible to OS Command Injection if they execute system commands using unsanitized user inputs. Below are different ways OS Command Injection can occur in JavaScript, with examples for various frameworks and methods.

#### Node.js Standard Library
- **`child_process.exec` method**:
    ```javascript
    const { exec } = require('child_process');
    const userInput = 'someInput'; // User-controlled input
    exec(`ls -l ${userInput}`, (err, stdout, stderr) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log(stdout);
    });
    ```
    If `userInput` is set to `; rm -rf /`, it can lead to catastrophic results.

- **Mitigation**:
    Ensure that user inputs are sanitized and validated.
    ```javascript
    const { exec } = require('child_process');
    const sanitize = require('sanitize'); // hypothetical sanitization library
    const userInput = sanitize('someInput'); 
    exec(`ls -l ${userInput}`, (err, stdout, stderr) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log(stdout);
    });
    ```

#### Express.js Framework
- **Example with user-provided input in a URL parameter**:
    ```javascript
    const express = require('express');
    const { exec } = require('child_process');
    const app = express();

    app.get('/run/:command', (req, res) => {
        const userCommand = req.params.command;
        exec(userCommand, (err, stdout, stderr) => {
            if (err) {
                res.status(500).send(err.message);
                return;
            }
            res.send(stdout);
        });
    });

    app.listen(3000);
    ```
    Accessing `http://localhost:3000/run/ls;rm -rf /` would be disastrous.

- **Mitigation**:
    Use a whitelist approach to validate commands.
    ```javascript
    const express = require('express');
    const { exec } = require('child_process');
    const app = express();

    app.get('/run/:command', (req, res) => {
        const safeCommands = ['ls', 'pwd'];
        const userCommand = req.params.command;
        if (!safeCommands.includes(userCommand)) {
            res.status(400).send("Invalid command");
            return;
        }
        exec(userCommand, (err, stdout, stderr) => {
            if (err) {
                res.status(500).send(err.message);
                return;
            }
            res.send(stdout);
        });
    });

    app.listen(3000);
    ```

#### Electron Framework
- **Electron vulnerabilities via Node.js**:
    ```javascript
    const { exec } = require('child_process');
    const { ipcMain } = require('electron');

    ipcMain.on('run-command', (event, arg) => {
        exec(arg, (err, stdout, stderr) => {
            if (err) {
                event.reply('command-result', err.message);
                return;
            }
            event.reply('command-result', stdout);
        });
    });
    ```
    Here, using `arg` directly can open the door to command injection.

- **Mitigation**:
    Strip out risky characters and validate input.
    ```javascript
    const { exec } = require('child_process');
    const { ipcMain } = require('electron');
    const escape = require('shell-escape'); // hypothetical escape module

    ipcMain.on('run-command', (event, arg) => {
        const safeArg = escape(arg); // escape potentially dangerous characters
        exec(safeArg, (err, stdout, stderr) => {
            if (err) {
                event.reply('command-result', err.message);
                return;
            }
            event.reply('command-result', stdout);
        });
    });
    ```

### Mitigation Strategies

1. **Avoid Direct Command Execution**: Use language-specific functions or libraries that provide safe handling of required operations (e.g., file handling, database access).
   
2. **Input Validation and Sanitization**: Implement input validation to ensure only safe, expected input is processed. Reject or sanitize anything that deviates from this standard.
   
3. **Parameterization**: Some languages and frameworks provide parameterized functions that can automatically handle input safely.

4. **Using Environment-Specific Escaping/Quoting**: If inputs must be included in commands, ensure they are properly escaped for the specific shell environment to avoid interpretation as commands.

By following these strategies, the risk of OS Command Injection can be significantly reduced, leading to more secure JavaScript applications.

For further references:
- OWASP Cheat Sheet Series【4:0†source】.
- Path traversal prevention .
- Secure coding practices specific to Node.js and Express.js frameworks.

This should provide an author of SAST tool detection rules the detail and breadth required for creating effective rules to detect OS Command Injection vulnerabilities in JavaScript applications.