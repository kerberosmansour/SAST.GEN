# Improper Neutralization of Special Elements used in a Command ('Command Injection') (CWE-077) in JavaScript

###### Improper Neutralization of Special Elements used in a Command ('Command Injection')

#### Explanation

Improper neutralization of special elements used for command execution, commonly known as Command Injection, occurs when an application constructs all or part of an operating system command using input data supplied by a potential attacker without proper validation or sanitization. This vulnerability can allow an attacker to execute arbitrary commands on the host operating system via a vulnerable application. This happens because user-controlled data can alter the way commands work by adding unintended special characters or commands.

For instance, a web application might pass input directly to system commands such as shell scripts without appropriate sanitation:
```javascript
const { exec } = require('child_process');
app.post('/execute', (req, res) => {
    const command = req.body.command;  // Potentially dangerous input
    exec(command, (error, stdout, stderr) => {
        if (error) {
            res.send(`Error: ${stderr}`);
        } else {
            res.send(`Output: ${stdout}`);
        }
    });
});
```

#### Variations of Command Injection in JavaScript

##### 1. Basic Command Injection
In JavaScript, especially within Node.js applications, basic command injection occurs when untrusted input is directly used in command execution functions, such as `exec`, `execFile`, `spawn`, and similar functions in the `child_process` module.

**Example:**
```javascript
const {exec} = require('child_process');
const userInput = "ls; rm -rf /";   // Dangerous input
exec(userInput, (err, stdout, stderr) => {
    if(err) {
        console.error(`exec error: ${err}`);
        return;
    }
    console.log(`stdout: ${stdout}`);
    console.log(`stderr: ${stderr}`);
});
```

##### 2. Argument Injection
In scenarios where additional arguments can be passed, an attacker can inject additional flags or commands, exploiting the way arguments are handled.

**Example:**
```javascript
const {execFile} = require('child_process');
const userUrl = "example.com; rm -rf /";
execFile('curl', [userUrl], (error, stdout, stderr) => {
    if (error) {
        console.error(`execFile error: ${error}`);
    } else {
        console.log(`stdout: ${stdout}`);
        console.log(`stderr: ${stderr}`);
    }
});
```

##### 3. Template Injection leading to Command Injection
In web applications using template engines, untrusted data injected into template contexts can lead to command injection if the templates are rendered in a context that executes commands.

**Example with untrusted input in a template engine**:
```javascript
app.post('/render', (req, res) => {
  const template = 'Hello ${name}!';
  const name = req.body.name;  // Potentially dangerous input
  const result = eval('`' + template + '`');  // Dangerous - evaluates untrusted input
  res.send(result);
});
```

##### Detection for SAST Tools

To detect these vulnerabilities in a SAST tool, the rules should:
1. Identify usage of command execution functions (`exec`, `execFile`, `spawn`, etc.) and flag instances where these functions use user inputs.
2. Trace the flow of input data to ensure that it does not come from untrusted sources leading directly or indirectly into command execution.
3. Recognize template rendering contexts where evaluation of code happens, especially those evaluating untrusted data.
4. Detect lack of validation or escaping special characters in user inputs before they are concatenated into any command strings.

**Summary of patterns to look for:**
- Command execution API with direct, unvalidated user input.
- Presence of special characters within strings concatenated into commands (`;`, `&&`, `||`, `|`, `${}`, etc.).
- Use of `eval` or other dynamic code evaluation functions on data obtained directly from user inputs.

**References:**
- OWASP Testing Guide on [Command Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/12-Testing_for_Command_Injection)【4:0†source】
- OWASP [Command Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Command_Injection_Prevention_Cheat_Sheet.html) 

Developing rules for detecting these patterns will help in early identification and mitigation of Command Injection vulnerabilities in JavaScript applications, thus improving their security posture.