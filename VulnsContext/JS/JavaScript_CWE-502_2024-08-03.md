# Deserialization of Untrusted Data (CWE-502) in JavaScript

###### What is Deserialization of Untrusted Data?

Deserialization of untrusted data refers to the process where an application converts data from a format that can be easily stored or transmitted (serialization) back into an object (deserialization). When this process uses untrusted data, it can lead to severe security vulnerabilities such as arbitrary code execution, denial of service, and other attacks. This is particularly problematic in web applications, where user inputs or third-party data sources can introduce malicious payloads.

### Variations of Deserialization in JavaScript

In JavaScript, deserialization or the improper handling of untrusted data can occur in various ways, particularly in popular frameworks and contexts. Below are scenarios that describe how deserialization vulnerabilities can arise in JavaScript:

#### 1. Use of `eval()`
```javascript
let userData = '{"name":"John"}';
let parsedData = eval('(' + userData + ')');
```
**Danger:** `eval()` parses the string as JavaScript code, running any code within the string, which is a direct security issue.

#### 2. Insecure Handling of JSON Parsing
```javascript
let userData = '{"name":"John", "age":30}';
let parsedData = JSON.parse(userData);
```
**Danger:** If `userData` is sourced from an untrusted input, it could contain unexpected structures or types that could be manipulated.

#### 3. Using `jQuery`'s `load()` Method with Untrusted Data
```javascript
$("#result").load("data.php?userInput=" + userProvidedInput);
```
**Danger:** If user input is not sanitized, it can lead to script injection or other forms of content injection.

#### 4. Direct DOM Manipulation
```javascript
document.getElementById("result").innerHTML = userData;
```
**Danger:** This allows the attacker to inject arbitrary HTML or JavaScript.

#### 5. AngularJS Expressions
```html
<div ng-bind-html="userInput"></div>
```
**Danger:** Older versions of AngularJS that do not sanitize inputs properly can execute embedded expressions.

### SAST Rule Suggestions

To create SAST rules for detecting deserialization vulnerabilities in JavaScript, consider targeting specific patterns and functions that often lead to security issues. Below are some suggested patterns and checks:

**1. Detecting Use of `eval()` Function**
- **Rule:** Flag any usage of `eval()`.
- **Rationale:** `eval()` should be avoided entirely as it poses significant security risks.
```json
{
    "pattern": "eval(__)",
    "message": "Use of eval() is dangerous and should be avoided.",
    "severity": "high"
}
```

**2. Insecure JSON Parsing**
- **Rule:** Flag `JSON.parse()` usage where input originates from an untrusted source.
- **Rationale:** JSON parsing should always be preceded by rigorous input validation.
```json
{
    "pattern": "JSON.parse(__)",
    "message": "Ensure the input to JSON.parse() is sanitized and validated.",
    "severity": "medium"
}
```

**3. Direct DOM Manipulation**
- **Rule:** Flag any assignment to `innerHTML`, `outerHTML`, or `document.write()` where the source is untrusted.
- **Rationale:** These assignments should avoid directly including untrusted data.
```json
{
    "pattern": "__.innerHTML = __",
    "message": "Avoid assigning untrusted data to innerHTML.",
    "severity": "high"
}
```

**4. Untrusted Data in jQuery `load()`**
- **Rule:** Flag `load()` method usage with dynamic parameters.
- **Rationale:** Parameters to `load()` should be validated or sanitized.
```json
{
    "pattern": "$(__).load(__)",
    "message": "Dynamic parameters in jQuery load() should be sanitized.",
    "severity": "medium"
}
```

**5. AngularJS Template Injection**
- **Rule:** Flag use of `ng-bind-html` without proper sanitization.
- **Rationale:** Ensure input binding to AngularJS expressions and HTML is sanitized.
```json
{
    "pattern": "ng-bind-html",
    "message": "Ensure AngularJS template expressions are sanitized.",
    "severity": "high"
}
```

### Detailed Examples and Cases

Here are examples of real-world scenarios and how a SAST tool might flag these issues:

**Example of `eval()` Abuse**
```javascript
// This will be flagged
let userData = prompt("Enter data:");
eval('(' + userData + ')');
```

**Example of Unsanitized JSON Parsing**
```javascript
// This will be flagged
let userData = getUserInput(); // Assuming getUserInput() is untrusted
let parsedData = JSON.parse(userData);
```

**Example of Dangerous DOM Manipulation**
```javascript
// This will be flagged
document.getElementById("result").innerHTML = getUserInput(); // User-provided input directly to innerHTML
```

### References
Consider referring to the OWASP Deserialization Cheat Sheet and other resources for additional guidance:

- [OWASP Deserialization Cheat Sheet](https://owasp.org/www-cheat-sheet-series/Deserialization_Cheat_Sheet.html)
- [OWASP Software and Data Integrity Failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)【4:6†source】   

Use these guidelines to inform detection rule creation in SAST tools, ensuring robust checks against deserialization vulnerabilities in JavaScript applications.