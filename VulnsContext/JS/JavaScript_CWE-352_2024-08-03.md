# Cross-Site Request Forgery (CSRF) (CWE-352) in JavaScript

###### What is Cross-Site Request Forgery (CSRF)?

Cross-Site Request Forgery (CSRF) is a type of attack that tricks a user into executing unwanted actions on a web application in which they're currently authenticated. An attacker can cause the user to perform actions like changing account details, making purchases, transferring funds, or other activities that the authenticated user is permitted to do.

This attack leverages the fact that web browsers automatically include relevant cookies (including session cookies) with each request made to a web application. As a result, malicious requests can appear legitimate to the web application if it does not properly validate the identity of the requester. For instance, if a logged-in user visits a malicious website, the site might carry out unauthorized actions on the user's behalf by exploiting their authenticated session with another site.

### General Principles for Mitigating CSRF

1. **Use Built-In CSRF Protection**: Many modern web frameworks provide built-in CSRF protection mechanisms. Where available, these should be the first line of defense.
2. **Token-Based Mitigation**: Use CSRF tokens to ensure that state-changing requests originate from the same source as the user’s current session.
3. **Double Submit Cookies**: This technique involves sending the CSRF token in both a cookie and a request parameter.
4. **Custom Request Headers**: For AJAX requests, custom headers can be employed to bypass CSRF attacks.
5. **Defense in Depth**: Supplement primary defenses with secondary measures, such as SameSite cookie attributes and origin verification.
6. **Avoid State-Altering GET Requests**: Do not utilize GET requests for state-changing operations as they are inherently more vulnerable to CSRF.

### Variations and Examples of CSRF in JavaScript

To help build SAST rules for detecting CSRF vulnerabilities in JavaScript applications, consider the following scenarios and examples:

1. **Basic CSRF Example**:
   ```html
   <!-- Malicious form that might be placed on an attacker's site -->
   <form action="https://trusted-site.com/change-email" method="post">
      <input type="hidden" name="email" value="attacker@example.com" />
   </form>
   <script>
      document.forms[0].submit(); // Submits the form automatically
   </script>
   ```

2. **CSRF Using XMLHttpRequest (AJAX)**:
   ```js
   // A JavaScript snippet on an attacker's site that sends a request to a victim site
   var xhr = new XMLHttpRequest();
   xhr.open('POST', 'https://trusted-site.com/account/delete', true);
   xhr.withCredentials = true; // Send cookies if the cookies flag is true for the user agent
   xhr.send();
   ```

3. **CSRF in Single Page Applications (SPA)**:
   - **Angular.js**: By default, Angular.js supports CSRF protection by sending a XSRF-TOKEN cookie and expecting it back in an X-XSRF-TOKEN header.
   ```js
   // Angular specific CSRF protection method
   $http({
       method: 'POST',
       url: 'https://trusted-site.com/api/request',
       headers: {'X-XSRF-TOKEN': $cookies.get('XSRF-TOKEN')}
   });
   ```

   - **React.js/Redux**: Explicitly send CSRF tokens stored as cookies:
   ```js
   const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
   fetch('https://trusted-site.com/api/request', {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json',
           'X-CSRF-Token': csrfToken
       },
       credentials: 'include',
       body: JSON.stringify({data: 'example'})
   });
   ```

4. **CSRF in Vue.js**:
   ```js
   axios.defaults.withCredentials = true; // Include credentials
   axios.post('https://trusted-site.com/api/request', {
       data: 'example'
   }, {
       headers: {
           'X-CSRF-Token': 'your-csrf-token-value'
       }
   });
   ```

5. **Asynchronous CSRF Protection by Custom Headers**:
   - A setup that employs custom headers to protect against CSRF in an API-driven app:
   ```js
   // Custom header method for CSRF protection
   fetch('https://trusted-site.com/api/submit', {
       method: 'POST',
       headers: {
           'X-Custom-Header': 'your-random-token',
       },
       credentials: 'include',
       body: JSON.stringify({data: 'example'})
   });
   ```

### Detecting CSRF Vulnerabilities in JavaScript

For a SAST tool, the detection rules need to account for the following patterns:
- **Form submissions without CSRF tokens**.
- **AJAX requests not including CSRF tokens or custom headers**.
- **Framework-specific defaults not being overridden or properly set up**.

Examples of specific checks:
1. **Form Check**: Detect presence of forms that do not include CSRF tokens.
   ```json
   {
       "pattern": "<form[^>]*method=[\"']post[\"'][^>]*>",
       "message": "Forms submitting POST requests should include CSRF tokens."
   }
   ```

2. **AJAX Check**: Identify AJAX requests made without appropriate CSRF tokens in headers.
   ```json
   {
       "pattern": "xhr.open\\(\\s*'POST',[^,]*,\\s*true\\s*\\)[^;]*",
       "message": "AJAX POST requests should include CSRF tokens in headers."
   }
   ```

3. **Cookie Based CSRF Token Check**:
   ```json
   {
       "pattern": "\\.use\\(csrf\\(\\{\\s*cookie:\\s*true\\s*\\}\\)",
       "message": "Double submit cookies should be used for CSRF protection."
   }
   ```

By encompassing these checks into the SAST tool, detecting potential CSRF vulnerabilities in JavaScript applications becomes more systematic and comprehensive.

**References**:
- OWASP, "Cross-Site Request Forgery Prevention Cheat Sheet"【4:0†source】.
- OWASP, "Cross-Site Request Forgery (CSRF)"【4:0†source】.