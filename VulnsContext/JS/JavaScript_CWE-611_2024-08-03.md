# Improper Restriction of XML External Entity Reference (CWE-611) in JavaScript

###### Explanation of Improper Restriction of XML External Entity Reference

#### What is XXE?
An **XML eXternal Entity (XXE)** attack is a type of attack against an application that parses XML input. This vulnerability occurs when XML input containing a reference to an external entity is processed by a weakly configured XML parser. If exploited, it can lead to severe consequences, including:

- **Denial of Service (DoS)**
- **Server-Side Request Forgery (SSRF)**
- **Port Scanning**
- **Exfiltration of Data**   

#### Prevention Methods
The safest way to prevent XXE attacks is to disable Document Type Definitions (DTDs) and external entities. This can be achieved by configuring the XML parser to disallow DTDs and external entities entirely. If disabling DTDs completely isn't possible, external entities and external document type declarations must be disabled individually for each parser.

## XXE in JavaScript Contexts

### Variations of XXE in JavaScript

#### 1. Traditional JavaScript XML Parsers
XML parsers in JavaScript, such as `DOMParser`, `XMLHttpRequest`, and `jQuery.ajax`, can be susceptible to XXE attacks if improperly configured.

**Example: Using DOMParser without Proper Configuration**

```javascript
function parseXML(xmlString) {
    var parser = new DOMParser();
    var xmlDoc = parser.parseFromString(xmlString, "application/xml");
    // Process xmlDoc
}
```

If `xmlString` contains malicious XML with an external entity, the parser might process it, leading to an XXE vulnerability.

**Mitigation: Sanitizing Input and Validating**

```javascript
function parseXMLSafer(xmlString) {
    if (!isValidXML(xmlString)) {
       throw new Error("Invalid XML input");
    }

    var parser = new DOMParser();
    var xmlDoc = parser.parseFromString(xmlString, "application/xml");
    // Process xmlDoc
}

function isValidXML(xml) {
  // Implement XML validation logic here (e.g., using an XML schema)
}
```

#### 2. Server-side JavaScript (Node.js) with XML Parsers
Node.js can use various XML parsing libraries, such as `xml2js` or `xmldom`, which can also be at risk without proper configuration.

**Example: Parsing XML with `xml2js`**

```javascript
const xml2js = require('xml2js');

function parseXML(xmlString) {
    xml2js.parseString(xmlString, (err, result) => {
        if (err) {
            throw new Error('Failed to parse XML');
        }
        
        // Process result
    });
}
```

**Mitigation: Disabling External Entities**

As of today, some parsers have built-in features to disable DTD parsing. In `xml2js`, there's no direct method to disable DTD or external entities, so you must sanitize input before feeding it into the parser.

#### 3. Framework-Specific Examples

**Example for Angular**

Angular often handles XML via HTTP requests that might need parsing. Here’s how a risky approach looks:

```typescript
import { HttpClient } from '@angular/common/http';

class MyComponent {
  constructor(private http: HttpClient) {}

  getXMLData(url: string) {
    this.http.get(url, { responseType: 'text' }).subscribe(data => {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, 'application/xml');
      // Process xmlDoc
    });
  }
}
```

**Mitigation: Sanitizing Input**

Always validate and sanitize data from untrusted sources before parsing. Instead of directly using an insecure parser, implement validation:

```typescript
import { HttpClient } from '@angular/common/http';

class MyComponent {
  constructor(private http: HttpClient) {}

  // Suppose we have a validator function that guarantees the XML does not contain unwanted DTDs or entities
  validateXMLString(xmlString: string): boolean {
    // Implement your validation logic
    return true;
  }

  getXMLData(url: string) {
    this.http.get(url, { responseType: 'text' }).subscribe(data => {
      if (this.validateXMLString(data)) {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(data, 'application/xml');
        // Process xmlDoc
      } else {
        console.error('Invalid XML');
      }
    });
  }
}
```

### Writing SAST Rules for XXE Detection

To detect XXE vulnerabilities, SAST rules should include the following checks:

1. **Detection of XML Parsing Libraries and Functions**:
   - Identify the usage of `DOMParser`, `XMLHttpRequest`, `xml2js`, and other XML parsers in JavaScript and Node.js.
   - Flag instances where input XML is parsed without any validations or configurations to disable DTDs and external entity parsing.

2. **Detect Hardcoded or Unvalidated External Content**:
   - Flag instances where XML content from untrusted sources is being parsed directly.

3. **Check for Disabling External Entities and DTDs**:
   - Confirm that `DOMParser` is not being used in a way that processes potentially harmful DTDs.
   - For libraries like `xml2js`, ensure that input XML is validated and sanitized before parsing.

4. **Framework-Specific Rules**:
   - In Angular, flag XML parsing in HTTP methods without validation or sanitization of responses.
   - In Node.js, check XML parsing-related imports and method calls to ensure best practices are enforced.

With these guidelines, the SAST rules can effectively identify and prevent XXE vulnerabilities across different JavaScript environments and frameworks.

For detailed prevention techniques across various languages and XML parsers, refer to the [XML External Entity Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html) .