# Cleartext Transmission of Sensitive Information (CWE-319) in TypeScript

###### Understanding Cleartext Transmission of Sensitive Information
"Cleartext Transmission of Sensitive Information" describes scenarios where sensitive data is transmitted over a network in a format that is not encrypted, making it readable to anyone who intercepts the transmission. This is often a result of using unencrypted protocols or failing to properly implement encryption mechanisms. Some common protocols that can be problematic when used in cleartext are HTTP, SMTP, FTP, and outdated versions of TLS【4:0†source】【4:2†source】【4:4†source】.

#### Consequences
- **Eavesdropping:** Malicious actors can capture and read the transmitted data.
- **Data Theft:** Sensitive information like passwords, credit card numbers, or personal identifiers can be stolen.
- **Man-in-the-Middle Attacks:** Attackers can intercept and alter the data being transmitted between two parties.

### Cleartext Transmission in TypeScript Applications
In TypeScript applications, cleartext transmission can occur in various ways, especially when using popular frameworks like Node.js with Express, Angular, React, and Next.js. Here are some practical examples and patterns that you can use to develop SAST (Static Application Security Testing) rules for detecting such vulnerabilities.

#### 1. Direct HTTP Requests
Using plaintext HTTP requests instead of HTTPS is the most straightforward example:
```typescript
// Bad Practice: Making an HTTP request with sensitive data
fetch('http://example.com/api', {
  method: 'POST',
  body: JSON.stringify({ password: 'supersecret' }),
  headers: { 'Content-Type': 'application/json' }
});
```

#### 2. Angular HTTP Client
In Angular, the `HttpClient` can also be misused to transmit sensitive information without encryption:
```typescript
// Bad Practice: Angular service making an HTTP request
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable()
export class ApiService {
  constructor(private http: HttpClient) {}

  sendSensitiveData(data: any) {
    return this.http.post('http://example.com/api', data);
  }
}
```

#### 3. Axios in React or Node.js
The Axios library is commonly used for making HTTP requests. It's easy to misuse:
```typescript
// Bad Practice: Using Axios in React or Node.js to transmit data over HTTP
import axios from 'axios';

axios.post('http://example.com/api', { password: 'supersecret' })
  .then(response => console.log(response));
```

#### 4. Express.js Server
An Express server transmitting sensitive data over HTTP instead of HTTPS:
```typescript
// Bad Practice: Express server returning sensitive data over HTTP
import * as express from 'express';
const app = express();

app.post('/api', (req, res) => {
  res.send('Sensitive Information');
});

app.listen(80, () => {
  console.log('Server is running on http://localhost:80');
});
```

#### 5. WebSocket Communication
WebSockets should use the `wss` protocol rather than `ws` to ensure encryption:
```typescript
// Bad Practice: WebSocket connection without using secure WebSocket (wss)
const socket = new WebSocket('ws://example.com/socket');

socket.onopen = () => {
  socket.send('Sensitive Data');
};
```

### How to Write a SAST Rule
For writing effective SAST rules to detect Cleartext Transmission of Sensitive Information in TypeScript, here are the specific patterns and practices to look for:

1. **Detect Plaintext Protocols:**
   - Identify `http`, `ws` usage in URL strings of network requests.
   - Check common libraries for network communication like `fetch`, `axios`, `HttpClient`.

2. **API Configuration:**
   - Inspect server configuration files (e.g., Express.js) for HTTP setup instead of HTTPS.
   - Identify WebSocket initializations ensuring they're not using the secure protocol.

### Example Patterns for SAST Rules:
1. **Plaintext HTTP Requests:**
   ```regex
   (fetch|axios\.get|axios\.post|this\.http\.post|this\.http\.get)\('http:\/\/[^\']*'
   ```

2. **Express HTTP Configuration:**
   ```regex
   app\.listen\((80|httpPortVariable),\s*.*\)
   ```

3. **Plaintext WebSocket:**
   ```regex
   new\s+WebSocket\('ws:\/\/[^\']*'
   ```

### Conclusion
Detecting cleartext transmissions involves identifying instances where data is being sent over unencrypted channels. By focusing on common libraries and network communication patterns in popular TypeScript frameworks, such as Angular and React, we can construct SAST rules that identify these vulnerabilities with high accuracy. Ensure that the rules are continually refined and tested against diverse codebases to maintain their effectiveness【4:0†source】【4:1†source】【4:4†source】.