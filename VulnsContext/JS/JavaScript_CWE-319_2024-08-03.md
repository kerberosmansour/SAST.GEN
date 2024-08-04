# Cleartext Transmission of Sensitive Information (CWE-319) in JavaScript

###### Cleartext Transmission of Sensitive Information

**Cleartext Transmission of Sensitive Information** occurs when sensitive data is transmitted across a network in an unencrypted format. This leaves the data vulnerable to interception and unauthorized access by attackers. Sensitive information can include credentials, personal data, and financial information, among others. Common vectors include HTTP, FTP, SMTP, and other protocols that do not enforce encryption.

**Preventive measures**:
1. Always use secure protocols such as HTTPS for transmitting sensitive data.
2. Ensure all data in transit is encrypted with strong algorithms.
3. Disable protocols that do not support encryption.
4. Implement HTTP Strict Transport Security (HSTS) to enforce the use of HTTPS.
5. Properly configure firewalls and network controls to block unencrypted traffic.

### Variations in JavaScript and Frameworks

In JavaScript (including Node.js and popular frameworks like Express, React, Angular, and Vue.js), cleartext transmission of sensitive information can occur in several ways. Here are some examples and how a SAST (Static Application Security Testing) tool might detect these vulnerabilities:

1. **Sending Sensitive Data over HTTP**:
   ```javascript
   // Example of sensitive data being sent over HTTP
   const xhr = new XMLHttpRequest();
   xhr.open("POST", "http://example.com/api/login", true);
   xhr.setRequestHeader("Content-Type", "application/json");
   xhr.send(JSON.stringify({username: "user", password: "password"}));
   ```

2. **Unprotected WebSocket Communication**:
   ```javascript
   const ws = new WebSocket('ws://example.com/socket');
   ws.onopen = function () {
       ws.send('Sensitive data');
   };
   ```

3. **Hardcoding Sensitive Information**:
   ```javascript
   const apiKey = "1234567890";
   // usage: sending apiKey in an unsecured way
   fetch(`http://example.com/data?api_key=${apiKey}`)
       .then(response => response.json())
       .then(data => console.log(data));
   ```

4. **Misconfigured AJAX Requests in jQuery**:
   ```javascript
   $.ajax({
       type: "POST",
       url: "http://example.com/api/endpoint",
       data: JSON.stringify({ sensitiveData: "secret" }),
       contentType: "application/json",
       success: function (response) {
           console.log("Data sent successfully");
       }
   });
   ```

5. **Forms submitting over HTTP**:
   ```html
   <form action="http://example.com/login" method="POST">
       <input type="text" name="username">
       <input type="password" name="password">
       <input type="submit" value="Login">
   </form>
   ```

6. **Vue.js HTTP Requests**:
   ```javascript
   axios.post('http://example.com/login', {
       username: 'user',
       password: 'pass'
   })
   .then(response => console.log(response))
   .catch(error => console.error(error));
   ```

**SAST Rule Implementation**:
To detect these vulnerabilities, a SAST tool should inspect:
- Usage of insecure protocols (e.g., `http://` or `ws://` instead of `https://` or `wss://`).
- Hardcoded sensitive information such as API keys, tokens, passwords in the code.
- Form action URLs not using HTTPS.
- Sensitive data in network requests that are not encrypted.

**Example Patterns for SAST Detection**:
1. **Insecure Protocol Usage**:
   - Pattern: `http://` in URL strings
   - Pattern: `ws://` in WebSocket connections

2. **Hardcoded Sensitive Information**:
   - Pattern: Variable names and constants matching "key", "token", "secret", "password" etc., with string values.

3. **Unsecured Form Actions**:
   - Pattern: `<form action="http://"`

**Extended Prevention Tips**:
1. Leverage environment variables for sensitive information and avoid hardcoding.
2. Centralize network request configurations to enforce HTTPS and reuse consistent security settings.
3. Regularly audit and refactor code to replace unguarded practices with secure alternatives.
4. Educate developers on the importance of securing data in transit to preempt negligent patterns from emerging.

**References**:
- CWE-319 Cleartext Transmission of Sensitive Information    .