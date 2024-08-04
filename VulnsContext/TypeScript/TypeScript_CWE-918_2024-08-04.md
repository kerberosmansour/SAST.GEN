# Server-Side Request Forgery (SSRF) (CWE-918) in TypeScript

###### Server-Side Request Forgery (SSRF) Overview

Server-Side Request Forgery (SSRF) is a security vulnerability where an attacker can make a server-side application send HTTP requests to an arbitrary domain of the attacker's choosing. This can lead to exploitation of the internal network, sensitive data exposure, and other severe exposures. SSRF typically arises from fetching a remote resource without validating the user-supplied URL properly. Attackers can craft requests that force the server to fetch and potentially act on unintended resources【4:0†source】【4:3†source】【4:6†source】.

### SSRF in TypeScript and Popular Frameworks

To ensure that your Static Application Security Testing (SAST) tool can detect SSRF in various TypeScript frameworks, it's essential to understand the common patterns and functionalities where SSRF can occur. Below are examples and explanation for different scenarios:

#### Node.js with Axios

Axios is a popular HTTP client for Node.js and browser. If user input is directly used in Axios requests without validation, it could lead to SSRF.

Example:
```typescript
import axios from 'axios';
import express from 'express';

const app = express();

app.get('/fetch', async (req, res) => {
    const url = req.query.url;
    try {
        const response = await axios.get(url);
        res.send(response.data);
    } catch (error) {
        res.status(500).send('Error fetching data');
    }
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

#### HTTP Client in Angular

Angular applications use HttpClient to make HTTP requests. Although Angular typically runs on the client-side, SSRF can still happen if the server API directly uses unvalidated URLs from client requests.

Example:
```typescript
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `<input #url /><button (click)="fetchData(url.value)">Fetch</button>`
})
export class AppComponent {
  constructor(private http: HttpClient) {}

  fetchData(url: string) {
    this.http.get(url).subscribe(data => {
      console.log(data);
    });
  }
}
```

#### NestJS Framework

NestJS, a progressive Node.js framework for building scalable server-side applications, can also fall victim to SSRF if user input isn't validated.

Example:
```typescript
import { Controller, Get, Query } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';

@Controller('fetch')
export class FetchController {
    constructor(private httpService: HttpService) {}

    @Get()
    async fetchData(@Query('url') url: string) {
        try {
            const response = await this.httpService.get(url).toPromise();
            return response.data;
        } catch (error) {
            throw new Error('Error fetching data');
        }
    }
}
```

### Writing SAST Rules for SSRF Detection

To detect SSRF vulnerabilities effectively with SAST, focus on the following elements:

1. **Identify Sources of User Input**:
   - Functions such as `req.query`, `req.body`, `axios.get`, `http.get`, etc., often serve as sources of user input.
   
2. **Identify HTTP Request Libraries/Components**:
   - Look for usage of HTTP client libraries such as `axios`, `node-fetch`, `HttpClient`, or `HttpService` in the case of NestJS.
   
3. **Trace Data Flow**:
   - Trace the data flow from the source of input to the HTTP request. Ensure that the URL is subject to validation or sanitization before it is used in any HTTP request.

4. **Detection Rules Example**:
   - Search for unvalidated input passing directly to HTTP request libraries.
   ```typescript
   function detectSSRF() {
       const userInputSources = ["req.query", "req.body", "context.req.query", "context.req.body"];
       const httpClients = ["axios.get", "http.get", "HttpClient.get", "HttpService.get"];

       userInputSources.forEach(source => {
           httpClients.forEach(client => {
               // Pseudo-code for SAST rule logic
               if (inputComesDirectlyFrom(source) && resultsInHttpClient(client)) {
                   return "Potential SSRF Vulnerability";
               }
           });
       });
   }
   ```

### Best Practices for Mitigation

1. **Input Validation**:
   - Use a whitelist approach, validating the input against known good URLs or domains.
   - Validate the structure of the URL and ensure it conforms to expected patterns.
   - Restrict protocols (allow only HTTP/HTTPS) and disallow redirects.

2. **Network Segmentation**:
   - Separate remote access functionality into different network segments to minimize the potential impact.

3. **Output Handling**:
   - Avoid reflecting raw server responses to the client.
   - Log all accepted requests and responses for monitoring and auditing.

In summary, detecting SSRF vulnerabilities involves identifying insecure data flows where user input is directly used in making HTTP requests. Your SAST rules should focus on tracing the path from input sources to HTTP client usages and ensuring adequate validation is performed. Implementing robust input validation and following best practices can significantly reduce the incidence of SSRF vulnerabilities【4:0†source】【4:1†source】【4:3†source】.