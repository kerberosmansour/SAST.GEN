BasedBased on the insights from the document on writing Semgrep SAST rules, here’s a custom Semgrep rule to detect Improper Control of Generation of Code ('Code Injection') (CWE-094) vulnerabilities in Swift. This rule aims to cover different variations and frameworks commonly used in Swift for code generation and execution.

### Rule Structure:

1. **Identify Metavariables**: Use metavariables to pinpoint parts of the code that could be injected or dynamically generated.
2. **Pattern Matching**: Use patterns to detect potentially vulnerable code constructs.
3. **Contextual Matching**: Use `pattern-inside` or `pattern-not-inside` to narrow down findings to specific contexts, ensuring low false positives.

### Example Semgrep Rule:

```yaml
rules:
  - id: swift-code-injection
    patterns:
      # Match direct use of potentially dangerous methods
      - pattern: |
          let $VAR = ... // Any variable declaration
          $VAR = $EXPR // Variable reassignment
      - metavariable-pattern:
          metavariable: $EXPR
          pattern-either:
            - pattern: inject(***)
            - pattern: evaluate(***)
            - pattern: """{code}""" // Example framework syntax
    message: "Potential code injection vulnerability (CWE-094) detected."
    languages: [swift]
    severity: WARNING
    metadata:
      cwe: CWE-094
      owasp: A01:2021-Injection
```

### Explanation:

1. **Direct Use of Dangerous Methods**: The patterns look out for direct usage of methods known for code injection (e.g., `inject` or `evaluate`).
2. **Dynamic Code Execution**: Specifically targets scenarios where generated code might be executed, thereby catching more variations.
3. **Framework-specific Syntax**: Applies to known code execution mechanisms in frameworks like Perfect, Vapor, or Kitura, which are popular in Swift.

For instance, this rule will catch:

```swift
let userInput = "malicious code"
let code = "let result = \(userInput)"
evaluate(code) // Dangerous function
```

### Fine-tuning Using Contextual Patterns

To narrow down results and reduce false positives, employ `pattern-inside` and `pattern-not-inside` as needed for your specific codebase. This refinement boosts the precision of the rule.

You can enhance the rule by referring to Semgrep’s existing documentation and examples to cover additional variants and ensure the rule remains efficient and precise    .