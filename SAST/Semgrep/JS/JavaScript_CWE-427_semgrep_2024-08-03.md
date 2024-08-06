#### Writing Semgrep SAST Rules for Uncontrolled Search Path Element (CWE-427) in JavaScript

Based on the provided context and examples of Semgrep rules, I'll help you create a custom rule to detect instances of uncontrolled search path elements in JavaScript. This will involve generating Semgrep SAST rules that cover different variations of this vulnerability, including those that might occur in popular frameworks.

### Vulnerability Overview

**Uncontrolled Search Path Element (CWE-427)**: This type of vulnerability occurs when a program uses external input to construct a path or command, typically for loading a library or an executable, without properly managing or sanitizing the input, leading to the possibility of an attacker manipulating the execution path.

### Example Scenarios

- Direct use of unsanitized input in `require` or `import`.
- Use of environment variables to determine a path or command.
- Use of user-provided paths to load files or modules within popular frameworks such as Express.js or Electron.

### Semgrep SAST Rule Example

Our Semgrep rule will look for the following patterns:
1. Direct `require` or `import` using unsanitized input.
2. Using environment variables to construct paths for `require` or `import`.
3. Common patterns in frameworks like Express.js where user input may affect the module load path.

```yaml
rules:
  - id: uncontrolled-search-path-elem
    patterns:
      - pattern: require($VAR)
      - metavariable-pattern:
          metavariable: $VAR
          patterns:
            - pattern-not: sanitize($VAR)
            - pattern-not: validate($VAR)
    message: "Potential uncontrolled search path element in require"
    severity: ERROR
    languages: [javascript]

  - id: uncontrolled-search-path-import
    patterns:
      - pattern: import $VAR from ...
      - metavariable-pattern:
          metavariable: $VAR
          patterns:
            - pattern-not: sanitize($VAR)
            - pattern-not: validate($VAR)
    message: "Potential uncontrolled search path element in import"
    severity: ERROR
    languages: [javascript]

  - id: env-var-path-usage
    patterns:
      - pattern: |
          const $VAR = process.env[$ENV_VAR];
          require($VAR)
      - metavariable-pattern:
          metavariable: $VAR
          patterns:
            - pattern-not: sanitize($VAR)
            - pattern-not: validate($VAR)
    message: "Potential uncontrolled search path element via environment variable"
    severity: ERROR
    languages: [javascript]

  - id: express-path-param
    patterns:
      - pattern: |
          app.get('/path/:param', (req, res) => {
            require(`./path/to/module/${req.params.param}`);
          });
      - metavariable-pattern:
          metavariable: $VAR
          patterns:
            - pattern-not: sanitize(req.params.param)
            - pattern-not: validate(req.params.param)
    message: "Potential uncontrolled search path element via req.params in Express"
    severity: ERROR
    languages: [javascript]

  - id: electron-file-path
    patterns:
      - pattern: |
          const $VAR = require('electron').remote.dialog.showOpenDialog(...);
          require($VAR[0]);
      - metavariable-pattern:
          metavariable: $VAR
          patterns:
            - pattern-not: sanitize($VAR[0])
            - pattern-not: validate($VAR[0])
    message: "Potential uncontrolled search path element in Electron"
    severity: ERROR
    languages: [javascript]
```

### Explanation of Patterns

1. **Direct `require` or `import` using unsanitized input:**
   - This rule covers any use of `require` or `import` where the variable being used has not gone through a sanitization process.

2. **Using environment variables:**
   - This checks for situations where environment variables are used to construct the path for `require`.

3. **Framework-specific patterns:**
   - For Express.js, we monitor for the use of user-provided path parameters in `require`.
   - For Electron, we check for the paths returned by their dialog module being used directly without validation.

### Testing and Validation

Each rule should be tested against known vulnerable and secure code patterns to ensure accuracy and minimize false positives. Example vulnerable code snippets were used to match the patterns specified.

### References

- The structure and methodology of Semgrep rules are inspired by the Semgrep documentation and examples  .
- [Semgrep Documentation](https://semgrep.dev/docs/)
- [Semgrep Playground](https://semgrep.dev/playground)

Sherif Mansour, if you have any specific frameworks or scenarios you'd like more coverage on, please let me know!