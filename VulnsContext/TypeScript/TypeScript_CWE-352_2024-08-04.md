# Cross-Site Request Forgery (CSRF) (CWE-352) in TypeScript

###### Cross-Site Request Forgery (CSRF) Overview

A Cross-Site Request Forgery (CSRF) attack occurs when a malicious site tricks a user's browser into making unwanted actions on another site where the user is authenticated. The attack leverages the fact that browsers automatically include credentials (like cookies, session tokens) in requests. Essentially, a CSRF attack compels a user to execute actions that they did not intend, often without their knowledge【4:0†source】.

### CSRF Mitigation Techniques

1. **Token-Based Mitigations**:
   - **Synchronizer Token Pattern**: Embed a unique, unpredictable token in each request. This token is then validated server-side.
   - **Double Submit Cookies**: Include a CSRF token in a cookie and a matching CSRF token in the request (header or body), verifying that they match server-side【4:0†source】【4:1†source】【4:2†source】.
2. **Custom Request Headers**: Ensure that any state-changing requests have a custom header that normal browsers do not send cross-domain by default.
3. **SameSite Cookie Attribute**: Configure cookies to be sent only in first-party contexts, mitigating the risk of CSRF from third-party sites.

### CSRF in TypeScript: Examples in Various Frameworks

#### 1. **Angular**
Angular has built-in support for CSRF protection via `HttpClient`:

```typescript
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {
  constructor(private http: HttpClient) {}

  makeRequest() {
    this.http.post('/api/change-password', { newPassword: 'new_password' }).subscribe(response => {
      console.log('Password changed');
    });
  }
}
```

Here, Angular automatically sends the CSRF token as a custom header `X-XSRF-TOKEN` which is protected against CSRF attacks, provided that the server checks for this header.

#### 2. **React with Axios**
React does not include built-in CSRF protection, but it can be manually implemented with libraries like Axios:

```typescript
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken'; // Default cookie name to look for the token
axios.defaults.xsrfHeaderName = 'X-CSRFToken'; // Default header name to send the token

function changePassword(newPassword: string) {
  axios.post('/api/change-password', { newPassword })
    .then(response => {
      console.log('Password changed');
    })
    .catch(error => {
      console.error('There was an error!', error);
    });
}
```

Ensure that the server sends a `csrftoken` cookie, and Axios will automatically include it in subsequent requests.

#### 3. **Vue.js with Axios**
Similar to React, CSRF tokens need to be manually configured:

```typescript
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
  name: 'App',
  methods: {
    changePassword(newPassword) {
      axios.post('/api/change-password', { newPassword })
        .then(response => {
          console.log('Password changed');
        })
        .catch(error => {
          console.error('There was an error!', error);
        });
    }
  }
}
```

#### 4. **Express.js (Server-Side)**
For server-side frameworks such as Express, middleware like `csurf` can be used:

```typescript
import express from 'express';
import csurf from 'csurf';

const app = express();
const csrfProtection = csurf({ cookie: true });

app.use(express.json()); // For parsing application/json
app.use(csrfProtection);

app.get('/form', (req, res) => {
  res.send(`<form action="/process" method="POST">
              <input type="hidden" name="_csrf" value="${req.csrfToken()}">
              <button type="submit">Submit</button>
            </form>`);
});

app.post('/process', (req, res) => {
  res.send('Data is being processed');
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```

### Writing SAST Rules for CSRF Detection

#### Key Patterns to Detect:
1. **Absence of CSRF Tokens in State-Altering Requests**: Identify methods such as `POST`, `PUT`, or `DELETE` where no CSRF token validation is present.
2. **Custom Headers Presence**: Ensure the presence of custom headers (e.g., `X-CSRFToken`) in state-altering requests.
3. **Usage of GET Requests for State Changes**: Warn if state changes are made using `GET` requests.

#### Example SAST Rule Logic:
- **Angular/HttpClient**:
  - Check for HttpClient `POST`, `PUT`, `DELETE` operations.
  - Verify that `HttpClientModule` is imported and used with CSRF token configurations.

- **React/Vue/Axios**:
  - Check that `axios.defaults.xsrfCookieName` and `axios.defaults.xsrfHeaderName` are set.
  - Verify that Axios post requests include headers for CSRF tokens.

- **Express.js**:
  - Detect usage of state-modifying endpoints.
  - Ensure middleware like `csurf` is applied globally or on sensitive routes.

By identifying these patterns and ensuring the presence of required mitigation strategies, false negatives can be minimized while keeping false positives to a minimum【4:0†source】【4:1†source】【4:2†source】【4:3†source】.