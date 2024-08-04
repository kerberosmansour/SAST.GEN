GivenGiven the context of Semgrep rules and taint tracking for identifying SQL Injection vulnerabilities in JavaScript, here's a Semgrep rule that uses taint mode and covers variations in popular JavaScript frameworks like Express.js and Sequelize.

```yaml
rules:
- id: sql-injection-js
  languages: [javascript]
  message: "Potential SQL Injection vulnerability detected"
  severity: ERROR
  mode: taint
  pattern-sources:
    - pattern: |
        function $FUNC(...) {
          ...
          req.body.$SOURCE = ...
          ...
        }
    - pattern: |
        router.$METHOD(..., (req, res) => {
          ...
          req.body.$SOURCE = ...
          ...
        })
  pattern-sinks:
    - pattern: |
        $QUERY.query(`... $SOURCE ...`)
    - pattern: |
        connection.execute(`... $SOURCE ...`)
  pattern-propagators:
    - pattern: |
        function $FUNC(...) {
          ...
          var $PROPAGATOR = $SOURCE;
          ...
        }
    - pattern: |
        router.$METHOD(..., (req, res) => {
          ...
          var $PROPAGATOR = req.body.$SOURCE;
          ...
        })
  pattern-sanitizers:
    - pattern: |
        sanitizer.escape($SOURCE)
    - pattern: |
        req.sanitize($SOURCE)
  metadata:
    cwe: "CWE-089"
    confidence: high
    impact: high
    likelihood: high
    subcategory: vuln
```

### Explanation:

1. **Sources:**
    - We are capturing input from HTTP requests, specifically `req.body` in Express.js applications.
    - The source patterns identify locations where data from `req.body` is assigned to variables within route handler functions.

2. **Sinks:**
    - We look for instances where these untrusted inputs are used directly in SQL queries.
    - Patterns for executing queries using different approaches: `connection.execute` and `.query` (common in Sequelize).

3. **Propagators:**
    - Identify where the tainted data propagates through different variables within the code.
    - Detect propagation within functions and route handlers.

4. **Sanitizers:**
    - Recognize code pieces where potential sanitization occurs, using libraries like sanitizer or similar middleware in Express.js.

5. **Metadata:**
    - Provides context about the vulnerability, including the CWE identifier, confidence, impact, and likelihood.

This rule helps in detecting SQL Injection vulnerabilities by tracking the flow of untrusted data (`req.body`) through the application and ensuring it is not used directly in SQL queries without proper sanitization.

If needed, rules can be updated or refined based on the context and specific usage patterns observed in the project's codebase. For further guidance and examples, you can refer to the documentation provided in the Semgrep files and the links therein   .