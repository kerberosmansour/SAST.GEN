# Improper Certificate Validation (CWE-295) in JavaScript

ImproImproper Certificate Validation is a security vulnerability that occurs when a system does not properly validate certificates, which can enable man-in-the-middle (MitM) attacks, interception of encrypted communications, and other security risks. This vulnerability is characterized by a failure to verify certificates against a trusted certificate authority (CA) or an improper matching of the certificate to the host.

### Variations of Improper Certificate Validation in JavaScript

Improper certificate validation can manifest in JavaScript applications, particularly those using various frameworks and libraries for making HTTPs requests. Here are some common variations:

1. **Ignoring Certificate Errors in Node.js**

   In Node.js applications, using the `https` module improperly can lead to ignoring certificate errors. Below is an example:

   ```javascript
   const https = require('https');

   const options = {
     hostname: 'example.com',
     port: 443,
     path: '/',
     method: 'GET',
     rejectUnauthorized: false // This disables certificate validation
   };

   const req = https.request(options, (res) => {
     // ... handle response
   });

   req.end();
   ```

   Setting `rejectUnauthorized: false` disables SSL certificate validation, making the application vulnerable to MitM attacks.

2. **Improper Handling in Axios (JavaScript Library)**

   Axios is a popular library for making HTTP requests in JavaScript. Improperly configuring Axios can also lead to certificate validation issues:

   ```javascript
   const axios = require('axios');

   // Disabling SSL verification
   const instance = axios.create({
     baseURL: 'https://example.com',
     httpsAgent: new (require('https').Agent)({
       rejectUnauthorized: false // This disables certificate validation
     })
   });

   instance.get('/path')
     .then(response => {
       console.log(response.data);
     });
   ```

3. **Insecure Implementations in Fetch API**

   The Fetch API, available in the browser, does not provide direct options for certificate validation. However, using insecure third-party proxies or configurations can inadvertently expose vulnerabilities:

   ```javascript
   // Example where a proxy is used without validation
   fetch('https://example.com', {
     method: 'GET',
     // no option to disable SSL checks directly in Fetch API
   }).then(response => {
     return response.json();
   }).then(data => {
     console.log(data);
   }).catch(error => {
     console.log('Error: ', error);
   });
   ```

4. **Bypassing Validation in Request-Promise (JavaScript Library)**

   Request-Promise is another HTTP request library that can be misconfigured similarly:

   ```javascript
   const rp = require('request-promise');

   const options = {
     uri: 'https://example.com',
     rejectUnauthorized: false // Disables certificate validation
   };

   rp(options)
     .then(function (response) {
       console.log(response);
     })
     .catch(function (err) {
       console.error(err);
     });
   ```

### Writing SAST Rules for Detection

To detect improper certificate validation in JavaScript, here are the key patterns and configurations a SAST tool should look for:

1. **Pattern for Node.js `https` Module**:

   - Check for `rejectUnauthorized: false` in `https.request` or `https.get`.

2. **Pattern for Axios**:

   - Look for the creation of Axios instances with `httpsAgent` having `rejectUnauthorized: false`.

3. **Pattern for Request-Promise**:

   - Identify `rp` or `request` options where `rejectUnauthorized: false`.

4. **Custom JWT Verification**:

   - Code patterns where custom JWT token verifications are done incorrectly, bypassing native library verifications.

Example Pseudo-Rules:

1. **Node.js Detection**:
   ```regex
   \bhttps\.request\s*\(\s*\{[^\}]*rejectUnauthorized\s*:\s*false[^\}]*\}\s*\)
   ```

2. **Axios Detection**:
   ```regex
   \baxios\.create\s*\(\s*\{[^\}]*httpsAgent\s*:\s*new\s*\(\s*require\s*\('\s*https\s*'\)\.Agent\s*\(\s*\{[^\}]*rejectUnauthorized\s*:\s*false[^\}]*\}\s*\)[^\}]*\}\s*\)
   ```

3. **Request-Promise Detection**:
   ```regex
   \brp\s*\(\s*\{[^\}]*rejectUnauthorized\s*:\s*false[^\}]*\}\s*\)
   ```

By detecting these patterns, a SAST tool can alert developers about potential improper certificate validation issues, prompting them to secure their HTTP requests and enforce proper SSL/TLS practices【4:0†source】【4:1†source】【4:2†source】【4:3†source】【4:4†source】.