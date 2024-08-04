ToTo create Semgrep SAST rules for "Improper Certificate Validation (CWE-295) in JavaScript," let's utilize the information extracted from `Semgrep.output.md` on how to write and structure Semgrep rules. We'll cover several variations where this vulnerability could occur in popular frameworks.

### Sample Semgrep SAST Rule for JavaScript

This rule will detect instances where HTTPS requests are made without proper certificate validation, focusing on cases where libraries like `axios`, `request`, and `fetch` might omit validation.

```yaml
rules:
  - id: improper-certificate-validation-axios
    patterns:
      - pattern: |
          axios.get(..., { httpsAgent: new https.Agent({ rejectUnauthorized: false })})
      - pattern: |
          axios.post(..., { httpsAgent: new https.Agent({ rejectUnauthorized: false })})
      - pattern: |
          axios.request({ httpsAgent: new https.Agent({ rejectUnauthorized: false }), ...})
    message: "HTTPS request made without proper certificate validation using axios"
    languages: [javascript]
    severity: ERROR

  - id: improper-certificate-validation-request
    patterns:
      - pattern: |
          request(...) // Inside options object:
            { rejectUnauthorized: false, ... }
    message: "HTTPS request made without proper certificate validation using the request library"
    languages: [javascript]
    severity: ERROR

  - id: improper-certificate-validation-fetch
    patterns:
      - pattern: |
          fetch(..., { agent: new https.Agent({ rejectUnauthorized: false })})
    message: "HTTPS request made without proper certificate validation using fetch"
    languages: [javascript]
    severity: ERROR

  - id: improper-certificate-validation-node-https
    patterns:
      - pattern: |
          https.get(..., { rejectUnauthorized: false })
      - pattern: |
          https.request(..., { rejectUnauthorized: false })
    message: "HTTPS request made without proper certificate validation using Node.js https module"
    languages: [javascript]
    severity: ERROR
```

### Explanation
1. **Patterns**:
   - **`axios.get`**, **`axios.post`**, and **`axios.request`**:
     - These configurations detect the `httpsAgent` property configured with `rejectUnauthorized: false`, which disables certificate validation.
   - **`request`**:
     - Detects when the `request` library is used with the `rejectUnauthorized: false` property inside the options object.
   - **`fetch`**:
     - Detects the `fetch` API when used with an agent that disables certificate validation via `rejectUnauthorized: false`.
   - **`https.get`** and **`https.request`**:
     - Identifies the use of Node.js `https` module configured without certificate validation.

2. **Messages**: Each pattern is accompanied by an informative message indicating the detected issue.

3. **Languages**: These rules are specified for JavaScript.

4. **Severity**: Set to `ERROR` to indicate a critical issue that needs fixing.

### Further Customization
You can extend these rules to cover more specific cases or additional patterns by adding more `patterns` to each rule block.

This example leverages understanding of JavaScript’s common HTTP libraries and how improper certificate validation might be configured. The customization options provided by Semgrep make it an effective tool for ensuring code security【4:1†source】  .