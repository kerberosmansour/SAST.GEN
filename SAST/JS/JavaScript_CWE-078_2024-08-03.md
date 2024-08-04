Here'sHere's a Semgrep SAST rule for detecting Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') (CWE-078) in JavaScript:

```yaml
rules:
- id: os-command-injection
  patterns:
    - pattern: |
        const { exec } = require('child_process');
        exec($CMD, ($ERROR, $STDOUT, $STDERR) => {
          ...
        });
    - pattern: |
        const { execSync } = require('child_process');
        execSync($CMD);
    - pattern: |
        import { exec } from 'child_process';
        exec($CMD, ($ERROR, $STDOUT, $STDERR) => {
          ...
        });
    - pattern: |
        import { execSync } from 'child_process';
        execSync($CMD);
  message: "Possible OS command injection in $CMD"
  severity: ERROR
  languages:
    - javascript
  metadata:
    cwe: "CWE-078"
    confidence: "high"
    impact: "high"
    likelihood: "high"
    subcategory: "vuln"
```

This rule covers various uses of the `exec` and `execSync` methods in JavaScript's `child_process` module, which are prone to OS command injection attacks if they execute commands containing user-controlled input without proper sanitization.

### Explanation:
1. **`patterns`:** 
    - Multiple pattern clauses to match different variations and import styles of `exec` and `execSync`.
    - The pattern looks for `exec` and `execSync` usage with variable commands that are potentially user-controlled.
2. **`languages`:** Indicates the rule is for JavaScript.
3. **`message`:** The error message displayed when a match is found.
4. **`metadata`:** Provides additional context about the CWE identifier, confidence, impact, and likelihood to help developers understand the severity of the detected issue and prioritize fixing it.

### Metadata Fields:
Adding metadata fields like CWE, confidence, impact, and likelihood is a good practice to give more context and help developers prioritize fixes【4:2†source】 .

### Additional Context:
Ensure that your Semgrep rule uses proper metadata to help developers understand the implications of the detected issue  .

If you have any specific applications or frameworks you want the rule to cover (e.g., Express.js, Koa, etc.), additional patterns can be added accordingly to detect framework-specific command execution points.