BasedBased on the details from the given Semgrep rules and examples, here's a Semgrep SAST rule for detecting Improper Neutralization of Special Elements used in a Command ('Command Injection') (CWE-077) in JavaScript, including coverage for variations in popular frameworks:

```yaml
rules:
  - id: js-command-injection
    patterns:
      - pattern-either:
          - pattern: exec($CMD)
          - pattern: execSync($CMD)
          - pattern: spawn($CMD, $ARGS, ...)
          - pattern: spawnSync($CMD, $ARGS, ...)
          - pattern: system($CMD)
          - pattern: `$LIB.execFile($CMD, ...`
      - pattern-not-inside: |
          function safeFunction(...)
          {
            try {
              $CMD = ...; 
              if ($CMD.startsWith("safeCommand")) {
                return $CMD;
              }
            } catch (err) {
              // handle error
            }
          }
    message: Potential Command Injection detected with '$CMD'
    languages:
      - javascript
    severity: ERROR
    metadata:
      cwe: "CWE-077"
      confidence: "high"
      likelihood: "high"
      impact: "high"
      subcategory: "vuln"
    examples:
      - code: |
          const { exec, execSync } = require('child_process');
          exec(userInput); // ruleid: js-command-injection
          execSync(userInput); // ruleid: js-command-injection

          const { spawn, spawnSync } = require('child_process');
          spawn(userInput, ['arg1']); // ruleid: js-command-injection
          spawnSync(userInput, ['arg1']); // ruleid: js-command-injection

          const system = require('system');
          system(userInput); // ruleid: js-command-injection

          someLib.execFile(userInput); // ruleid: js-command-injection
      - code: |
          // ok: js-command-injection
          function safeFunction(cmd) {
            try {
              if (cmd.startsWith("safeCommand")) {
                require('child_process').exec(cmd);
              }
            } catch (err) {
              // handle error
            }
          }
          safeFunction(userInput);
```

### Details:

1. **Patterns**:
   - The rule uses `pattern-either` to match multiple variations of command execution functions (`exec`, `execSync`, `spawn`, `spawnSync`, `system`, and `execFile`) in JavaScript.
   - The `pattern-not-inside` clause ensures that safe usages, such as commands starting with a known safe prefix inside a try-catch block, are not flagged by the rule.

2. **Metadata**:
   - The metadata provides context about the rule, including the CWE identifier, confidence, likelihood, impact, and subcategory, aligning with best practices for Semgrep rule metadata【4:18†source】.

3. **Examples**:
   - Examples are provided to illustrate code that will trigger the rule (ruleid) as well as code that will not trigger it (ok), enhancing understanding and verification context.

### Usage Considerations:
- It's important to test the rule with real-world code to ensure effectiveness and to minimize false positives. This can be done using various codebases to verify that genuine vulnerabilities are detected while safe code is not flagged【4:19†source】.