ToTo create Semgrep SAST rules targeting the "Allocation of Resources Without Limits or Throttling (CWE-770)" vulnerability in JavaScript and its variations, we need to follow the Semgrep SAST rule-writing techniques and apply common patterns for detecting resource allocation issues.

Here is how you can write Semgrep rules for this specific vulnerability:

### Example Semgrep Rule for CWE-770 in JavaScript

1. **Detecting Unrestricted Allocation in Loops**
```yaml
rules:
  - id: unrestricted-allocation-in-loop
    languages: [javascript]
    message: "Resource allocation without limits or throttling inside a loop can lead to DoS vulnerabilities."
    severity: WARNING
    patterns:
      - pattern: |
          for (...) {
            ...
            $RESOURCE = new $RESOURCE_TYPE(...);
            ...
          }
      - pattern: |
          while (...) {
            ...
            $RESOURCE = new $RESOURCE_TYPE(...);
            ...
          }
    metadata:
      cwe: "CWE-770"
      owasp: "A6: Security Misconfiguration"
```

2. **Detecting Unthrottled API Calls**
```yaml
rules:
  - id: unthrottled-api-calls
    languages: [javascript]
    message: "Unthrottled API calls can lead to denial of service."
    severity: WARNING
    pattern: |
      function $FUNC(...) {
        ...
        setInterval(() => {
          $API_CALL(...)
        }, $DELAY);
        ...
      }
    metadata:
      cwe: "CWE-770"
      owasp: "A6: Security Misconfiguration"
```

3. **Detecting Excessive Resource Creation in a Single Block**
```yaml
rules:
  - id: excessive-resource-creation
    languages: [javascript]
    message: "Excessive resource creation in a single block can lead to resource exhaustion."
    severity: WARNING
    pattern-either:
      - pattern: |
          for (...) {
            ...
            $RESOURCE1 = new $RESOURCE_TYPE1(...);
            $RESOURCE2 = new $RESOURCE_TYPE2(...);
            ...
          }
      - pattern: |
          while (...) {
            ...
            $RESOURCE1 = new $RESOURCE_TYPE1(...);
            $RESOURCE2 = new $RESOURCE_TYPE2(...);
            ...
          }
    metadata:
      cwe: "CWE-770"
      owasp: "A6: Security Misconfiguration"
```

### Key Concepts from Semgrep Rule Writing

1. **Metavariables and Metavariable Patterns**: Use metavariables to create flexible patterns that can generalize across different variable names and resource types.
2. **Pattern Matching**: Use constructs like `pattern`, `pattern-either`, `pattern-not` to specify the exact conditions under which the code should be flagged.
3. **Severity Levels**: Assign appropriate severity levels like `WARNING`, `ERROR` based on the vulnerability's impact.
4. **Metadata**: Include important metadata, such as CWE ID and OWASP category, to help with categorization and reporting.

These rules aim to capture various instances where resource allocation without limits can be harmful, including loops and interval-based operations often used in JavaScript.

### References
The above examples are structured based on the techniques described within the provided Semgrep documentation, such as using metavariable patterns and the ellipsis operator to handle complex and nested code patterns effectively   . The message, severity, and patterns are all aligned with the guidelines from the Semgrep pattern syntax examples and rules used for detecting insecure coding practices.