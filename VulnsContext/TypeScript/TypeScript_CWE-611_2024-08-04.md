# Improper Restriction of XML External Entity Reference (CWE-611) in TypeScript

****Improper Restriction of XML External Entity Reference (XXE)**

### Overview
Improper Restriction of XML External Entity (XXE) Reference vulnerabilities arise when a system does not adequately restrict the XML parsers from handling external entity references. This can lead to various attacks, such as denial of service (DoS), Server-Side Request Forgery (SSRF), sensitive data exposure, and other system impacts【4:0†source】  .

### Definitions
1. **XML External Entity (XXE) Injection:** This occurs when an attacker crafts XML input containing a reference to an external entity. If processed by a vulnerable XML parser, it can enable the attacker to access or manipulate resources on the server.
2. **Denial of Service (DoS):** An attack to make a service unavailable by overwhelming the system.
3. **Server-Side Request Forgery (SSRF):** An attack in which the server makes unintended requests to internal resources or external third parties.

### Key Points
- **Disable DTDs and External Entities:** The safest way to prevent XXE attacks is to completely disable DTDs and external entities in the XML parser【4:0†source】.
- **Language-Specific Configurations:** Each programming language or XML parser might have a different way to disable DTDs and external entities.

### Examples of XXE in TypeScript
To detect XXE vulnerabilities in TypeScript across different frameworks, the SAST rules need to account for the different ways XML parsing can be implemented. Below are examples in popular TypeScript frameworks, illustrating potential XXE vulnerabilities:

#### 1. Node.js with xml2js Library
```typescript
import fs from 'fs';
import xml2js from 'xml2js';

const parser = new xml2js.Parser({
    explicitEntityParsing: true  // Vulnerable setting
});

fs.readFile('input.xml', (err, data) => {
    parser.parseString(data, (err, result) => {
        console.log(result);
    });
});
```

In the example above, the `explicitEntityParsing` option introduces a vulnerability if set to true. Secure configurations should ensure that all entity parsing is disabled.

#### 2. Node.js with fast-xml-parser Library
```typescript
import * as fastXmlParser from 'fast-xml-parser';

const parser = new fastXmlParser.XMLParser({
    ignoreAttributes: false, // This might not be safe
    allowBooleanAttributes: true
});

const xmlData = '<!ENTITY xxe SYSTEM "file:///etc/passwd" >';
const parsedData = parser.parse(xmlData);
console.log(parsedData);
```

The configuration should be audited to ensure entities and potentially malicious configurations are disabled.

#### 3. NestJS with xml2js
```typescript
import { Injectable } from '@nestjs/common';
import { parseString } from 'xml2js';

@Injectable()
export class XmlService {
  async parseXml(xml: string): Promise<any> {
    return new Promise((resolve, reject) => {
      parseString(xml, {
        explicitEntityParsing: true  // Vulnerable setting
      }, (err, result) => {
        if (err) {
          reject(err);
        } else {
          resolve(result);
        }
      });
    });
  }
}
```
Ensure the proper configurations are done to avoid XXE vulnerabilities.

#### 4. Express with libxmljs
```typescript
import express from 'express';
import fs from 'fs';
import libxmljs from 'libxmljs';

const app = express();

app.post('/upload', (req, res) => {
    fs.readFile(req.files.xmlfile.path, 'utf8', (err, data) => {
        const xmlDoc = libxmljs.parseXml(data, {
            noent: true  // Vulnerable setting
        });
        res.send(xmlDoc.toString());
    });
});

app.listen(3000, () => {
    console.log('Server started on port 3000');
});
```

Here, ensure that the setting `noent` is false to prevent XXE.

### Writing SAST Rules
For high-accuracy SAST rules:
1. **Identify XML parsing Libraries:** Focus on known libraries such as `xml2js`, `fast-xml-parser`, `libxmljs`, etc.
2. **Search for Vulnerable Configurations:** Look for configurations enabling DTDs or external entities (`noent`, `explicitEntityParsing`).
3. **Auditing Use of untrusted XML Data:** Verify that XML data comes from potentially untrusted sources.

### Conclusion
The key to writing effective SAST rules for detecting XXE vulnerabilities in TypeScript lies in:
1. **Static Analysis of XML Parser Configurations:** Ensuring all entry points and XML configurations are secure.
2. **Framework Awareness:** Understanding and accounting for how different frameworks (Express, NestJS, etc.) implement XML parsing.
3. **Contextual Understanding:** Flagging any setting that allows external entity references.

By focusing on these elements, SAST rules can achieve minimal false negatives and positives, thereby securing the application from XXE vulnerabilities efficiently.