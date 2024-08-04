# Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') (CWE-917) in JavaScript

###### Explanation of Improper Neutralization of Special Elements used in an Expression Language Statement (Expression Language Injection)

Improper Neutralization of Special Elements used in an Expression Language Statement, also known as Expression Language (EL) Injection, occurs when untrusted user input is used in an expression language statement without proper sanitization. Expression Language is often used in templating engines to dynamically generate content based on user input. Failure to properly sanitize this input can lead to several security issues, including data leakage, remote code execution, or unauthorized access.

### How EL Injection Occurs

EL Injection can occur when user input is incorrectly handled by an application, allowing an attacker to introduce special characters or elements into the expression language statement. These inputs can then alter the execution flow or logic of the application.

### Examples in JavaScript and Popular Frameworks

1. **Generic JavaScript Example**
   ```javascript
   // Dangerous use of user input in an evaluation context
   const userExpression = req.query.expression;
   eval(`result = ${userExpression}`);

   // If the user input is `2 + 2`, this works as intended
   // But if the user input is `2 + 2; process.exit()`, it can crash the server
   ```

2. **Using `eval` function**
   ```javascript
   // Assuming 'userData' is input from the user
   let userData = req.body.data;
   eval(userData);

   // Malicious input like `console.log('Hacked');` can execute arbitrary code
   ```

3. **Using `setTimeout` or `setInterval` with user input**
   ```javascript
   setTimeout("console.log(" + userInput + ")", 1000);

   // User input `1); alert('hacked');//` will run like 
   // setTimeout("console.log(1); alert('hacked');//", 1000);
   ```

4. **Template Engine Example (like Pug.js or EJS)**
   ```javascript
   // In Pug template
   p= "#{" + userInput + "}"

   // Unsafe usage allows attacker to inject scripts
   ```

5. **Framework Specific Examples**

   - **AngularJS (before Angular versions 1.6)**
     ```html
     <div ng-bind-html="userInput"></div> 

     // User input with AngularJS statements like `{{ 4 + 4 }}` can be executed
     ```

   - **React.js (if dangerouslySetInnerHTML is used without sanitization)**
     ```javascript
     const userInput = '<img src=x onerror=alert(1)//>';
     const element = <div dangerouslySetInnerHTML={{__html: userInput}}></div>;

     // This can execute userInput as HTML/JS
     ```

6. **String-based EL Injection in Vue.js**
   ```javascript
   new Vue({
       data: {
           message: userInput // User input can manipulate the message variable if not properly sanitized
       }
   });
   ```

### Mitigation Strategies

- **Sanitize Input:** Always sanitize input using libraries such as DOMPurify for HTML or escape sequences for strings in evaluation contexts.
- **Avoid `eval` and Similar Functions:** Refrain from using `eval` and other functions that execute code from strings, like `setTimeout` and `setInterval` with string arguments.

### Detection in SAST Tools

To detect potential EL injection vulnerabilities in a Static Application Security Testing (SAST) tool, look for the following patterns:

- Usage of `eval`, `setTimeout`, `setInterval` functions with dynamic content.
- Instances of `dangerouslySetInnerHTML` in React without sanitization.
- Expressions embedded in AngularJS templates without proper binding (before Angular 1.6).
- Direct assignment of user inputs into templating engines without proper sanitization.

By scanning for these patterns and applying static analysis, it is possible to identify and mitigate potential EL injection vulnerabilities in JavaScript applications.

### References
- OWASP: CWE-917 Improper Neutralization of Special Elements used in an Expression Language Statement (Expression Language Injection)【4:0†source】 
- OWASP Prevention Cheat Sheets: Injection Prevention Cheat Sheet【4:0†source】

This comprehensive understanding should assist in writing robust SAST rules to detect EL injection vulnerabilities across various JavaScript frameworks and generic implementations.