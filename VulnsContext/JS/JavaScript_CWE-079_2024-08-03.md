# Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') (CWE-079) in JavaScript

###### Overview of Improper Neutralization of Input During Web Page Generation (Cross-site Scripting or XSS)
Improper Neutralization of Input During Web Page Generation, commonly known as Cross-site Scripting (XSS), is a security vulnerability that occurs when an application includes untrusted data in a web page without proper validation or escaping. This can lead to the execution of malicious scripts in the context of a user's browser, enabling attackers to steal sensitive information, hijack user sessions, and perform other malicious activities.

### Types of XSS
1. **Stored XSS**: This occurs when a malicious script is stored on the server (e.g., in a database) and executed when the victim requests the stored data.
2. **Reflected XSS**: This occurs when a malicious script is reflected off a web server, such as in an error message or search result, and is executed immediately by the victim's browser.
3. **DOM-based XSS**: This occurs when the source of the data to be executed as code is based on DOM objects and can be manipulated on the client side.

### Examples of Potential XSS Vulnerabilities in JavaScript

#### 1. InnerHTML Assignment
```javascript
// Example of insecure innerHTML assignment
document.getElementById('output').innerHTML = userInput;
```
**Explanation**: If `userInput` contains malicious script tags, they will be executed by the browser.

#### 2. Unsafe Event Handlers
```javascript
// Example of insecure onclick attribute
someElement.setAttribute('onclick', userInput);
```
**Explanation**: Malicious code in `userInput` can be executed during the onclick event.

#### 3. Location and URL Manipulation
```javascript
// Example of insecure location.href manipulation
window.location.href = userInput;
```
**Explanation**: If `userInput` contains "javascript:" or other dangerous protocols, it can lead to XSS.

#### 4. Unsafe Data Insertion into DOM
```javascript
// Example of insecure document.write usage
document.write(userInput);
```
**Explanation**: Directly writing untrusted input into the document can execute any script content within `userInput`.

### Securing Against XSS

1. **Using textContent and innerText**
```javascript
// Safe method using textContent
document.getElementById('output').textContent = userInput;
```
**Explanation**: `textContent` automatically escapes any HTML in `userInput`, rendering it as plain text.

2. **Using Safe Methods for Attribute Assignment**
```javascript
// Safe attribute assignment
someElement.onclick = () => {
    // Function does not use any user input
};
```
**Explanation**: Directly assigning event handlers through property assignments instead of using `setAttribute`.

### XSS in Popular JavaScript Frameworks

#### 1. AngularJS (Pre-1.6)
```javascript
// Example of AngularJS binding (pre-1.6 versions)
<div ng-bind-html="userInput"></div>
```
**Mitigation**: Use Angular’s built-in `$sce` service to mark trusted HTML.

#### 2. React
```javascript
// Example of React’s dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{__html: userInput}} />
```
**Mitigation**: Avoid using `dangerouslySetInnerHTML`. If necessary, ensure the input is sanitized using a library like DOMPurify.

#### 3. Vue.js
```javascript
// Example of Vue.js v-html directive
<div v-html="userInput"></div>
```
**Mitigation**: Use `v-text` for safe rendering. If `v-html` is absolutely necessary, sanitize the input.

### Writing SAST Rules for XSS Detection

When writing rules for a Static Application Security Testing (SAST) tool to detect XSS instances, consider the following patterns:

1. **DOM Updates and Assignments**:
    - Detect usages of `innerHTML`, `outerHTML`, `document.write()`, `setAttribute()`, and similar functions when coupled with untrusted input.
    
2. **Event Handlers**:
    - Identify direct assignments to event handlers (e.g., `onclick`, `onload`) that incorporate user-controlled data.

3. **Framework-Specific Practices**:
    - For AngularJS, track bindings that use `ng-bind-html`.
    - For React, identify usages of `dangerouslySetInnerHTML`.
    - For Vue.js, flag uses of `v-html`.

### Example of a SAST Rule in Pseudo-code:

```pseudo
// Detect uses of innerHTML with unsanitized input
rule DetectInnerHTMLAssignment {
    when
    findAssignment(target: 'innerHTML' OR target: 'outerHTML')
    with untrustedSource
    then
    log "Potential XSS vulnerability in innerHTML assignment"
}

// Detect uses of setAttribute with unsafe events
rule DetectSetAttribute {
    when
    findSetAttribute(attr: 'onclick' OR attr: 'onmouseover' etc.)
    with untrustedValue
    then
    log "Potential XSS vulnerability in setAttribute usage"
}
```

### Conclusion
Understanding XSS vulnerabilities and patterns in JavaScript is essential for writing effective SAST rules to detect and mitigate these issues. Following the principles and examples provided will help in identifying and securing code against XSS attacks effectively.

For more details, you can refer to the OWASP guidelines and other resources mentioned in the uploaded documents, such as [CWE-79 - Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')](https://cwe.mitre.org/data/definitions/79.html)【4:0†source】.