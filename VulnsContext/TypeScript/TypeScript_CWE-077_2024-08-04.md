# Improper Neutralization of Special Elements used in a Command ('Command Injection') (CWE-077) in TypeScript

###### Understanding Command Injection

**Improper Neutralization of Special Elements in a Command ('Command Injection')**, commonly referred to as command injection, is a type of security vulnerability that occurs when an application constructs a command or system call using user input without properly neutralizing special characters. This allows attackers to alter the command's intended behavior, potentially executing arbitrary commands on the system.

For example, consider a scenario where a web application executes a system command to list files in a directory, using a user-provided directory name. If the application simply includes the user input directly into the command, an attacker could provide input like `; rm -rf /`, causing the application to execute a command that deletes all files on the system instead of just listing files  .

### Command Injection in TypeScript

In the context of TypeScript, command injection vulnerabilities can occur in applications utilizing system commands, particularly in server-side environments such as Node.js. Here are some practical examples illustrating various frameworks:

1. **Basic Node.js Example**:

   ```typescript
   import { exec } from 'child_process';

   const userDir = process.argv[2]; // User input from command-line arguments
   exec(`ls ${userDir}`, (error, stdout, stderr) => {
       if (error) {
           console.error(`Error: ${error}`);
           return;
       }
       console.log(`Output: ${stdout}`);
   });
   ```

   *Issue*: If `userDir` contains special characters like `;`, `&`, or `|`, an attacker could inject additional commands.

2. **Express.js Framework**:

   ```typescript
   import * as express from 'express';
   import { exec } from 'child_process';

   const app = express();
   
   app.get('/list-files', (req, res) => {
       const userDir = req.query.dir; // User input from query parameters
       exec(`ls ${userDir}`, (error, stdout, stderr) => {
           if (error) {
               res.status(500).send(`Error: ${error}`);
               return;
           }
           res.send(`Output: ${stdout}`);
       });
   });

   app.listen(3000, () => {
       console.log('Server is running on port 3000');
   });
   ```

   *Issue*: If `userDir` is not sanitized, an attacker can inject commands via the `dir` query parameter.

3. **Electron Framework**:

   ```typescript
   import { exec } from 'child_process';
   import { ipcMain } from 'electron';

   ipcMain.on('list-files', (event, userDir) => {
       exec(`ls ${userDir}`, (error, stdout, stderr) => {
           if (error) {
               event.sender.send('error', `Error: ${error}`);
               return;
           }
           event.sender.send('output', `Output: ${stdout}`);
       });
   });
   ```

   *Issue*: If `userDir` comes from user input in the renderer process, it needs to be sanitized.

### Developing SAST Rules

When developing SAST rules to detect command injection vulnerabilities, consider the following patterns present in the examples:

1. **Identify functions prone to command injection**:
   - Common functions like `exec()`, `execSync()`, `spawn()`, and `spawnSync()` from the `child_process` module are often vulnerable if the input is not sanitized.

2. **Track data flow from user inputs**:
   - Sources of user inputs include `process.argv`, HTTP request parameters (`req.query`, `req.body` in Express), and IPC messages in Electron.

3. **Detect unsafe string interpolation in commands**:
   - Look for concatenated commands where user input might include special characters to alter the intended command execution.

**Example SAST Detection Rule for Node.js**:
- **Pattern**:
  ```typescript
  const { exec } = require('child_process');
  const userInput = /* potential user input source */;
  exec(`command ${userInput}`, /* ...callback */);
  ```
- **Logic**:
  1. Identify `exec` or related command execution functions.
  2. Check for inclusion of variables directly in the command string.
  3. Trace the variable back to potential user input sources.

### Recommendations

1. **Avoid Command Usage**:
   - Prefer using safer, high-level APIs provided by the programming environment.

2. **Sanitize Inputs**:
   - Use libraries such as `shell-escape` to sanitize user inputs before including them in commands.

3. **Use Parameterized Commands**:
   - When available, use APIs that accept command parameters separately from the command to avoid the need for concatenation.

By recognizing these patterns and incorporating comprehensive input validation, developers can mitigate the risks of command injection vulnerabilities in TypeScript applications across various frameworks  .