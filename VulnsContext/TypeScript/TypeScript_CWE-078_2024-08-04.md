# Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') (CWE-078) in TypeScript

###### Understanding Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')

OS Command Injection is a severe type of security vulnerability where an application indirectly allows user input to be part of system command execution without proper neutralization or sanitization of special elements. This can enable an attacker to manipulate the system command in ways that were not intended by the application author. The impact may range from data exposure to complete system compromise.

For example:
```shell
calc
```
would launch the calculator application on Windows. If it were altered to:
```shell
calc & echo "test"
```
it would execute both the calculator application and the command `echo "test"`, showing how special characters can change command behavior【4:0†source】【4:1†source】.

#### Key Concepts:
1. **Argument Injection**: Executing commands along with unexpected additional arguments.
2. **Primary Defense**:
   - **Avoid Calling OS Commands Directly**: Use built-in library functions instead of system commands.
   - **Escape Values**: Properly escape user inputs before executing them in OS commands.
   - **Parameterization and Input Validation**: Enforce separation of command and data using structured mechanisms and validate inputs thoroughly【4:0†source】【4:10†source】.

### Examples of OS Command Injection in TypeScript

When writing SAST rules for detecting OS Command Injection, consider various TypeScript application scenarios, particularly the common frameworks such as Node.js, Angular, and NestJS. 

#### 1. **Node.js**

Node.js allows for running OS commands using modules like `child_process`. Here is a basic example:

```typescript
import { exec } from 'child_process';

const userInput = 'someuserinput';
exec(`ls ${userInput}`, (error, stdout, stderr) => {
    if (error) {
        console.error(`exec error: ${error}`);
        return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
});
```
In this case, if the `userInput` is not properly sanitized, it may allow injection of additional commands【4:16†source】.

**Example of Vulnerable Code:**
```typescript
import { exec } from 'child_process';

const userInput = 'test; rm -rf /';
exec(`ls ${userInput}`, (error, stdout, stderr) => {
    //...
});
```
**Detection Rule:**
- Identify usage of `exec`, `execSync`, `spawn`, `spawnSync` where user-provided data is concatenated into the command string.

#### 2. **Angular**

In Angular, indirect OS command execution might happen if an application calls endpoints that execute system commands. Still, front-end JavaScript can lead to such behaviors indirectly:

```typescript
http.post('http://example.com/api/execCommand', { command: userInput })
  .subscribe((response: any) => console.log(response));
```
In this mock example, if the backend API executes the `command` parameter directly, it poses a risk.

**Example of Vulnerable Backend Code:**
```typescript
import { exec } from 'child_process';

app.post('/api/execCommand', (req, res) => {
  const command = req.body.command;
  exec(command, (error, stdout, stderr) => {
    // ...
  });
});
```
**Detection Rule:**
- Trace API endpoints in the front-end to back-end calls, ensuring user inputs aren't directly executed.

#### 3. **NestJS**

NestJS is widely used for server-side applications. Here is an example:

```typescript
import { Injectable } from '@nestjs/common';
import { exec } from 'child_process';

@Injectable()
export class AppService {
  runCommand(userInput: string): string {
    let result: string;
    exec(`ls ${userInput}`, (error, stdout, stderr) => {
      result = stdout;
    });
    return result;
  }
}
```
**Example of Vulnerable Code:**
```typescript
import { Injectable } from '@nestjs/common';
import { exec } from 'child_process';

@Injectable()
export class AppService {
  runCommand(userInput: string): string {
    exec(`ls ${userInput}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
      }
      console.log(`stdout: ${stdout}`);
    });
  }
}
```
**Detection Rule:**
- Locate and flag usages of child process methods where user inputs are part of the command string without proper sanitization.

### Recommendations for SAST Rules with Low False Positives and Negatives:

1. **String Concatenation and Interpolation**: Detect commands built using concatenation or template literals with dynamic inputs.
2. **Common Methods**: Focus on functions like `exec`, `execSync`, `spawn`, `spawnSync`, and interaction with APIs returning sensitive data if unchecked user inputs are involved.
3. **Sanitization Checks**: Ensure proper validations or escaping mechanisms are applied to user inputs before executing any system command.
4. **Contextual Analysis**: Consider the application flow and variable propagation to accurately detect where user inputs come from and how they're used.
5. **Framework-Specific Practices**: Tailor rules for specific ID patterns and methods used in different frameworks.

In conclusion, writing precise SAST detection rules involves thorough understanding of how user inputs are managed within various frameworks and methods that interact with system commands. Applying contextual analysis aids in minimizing false positives and negatives, making the tool more reliable and effective in detecting OS Command Injection vulnerabilities.