# Improper Certificate Validation (CWE-295) in TypeScript

###### Improper Certificate Validation

**Improper Certificate Validation (CWE-295)** is a vulnerability that occurs when an application does not properly validate a certificate during an SSL/TLS connection. This can lead to various types of security weaknesses, enabling attackers to intercept or modify data in transit, impersonate other servers, or trigger other forms of man-in-the-middle attacks.

### Variations in TypeScript for Different Frameworks

Improper Certificate Validation can take multiple forms in TypeScript, especially when using various popular frameworks. Below, we will provide examples and potential detection rules for a SAST tool to identify these vulnerabilities. The goal is to create rules with low false positives and negatives.

#### 1. Using Node.js (Native HTTPS Module)

**Problematic Code Example:**
```typescript
const https = require('https');

const options = {
  hostname: 'example.com',
  port: 443,
  path: '/',
  method: 'GET',
  rejectUnauthorized: false // Disables certificate validation
};

https.request(options, (res) => {
  // handle response
}).end();
```

**Detection Rule:**
- Identify configurations where `rejectUnauthorized` is set to `false`.

#### 2. Axios

**Problematic Code Example:**
```typescript
const axios = require('axios');

axios.get('https://example.com', {
  httpsAgent: new (require('https').Agent)({ rejectUnauthorized: false })
}).then(response => {
  // handle response
});
```

**Detection Rule:**
- Check for `httpsAgent` configurations within Axios requests where `rejectUnauthorized` is `false`.

#### 3. Fetch with Custom Agent

**Problematic Code Example:**
```typescript
const fetch = require('node-fetch');
const https = require('https');

const agent = new https.Agent({
  rejectUnauthorized: false // Disables certificate validation
});

fetch('https://example.com', { agent })
  .then(res => res.json())
  .then(json => {
    // handle JSON
  });
```

**Detection Rule:**
- Look for instances where a custom agent is used with `fetch` where `rejectUnauthorized` is `false`.

#### 4. Angular HTTP Client

**Problematic Code Example:**
For Angular, the scenario is less about direct manipulation of certificate validation since such configuration is abstracted away. However, Angular applications might configure services to allow insecure endpoints or misuse of third-party libraries that disable certificate validation.

```typescript
import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get('http://example.com/insecure-endpoint')
      .subscribe(response => {
        // handle response
      });
  }
}
```

**Detection Rule:**
- Ensure URLs in HTTP requests use `https`. A rule might flag `http://`.

#### 5. React Native using `fetch`

**Problematic Code Example:**
```typescript
fetch('https://example.com', {
  // some custom configuration
})
  .then(response => response.json())
  .then(json => {
    console.log(json);
  });

// Potential custom agent configuration manipulation
import {NativeModules} from 'react-native';
const {HttpsAgent} = NativeModules;

const agent = new HttpsAgent({
  rejectUnauthorized: false
});

fetch('https://example.com', {agent})
  .then(response => response.json())
  .then(json => {
    console.log(json);
  });
```

**Detection Rule:**
- Similar to Node.js `fetch`, identify fetch calls with custom agents where `rejectUnauthorized` is `false`.

### Crafting SAST Rules

A SAST tool should scan the TypeScript code to spot these common patterns:
- **Literal Analysis**: Look for boolean values like `rejectUnauthorized: false`.
- **Configuration Analysis**: Detect configurations within objects passed to HTTPS/TLS requests.
- **URL Analysis**: Ensure usage of HTTPS rather than HTTP in the URL strings across frameworks.
- **Custom Agent Detection**: Identify instantiation of custom agents and inspect their configurations.

### Preventive Measures
To mitigate Improper Certificate Validation:
- Always ensure that certificate validation is enabled.
- Avoid setting `rejectUnauthorized` to `false` unless absolutely necessary and understand the security implications.
- Use trusted sources for certificates and properly validate those certificates within the application code.

### References
The listed variations and examples are based on understanding security standards laid out by OWASP and similar organizations【4:0†source】  .