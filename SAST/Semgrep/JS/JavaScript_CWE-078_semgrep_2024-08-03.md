ToTo develop a set of Semgrep SAST rules for detecting "Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') (CWE-078)" vulnerabilities and their variations in JavaScript, we can rely on custom rule creation principles laid out in the document you provided. Here's a framework:

### Information from the Document
1. **Writing Custom Rules**:
    - Semgrep uses YAML syntax for writing custom rules.
    - Basic rule structure includes ID, language, message, severity, and patterns【4:1†source】.
    - It is essential to familiarize with Semgrep's pattern syntax and use tools like the [Semgrep Playground](https://semgrep.dev/playground) for testing【4:2†source】 .

2. **Optimization Tips**:
    - Use `pattern-inside` and `pattern-not-inside` clauses effectively.
    - Minimize the use of ellipses (`...`) to avoid performance issues and false positives  .

3. **Sample Code and Experimentation**:
    - Utilize pre-built idioms from the Semgrep documentation on common frameworks like Express for more accurate pattern matching【4:5†source】 .

### Semgrep Rule for OS Command Injection
Here’s a comprehensive rule set for detecting OS Command Injection vulnerabilities in JavaScript:

```yaml
rules:
- id: os-command-injection
  languages: [javascript]
  message: "Potential OS Command Injection detected"
  severity: ERROR
  pattern-either:
    - pattern: exec($INJ)
    - pattern: execSync($INJ)
    - pattern: require('child_process').exec($INJ)
    - pattern: require('child_process').execSync($INJ)
  metavariables:
    INJ: $INJ
  patterns:
    - pattern-inside: |
        function (...) {
          ...
          $INJ
          ...
        }
  metadata:
    cwe: "CWE-078"
    references:
      - "https://cwe.mitre.org/data/definitions/78.html"
    
- id: unsafe-spawn
  languages: [javascript]
  message: "Use of child_process.spawn or child_process.spawnSync with unvalidated input"
  severity: ERROR
  pattern-either:
    - pattern: |
        spawn($CMD, $ARGS, ...)
    - pattern: |
        spawnSync($CMD, $ARGS, ...)
  metadata:
    cwe: "CWE-078"
    references:
      - "https://cwe.mitre.org/data/definitions/78.html"
  metavariables:
    CMD: $CMD
- id: shelljs-exec-vuln
  languages: [javascript]
  message: "shelljs exec() method with unvalidated input"
  severity: ERROR
  pattern: |
    require('shelljs').exec($CMD)
  metadata:
    cwe: "CWE-078"
    references:
      - "https://cwe.mitre.org/data/definitions/78.html"
```

### Explanation:
1. Addressing the `exec` and `execSync` methods from `child_process` as these are common injection points.
2. The `pattern-inside` clause to ensure the command injection patterns are checked within function scopes.
3. Added `spawn` and `spawnSync` patterns and addressing third-party modules like `shelljs` which provide similar functionalities.

By following optimized practices from the provided documentation and utilizing the Semgrep testing tools, these rules can help significantly in identifying and preventing OS Command Injection vulnerabilities in JavaScript projects. You can always adjust the rules and test real-world scenarios to ensure thorough validation  .