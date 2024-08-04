# Improper Control of Generation of Code ('Code Injection') (CWE-094) in TypeScript

###### What is Improper Control of Generation of Code (Code Injection)?

Improper Control of Generation of Code, commonly known as Code Injection, is a security vulnerability where an attacker can insert malicious code into a program due to incomplete or missing input validation. This vulnerability arises when software constructs part or all of its executed code using externally-supplied input, without ensuring that this input is properly sanitized. When successful, this can lead to unauthorized execution of code, potentially granting an attacker control over the host system.

#### Key Points:
1. **User-Supplied Data**: This is not validated, filtered, or sanitized by the application.
2. **Dynamic Execution**: The application dynamically executes code using the raw or improperly sanitized input.
3. **Security Impact**: This can lead to unauthorized actions, including data manipulation, privilege escalation, or system compromise.

For more information, refer to the Common Weakness Enumeration CWE-94: [Improper Control of Generation of Code ('Code Injection')](https://cwe.mitre.org/data/definitions/94.html)【4:0†source】【4:10†source】【4:1†source】.

### Code Injection in TypeScript

Code Injection in TypeScript, particularly within popular frameworks, can occur in various ways. Below, we provide detailed examples and strategies that a SAST tool detection rule author can employ to identify potential vulnerabilities with high precision.

#### General TypeScript Example

```typescript
// Vulnerable Code
const userCode = "console.log('User input');"; // Example of user input prone to injection
eval(userCode); // Dangerous use of eval
```

In the example above, using `eval` to execute user-supplied code should be avoided. Instead, safer alternatives such as template engines or strict validation should be employed for any dynamic content generation.

#### Example in Express.js

```typescript
import express from 'express';
const app = express();

app.get('/runCode', (req, res) => {
    const code = req.query.code;
    // Vulnerable: Directly running user input
    eval(code); // Unsafe
    res.send('Code executed');
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
```

Here, `eval` is used to execute the `code` parameter from the request query. This poses a significant security risk. A SAST rule should flag any use of `eval` or similar functions (`Function`, `setTimeout`, `setInterval` with string arguments) and suggest safer alternatives.

#### Example in Angular

```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `<div [innerHTML]="dynamicHtml"></div>`
})
export class AppComponent {
  dynamicHtml: string;

  constructor() {
    const userContent = "<script>alert('Hacked!');</script>"; // Example of user-supplied content
    this.dynamicHtml = userContent; // Unsafe
  }
}
```

In this Angular example, binding `innerHTML` to user-supplied content can lead to Cross-Site Scripting (XSS) which, in turn, might allow injection attacks. The SAST rule should analyze HTML bindings (`innerHTML`, `outerHTML`, etc.) and suggest sanitization.

#### Example in React

```typescript
import React from 'react';

class MyComponent extends React.Component {
  render() {
    const userCode = "console.log('Hello World');"; // User input
    // Vulnerable: Using Function constructor with user input
    new Function(userCode)(); // Unsafe
    return <div>Code executed</div>;
  }
}

export default MyComponent;
```

The use of the `Function` constructor with user input is as dangerous as `eval`. It should be flagged by the SAST tool.

### Detection Rules Recommendations

1. **Identify Dangerous Functions**: Flag the use of `eval`, `Function`, `setTimeout`, `setInterval` where inputs are not sufficiently sanitized.
2. **HTML Binding Analysis**: In frameworks like Angular, React, Vue, analyze the bindings to DOM properties like `innerHTML`, and ensure these bindings are either sanitized or avoided for user input.
3. **Whitelist Approach for APIs**: Encourage the whitelisting of safe APIs and discourage the direct use of dynamic code execution methods.
4. **Static Code Scanning**: Scan for patterns where user inputs are directly fed into the application's critical execution paths without proper validation or escaping.

By focusing on these areas, the rule sets developed for the SAST tool can effectively minimize false positives and negatives, thereby enhancing the security posture of TypeScript applications developed using popular frameworks like Express.js, Angular, and React.

Remember, detecting code injection vulnerabilities requires a combination of syntactic scanning for dangerous function calls and semantic analysis ensuring proper input validation and sanitization.