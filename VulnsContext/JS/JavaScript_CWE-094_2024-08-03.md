# Improper Control of Generation of Code ('Code Injection') (CWE-094) in JavaScript

###### Understanding Improper Control of Generation of Code ('Code Injection')

**Improper Control of Generation of Code ('Code Injection')** occurs when an application generates code based on untrusted input, leading to the execution of malicious code. This vulnerability typically arises in dynamic code generation and execution processes where user input is not properly validated, filtered, or sanitized. This can allow attackers to inject and execute arbitrary code, potentially leading to unauthorized actions such as data theft, data manipulation, or taking control of the system.

### JavaScript Code Injection Variations

JavaScript, being used widely for both the client-side and server-side (Node.js) applications, has several touchpoints where code injection can occur. Let's look at some common scenarios, especially in different popular frameworks:

#### 1. **Eval Injection**
The `eval` function evaluates JavaScript code represented as a string. If user input is passed directly to `eval`, it can execute any JavaScript, leading to code injection.

**Example:**
```javascript
let userInput = '1 + 2';
let result = eval(userInput);  // Potentially dangerous if userInput is untrusted
```

**SAST Rule:**
Detect any use of `eval` with user-supplied data. Examples:
- Direct use of `eval(userInput)`
- Dynamic property access using `eval`

#### 2. **Function Constructor Injection**
Similar to `eval`, the `Function` constructor can create new functions from strings.

**Example:**
```javascript
let userFunction = new Function('return ' + userInput);  // Potentially dangerous
userFunction();
```

**SAST Rule:**
Detect the use of the `Function` constructor with user-supplied data.

#### 3. **setTimeout/setInterval Injection**
`setTimeout` and `setInterval` can accept strings to be evaluated, which can be dangerous if these strings include user input.

**Example:**
```javascript
setTimeout("alert('Hello, " + userName + "')", 1000);  // Potentially dangerous
```

**SAST Rule:**
Detect instances of `setTimeout` and `setInterval` where the first argument is a string containing user input.

#### 4. **Template Literals Injection**
When using template literals to construct code dynamically, untrusted data can lead to injection vulnerabilities.

**Example:**
```javascript
let userInput = "maliciousCode();";
let code = `(() => { ${userInput} })()`;
eval(code);  // Potentially dangerous
```

**SAST Rule:**
Detect the use of template literals for constructing dynamic code or functions with user-supplied data.

#### 5. **DOM-based XSS in Frontend Frameworks**
Frameworks like Angular, React, or Vue can be susceptible to code injection if data binding is not handled securely.

**Example (React):**
```javascript
import { useState } from 'react';

function App() {
  const [dangerousHtml, setDangerousHtml] = useState('');

  return (
    <div dangerouslySetInnerHTML={{ __html: dangerousHtml }} />  // Dangerous if user-supplied
  );
}
```

**SAST Rule:**
Detect potential use of `dangerouslySetInnerHTML` in React with data that could be user-supplied. Similar checks for Angular's `innerHTML` binding and Vue's `v-html`.

#### 6. **Server-Side Template Injection (SSTI) in Node.js**
Using template engines like EJS, Pug, or Handlebars improperly can lead to SSTI.

**Example (EJS):**
```javascript
app.get('/user', (req, res) => {
  let user = req.query.user;
  res.render('userProfile', { user: user });  // `user` may include executable code
});
```

**SAST Rule:**
Detect instances where data taken directly from user input is passed to template engines without proper sanitization.

### Conclusion

Improper Control of Generation of Code (Code Injection) in JavaScript can manifest in many ways, from misuse of functions like `eval` to improper handling of data in frontend frameworks. For a SAST tool, focusing on detecting these patterns can help catch various injection points. Implement detection rules that flag:
1. Use of `eval`, `Function`, `setTimeout`, and `setInterval` with user inputs.
2. Usage of template literals that combine strings with user inputs.
3. Unsafe data binding in frontend frameworks (React's `dangerouslySetInnerHTML`, Angular's `innerHTML`, Vue’s `v-html`).
4. Unsafe rendering of templates on the server side in Node.js environments.

These rules, if enforced correctly, will significantly reduce the risk of code injection vulnerabilities in JavaScript applications.