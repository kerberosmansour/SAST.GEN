To create Semgrep SAST rules that detect "Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') (CWE-078)" in Swift, follow these steps using the examples and techniques from the provided document:

1. **Define the pattern to detect command injection in Swift**: Use Semgrep's metavariables and operators to create patterns that match common OS command injection points, such as `Process`, `system`, `sh`, and others.

2. **Include metavariable analysis**: Use metavariables to capture dynamic content that might be injected.

3. **Use `pattern-inside` and `pattern-not-inside`**: Refine rules by specifying contexts where commands should or should not match【4:1†source】【4:3†source】 .

### Example Rule: Detecting OS Command Injection in Swift

```yaml
rules:
  - id: swift-os-command-injection
    languages: [swift]
    message: "Possible OS Command Injection detected"
    severity: ERROR
    patterns:
      # Check for use of five common command execution methods
      - pattern-either:
        - pattern: ProcessInfo.processInfo.environment[$VAR]!
        - pattern: Process(...).launch()
        - pattern: Process(...).run()
        - pattern: sh(...)

      # Check for concatenation of dynamic user inputs within command strings
      - pattern: $CMD = "... " + $INJECT + " ..."
      - pattern-either:
        - metavariable-pattern:
            metavariable: $COMMAND
            patterns:
              - pattern: ... = $CMD
              - pattern-not: "sh -c $INJECT"

    # Example of deeper analysis with `metavariable-comparison` (match dynamic injection)
    - pattern: Process($INPUT)
    - metavariable-pattern:
        metavariable: $INPUT
        patterns:
          - pattern-inside: "... = $DANGEROUS_PARAM"
          # Sanitize safe methods (avoid)
          - pattern-not-inside: |
              let safePaths = getSafePaths()
              if safePaths.contains($DANGEROUS_PARAM) { ... }
          - pattern-not-inside: |
              let safeParams = getSafeParams()
              if safeParams.contains($DANGEROUS_PARAM) { ... }

    example:
        syntax: swift
        code: |
          let cmd = "ls \(userInput)"
          Process.create(cmd).launch()
```

### Explanation of the Rule Components:

1. **Patterns Section**: 
   - `pattern-either` combines multiple suspicious command execution patterns such as `Process(...)`, `system(...)`, and `sh(...)` to catch OS command execution.
   - `pattern` to capture string concatenations involving potentially insecure dynamic inputs.
   
2. **Metavariable Pattern**:
   - `metavariable-pattern` and `pattern-inside` are used for deeper analysis such as identifying if the dynamic input passed to the command is potentially dangerous .

3. **Severity and Message**:
   - Include a clear `message` that will be shown when a match is found and set the `severity` level to categorize the rule.

### Refinements:

Use additional patterns inside either sections and comparisons to cover variations and reduce false positives. Leveraging techniques such as taint tracking and symbolic propagation could further enhance the rule accuracy【4:1†source】【4:16†source】 .

This Semgrep rule aims to detect high-risk situations with low false positives by filtering out known safe patterns and verifying dynamic input positioning within the command strings. Adjust this base template according to the specific syntax and semantics of the Swift codebases you work with.