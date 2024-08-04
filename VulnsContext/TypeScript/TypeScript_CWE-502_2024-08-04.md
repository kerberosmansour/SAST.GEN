# Deserialization of Untrusted Data (CWE-502) in TypeScript

###### Deserialization of Untrusted Data

Deserialization of untrusted data is a vulnerability that occurs when an application deserializes data from an unreliable source without sufficient checks. This can lead to arbitrary code execution, data tampering, or changes in application behavior by manipulating the serialized data structure【4:0†source】 .

### Explanation for Author of SAST Tool Detection Rules

#### Definition:
Deserialization of untrusted data takes place when attacker-controlled data is used to reconstitute objects from serialized forms. Attackers can craft serialized objects to exploit weaknesses in deserialization mechanisms, leading to severe consequences such as remote code execution.

#### Prevention:
- Avoid deserialization of data from untrusted sources whenever possible.
- Use digital signatures or similar mechanisms to verify the integrity of the serialized data before deserialization.
- Implement checks to confirm that deserialized data conforms to expected types and structures .

### TypeScript Examples and Frameworks

#### TypeScript with Node.js (Express)
In a Node.js environment using the Express framework, consider an example where JSON data might be deserialized without proper checks:

```typescript
import express from 'express';

const app = express();

app.use(express.json());

// Insecure deserialization example
app.post('/deserialize', (req, res) => {
    const data = JSON.parse(req.body.serializedData);
    // Further processing with the deserialized data
    console.log(data);
    res.send('Data deserialized');
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

Insecure deserialization occurs here if `req.body.serializedData` is an attacker-controlled input. The attacker could manipulate the `serializedData` to include harmful payloads.

#### TypeScript with Angular
Angular applications might inadvertently deserialize untrusted data during HTTP operations:

```typescript
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) { }

  getData(url: string) {
    this.http.get(url).subscribe((response: any) => {
      // Insecure deserialization example
      const data = JSON.parse(response.serializedData);
      console.log(data);
    });
  }
}
```

If the `serializedData` is not validated, `JSON.parse` could introduce vulnerabilities.

#### TypeScript with NestJS
NestJS, a popular TypeScript framework for building server-side applications, can also fall prey to deserialization vulnerabilities:

```typescript
import { Controller, Post, Body } from '@nestjs/common';

@Controller('deserialize')
export class DeserializationController {

  @Post()
  deserialize(@Body() body: { serializedData: string }) {
    // Insecure deserialization example
    const data = JSON.parse(body.serializedData);
    console.log(data);
    return 'Data deserialized';
  }
}
```

Similar to the previous examples, `JSON.parse` on uncontrolled input data can lead to security issues.

### Framework-Specific Checks in SAST Rules

1. **Identify deserialization methods**:
   - `JSON.parse()`
   - Libraries (e.g., `fast-json`, `class-transformer`)

2. **Verify input validation**:
   Ensure the input passed to the deserialization function is validated against a schema or expected type.

3. **Context-aware checks**:
   - For Angular (`HttpClient`), ensure responses are validated before parsing.
   - For NestJS, ensure `@Body` parameters are sanitized and validated.

4. **Best practices**:
   - Encourage usage of TypeScript interfaces and classes for type checking during deserialization to minimize risk.
   - Recommend secure coding standards, such as avoiding dynamic evaluation functions like `eval()` and reviewing application logging practices to identify and mitigate serialization issues promptly.

Developing SAST rules for detecting deserialization of untrusted data involves flagging instances where deserialization occurs without prior validation or authorization checks. By focusing on the deserialization methods, contexts in which they are used, and enforcing strict input validation, false positives and negatives can be minimized   .