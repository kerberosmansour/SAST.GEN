BasedBased on the provided information and understanding of Semgrep SAST rules, here is a set of custom Semgrep rules to detect "Improper Control of Generation of Code ('Code Injection') (CWE-094)" vulnerabilities in JavaScript, including variations across popular frameworks.

### Rule for Generic Code Injection

```yaml
rules:
  - id: generic-code-injection
    patterns:
      - pattern: |
          eval($CODE)
      - pattern-not: |
          eval(safeFunction($CODE))
    message: "Possible code injection vulnerability using eval() detected."
    languages: [javascript]
    severity: ERROR
```

### Rule for Specific Frameworks (Node.js example)

#### Using `Function` Constructor

```yaml
rules:
  - id: function-constructor-code-injection
    patterns:
      - pattern: |
          new Function($ARGS, $CODE)
      - pattern-not: |
          new Function($ARGS, safeFunction($CODE))
    message: "Possible code injection vulnerability using the Function constructor detected."
    languages: [javascript]
    severity: ERROR
```

#### Using `vm` module

```yaml
rules:
  - id: vm-module-code-injection
    patterns:
      - pattern: |
          const vm = require('vm');
          vm.runInNewContext($CODE)
      - pattern-not: |
          const vm = require('vm');
          vm.runInNewContext(safeFunction($CODE))
    message: "Possible code injection vulnerability using vm.runInNewContext detected."
    languages: [javascript]
    severity: ERROR
```

### Rule for React Applications

#### Inline Event Handlers

```yaml
rules:
  - id: react-inline-event-handler
    patterns:
      - pattern: |
          <div onClick={eval($CODE)} />
      - pattern-not: |
          <div onClick={safeFunction(eval($CODE))} />
    message: "Possible code injection vulnerability in React inline event handler using eval detected."
    languages: [javascript]
    severity: ERROR
```

### Rule Involving Taint Tracking

#### Taint Source and Sink Definition

```yaml
rules:
  - id: taint-tracking-code-injection
    mode: taint
    pattern-sources:
      - pattern: req.body.$DATA
    pattern-sinks:
      - pattern: eval($DATA)
    message: "Data from request body is being evaluated directly, possible code injection."
    languages: [javascript]
    severity: ERROR
```

### Explanation

1. **Generic Code Injection**:
   - Detects usage of `eval` with arbitrary code without any prior sanitization.

2. **Framework Specific**:
   - **Function Constructor**: Detects the use of the `Function` constructor with unsanitized code.
   - **vm Module**: Monitors the Node.js `vm` module for unsafe execution contexts.

3. **React Inline Handlers**:
   - Identifies in-line event handlers leveraging `eval` within JSX to prevent code injection through React components.

4. **Taint Tracking**:
   - Utilizes Semgrep's taint mode to track data flow from HTTP request bodies to `eval`, highlighting dangerous data evaluation patterns.

These rules employ various Semgrep operators like `pattern`, `pattern-not`, and `metavariable-pattern` to ensure thorough detection of code injection vulnerabilities across different JavaScript frameworks.

Please validate these rules with your specific setup and include any necessary sanitization functions (`safeFunction` in examples) as required.

**Sources**:
- Detailed guidelines on writing Semgrep rules can be found in the provided document sections    .