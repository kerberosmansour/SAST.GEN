# Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') (CWE-079) in TypeScript

#### Explanation of Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')

### What is Cross-Site Scripting (XSS)?
Cross-site scripting (XSS) is a type of security vulnerability typically found in web applications. It allows attackers to inject malicious scripts into content from otherwise trusted websites. Due to the improper neutralization of input during the generation of web pages, an attacker can execute scripts in the context of a user’s browser, potentially compromising user interactions with the web application.

### Types of XSS
1. **Stored XSS**: The malicious script is stored on the target server, such as in a database, message forum, visitor log, comment field, etc. The script is executed when the victim requests the stored information.
2. **Reflected XSS**: The malicious script is reflected off a web server to the user's browser. This happens when data provided by a web user is immediately used by the server to generate a response.
3. **DOM-based XSS**: The vulnerability exists in the client-side code rather than server-side code, and the attack is executed in the user's browser.

### CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
According to the CWE (Common Weakness Enumeration), CWE-79 is the improper neutralization of input used in web page generation. This can result in the execution of malicious scripts by the web browser.

## Examples of XSS in TypeScript with Popular Frameworks

### 1. Plain TypeScript with Vanilla JS

#### Example:
```typescript
// Accepts user input and sets it in the innerHTML of an element
document.getElementById("example").innerHTML = userInput;
```
#### Risk:
If `userInput` contains scripts, they will be executed in the browser.

#### SAST Rule:
Detect the usage of `innerHTML` being assigned with any external input without proper sanitization or encoding.

### 2. Angular Framework

#### Example:
```typescript
@Component({
  selector: 'app-example',
  template: `<div [innerHTML]="userInput"></div>`
})
export class ExampleComponent {
  userInput: string;
  constructor() {
    this.userInput = "<script>alert('XSS');</script>";
  }
}
```
#### Risk:
Angular does sanitize by default, but the use of `[innerHTML]` binding can still introduce risk if the sanitizer is bypassed.

#### SAST Rule:
Detect `[innerHTML]` property binding combined with any potentially unsafe inputs.

### 3. React Framework

#### Example:
```tsx
class ExampleComponent extends React.Component {
  render() {
    return <div dangerouslySetInnerHTML={{ __html: this.props.userInput }} />;
  }
}
```
#### Risk:
Using `dangerouslySetInnerHTML` risks executing any script present within `userInput`.

#### SAST Rule:
Flag the usage of `dangerouslySetInnerHTML` and ensure that the content is sanitized before assignment.

### 4. Vue.js Framework

#### Example:
```typescript
new Vue({
  data: {
    userInput: '<script>alert("XSS")</script>'
  },
  template: '<div v-html="userInput"></div>'
});
```
#### Risk:
The `v-html` directive binds raw HTML to the element, risking XSS.

#### SAST Rule:
Detect the usage of `v-html` with inputs from untrusted sources.

### 5. Express.js with Server-Side Rendering

#### Example:
```typescript
app.get('/example', (req, res) => {
  res.send(`<div>${req.query.userInput}</div>`);
});
```
#### Risk:
The unescaped user input `req.query.userInput` is rendered directly into the HTML.

#### SAST Rule:
Inspect the usage of methods like `res.send` that output raw HTML containing user inputs without encoding or escaping.

### General SAST Detection Considerations
1. **Identification of Sinks**: Look for functions or properties like `innerHTML`, `outerHTML`, `document.write`, `dangerouslySetInnerHTML`, `v-html`, and template literals in rendering functions.
2. **Source Identification**: Track data from sources like `req.body`, `req.query`, `location.search`, user-controlled component props, etc.
3. **Data Flow Analysis**: Determine if data from an untrusted source flows into a dangerous sink without being properly sanitized or encoded.
4. **Framework-Specific Practices**: Incorporate rules specific to how each framework handles data binding and output, as built-in mitigations may vary.

### Summary
Improper neutralization of input can lead to severe security vulnerabilities such as XSS. Framework-specific rules can help in building an effective SAST tool to detect XSS vulnerabilities in TypeScript applications. This ensures a low false positive and negative rate by focusing on common pitfalls in popular frameworks.

For references:
- CWE-79【4:0†source】【4:1†source】【4:2†source】【4:3†source】【4:4†source】
- XSS prevention practices and guidelines【4:17†source】【4:18†source】【4:19†source】