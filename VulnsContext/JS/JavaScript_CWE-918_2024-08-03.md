# Server-Side Request Forgery (SSRF) (CWE-918) in JavaScript

###### Explanation of Server-Side Request Forgery (SSRF)

#### What is SSRF?

Server-Side Request Forgery (SSRF) is a vulnerability that occurs when a web application fetches a remote resource without validating the user-supplied URL. This flaw allows an attacker to coerce the application into sending crafted requests to unintended or even protected locations (e.g., internal services, local files, etc.)【4:0†source】.

#### Variations of SSRF in JavaScript

To help create rules for detecting SSRF in SAST (Static Application Security Testing) tools, let's look at common scenarios in JavaScript, especially in popular frameworks:

1. **Basic Fetching with `fetch` API:**
    ```javascript
    const fetch = require('node-fetch');

    function fetchData(userURL) {
        return fetch(userURL)
            .then(response => response.json())
            .catch(error => console.error('Error:', error));
    }
    ```
   **Description**: If `userURL` is not validated, an attacker might provide a malicious URL, leading to SSRF.

2. **Using Axios Library:**
    ```javascript
    const axios = require('axios');

    function fetchData(userURL) {
        axios.get(userURL)
            .then(response => console.log(response.data))
            .catch(error => console.error('Error:', error));
    }
    ```
   **Description**: Similar to `fetch`, an unvalidated `userURL` can cause SSRF.

3. **HTTP Module in Node.js:**
    ```javascript
    const http = require('http');

    function fetchData(userURL) {
        http.get(userURL, (resp) => {
            let data = '';
            resp.on('data', (chunk) => { data += chunk; });
            resp.on('end', () => { console.log(data); });
        }).on("error", (err) => {
            console.log("Error: " + err.message);
        });
    }
    ```
   **Description**: Default HTTP module, vulnerable if `userURL` is not sanitized.

4. **Express.js Application:**
    ```javascript
    const express = require('express');
    const axios = require('axios');
    const app = express();

    app.get('/fetch', (req, res) => {
        const userURL = req.query.url;
        axios.get(userURL)
            .then(response => res.send(response.data))
            .catch(error => res.status(500).send('Error occurred'));
    });

    app.listen(3000);
    ```
   **Description**: Express route using Axios to fetch user-supplied URL, potential SSRF if the input URL is not validated.

#### Preventive Measures

1. **Input Validation:**
   Implement robust input validation to ensure URLs conform to expected patterns (e.g., allow specific domains, protocols)【4:0†source】.

    ```javascript
    function validateURL(url) {
        const allowedDomains = ['example.com', 'api.example.com'];
        try {
            const parsedURL = new URL(url);
            if (!allowedDomains.includes(parsedURL.hostname)) {
                throw new Error('Invalid domain');
            }
        } catch (e) {
            console.error('Invalid URL:', e.message);
            return false;
        }
        return true;
    }
    ```

2. **Restrict Network Access:**
   Use "deny by default" policies and segment networks to control outgoing requests.

3. **Avoid Direct URL Usage:**
   Instead of using user-supplied URLs directly, use identifiers that map to specific URLs defined server-side.

4. **Disable Unnecessary Features:**
   Disable HTTP redirections and avoid sending raw responses to clients【4:15†source】【4:16†source】.

#### Conclusion

For SAST detection rules, focus on identifying unsanitized user inputs passed to HTTP request functions or libraries such as `fetch`, `axios`, and Node’s `http` module. Include checks for validation logic and known preventive measures. By integrating these detection mechanisms, you can significantly reduce the risk of SSRF vulnerabilities in JavaScript applications.