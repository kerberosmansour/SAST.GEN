Based on the provided context from the Semgrep document, we can now generate Semgrep SAST rules for detecting SSRF vulnerabilities (CWE-918) in JavaScript code. Here are the examples and explanation steps for crafting effective Semgrep rules tailored to various SSRF scenarios in popular JavaScript frameworks.

### Example Semgrep Rules for SSRF in JavaScript

#### 1. Basic SSRF Detection in Node.js using `http` library

```yaml
rules:
  - id: ssrf-http-request
    patterns:
      - pattern: |
          http.get($URL, ...)
      - pattern-not: |
          // safeURLPattern is a regex or logic that matches only safe URLs
          var safeURLPattern = ...
          if(safeURLPattern.test($URL)) { ... }
    message: |
      Possible Server-Side Request Forgery (SSRF) via 'http.get'
    severity: ERROR
    languages: [javascript]
    metadata:
      cwe: 918
```

#### 2. SSRF Detection in Express Applications via User Input

```yaml
rules:
  - id: ssrf-express-user-input
    patterns:
      - pattern: |
          app.get($ROUTE, (req, res) => {
            http.get(req.query.url, ...)
          })
      - pattern-not: |
          // safeURLPattern is a regex or logic that matches only safe URLs
          var safeURLPattern = ...
          if(safeURLPattern.test(req.query.url)) {
            http.get(req.query.url, ...)
          }
    message: |
      Potential SSRF vulnerability using user input in Express application
    severity: ERROR
    languages: [javascript]
    metadata:
      cwe: 918
```

#### 3. SSRF Detection in Common HTTP Libraries like `axios`

```yaml
rules:
  - id: ssrf-axios-request
    patterns:
      - pattern: |
          axios.get($URL, ...)
      - pattern-not: |
          // safeURLPattern is a regex or logic that matches only safe URLs
          var safeURLPattern = ...
          if(safeURLPattern.test($URL)) {
            axios.get($URL, ...)
          }
    message: |
      Possible SSRF vulnerability via 'axios.get'
    severity: ERROR
    languages: [javascript]
    metadata:
      cwe: 918
```

#### 4. SSRF Detection in Fetch API Usage

```yaml
rules:
  - id: ssrf-fetch-request
    patterns:
      - pattern: |
          fetch($URL, ...)
      - pattern-not: |
          const safeURLPattern = ...
          if(safeURLPattern.test($URL)) {
            fetch($URL, ...)
          }
    message: |
      Possible Server-Side Request Forgery (SSRF) via 'fetch'
    severity: ERROR
    languages: [javascript]
    metadata:
      cwe: 918
```

### Explanation and Key Points for Writing Semgrep Rules

1. **Patterns and Pattern-not**:
   - **Pattern**: Defines the code pattern to be detected.
   - **Pattern-not**: Uses conditions to exclude safe patterns. For example, it ensures that URLs are validated against a safe URL pattern before making requests.

2. **Metavariables**: 
   - Used as placeholders (e.g., `$URL`) to match variable portions in the code.
   - Meta patterns enable flexibility and more realistic code matching.

3. **Severity and Metadata**:
   - **Severity**: Defines the level of the issue (e.g., ERROR, WARNING).
   - **Metadata**: Additional info like CWE IDs (e.g., `cwe: 918` for SSRF).

4. **Framework-Specific Adjustments**:
   - Customize patterns for different libraries (e.g., `http`, `axios`, `fetch`).
   - Patterns tailored to common practices in frameworks like Express.

By leveraging these patterns, developers can use Semgrep for effective detection of potential SSRF vulnerabilities in their JavaScript projects. Adapting these rules ensures they cover different routes and methods used in popular frameworks and coding patterns.

For further reading, you can refer to the detailed documentation and examples in the Semgrep repository and tutorial pages  .