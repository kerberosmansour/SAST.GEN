ToTo write robust Semgrep Static Application Security Testing (SAST) rules for detecting "Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')" (CWE-917) in Swift, follow these guidelines. The rule must cover various frameworks popular in Swift:

### Semgrep SAST Rules for CWE-917 in Swift

#### 1. Identify Potential Injection Points
Search for common functions and methods that might accept untrusted input in Swift frameworks such as:
- Foundation
- SwiftUI
- Vapor

#### 2. Use `pattern-either` to Cover Multiple Variations
Combine patterns to catch different variations of the vulnerability.

#### Example Custom Rule

```yaml
rules:
  - id: cwe-917-expression-language-injection
    languages: [swift]
    message: "Potential Expression Language Injection detected"
    severity: ERROR
    patterns:
      - pattern: |
          @$INJECTION_ANNOTATION(...)
          func $FUNC(...) {
            # Potentially unsafe code here
            ...
          }
      - pattern: |
          $CLASS @INJECTION_ANNOTATION
          ...
          $CLASS_FUNC(...)
          ...
      - pattern: |
          let $VAR = $DATA_SOURCE
          ...
          evaluate(expression: $VAR)
    pattern-either:
      - pattern: |
          @UIApplicationMain
      - pattern: |
          @IBDesignable
      - pattern: |
          @IBAction
    metadata:
      cwe: "CWE-917"
      owasp: "A10:2017 - Insufficient Logging and Monitoring"

```

### Explanation of the Rule Components

#### `patterns`
1. **Annotations**: Check for unsafe annotations that might suggest user input is being processed.
   - `@$INJECTION_ANNOTATION(...)` captures any annotation.
   - `@UIApplicationMain` and `@IBDesignable` are specific annotations that could be vulnerable when handling input.
   
2. **Function Patterns**: Identify unsafe functions or classes annotated in a way that they can process user input.
   - `func $FUNC(...)` captures any function.
   - Using `$CLASS_FUNC(...)` captures methods within classes to apply annotations like `@IBAction`.

3. **Variable Patterns**: Identify places where input is being read or evaluated. 
   - `let $VAR = $DATA_SOURCE` captures variable declarations where data is being assigned from an unknown or potentially unsafe source.
   - `evaluate(expression: $VAR)` ensures that the variable with user data is being evaluated, which signifies the vulnerability.

#### `pattern-either`
Combines multiple annotations to detect a more extensive range of potential issues.

### Using the Rule
To use the rule, save the configuration in a YAML file (e.g., `swift_cwe_917.yaml`) and run Semgrep using the following command:

```sh
semgrep --config swift_cwe_917.yaml /path/to/swift/project
```

### Additional Best Practices
1. **Context-Aware Matching**: Use `pattern-inside` and `pattern-not-inside` for specific contexts to reduce false positives.
2. **Keeping Rules Updated**: Review and update your rules regularly as new frameworks and coding practices evolve.
3. **Testing Rules**: Test the rules in diverse codebases to ensure they accurately identify vulnerabilities without raising unnecessary false positives and negatives.

Refer to the official [Semgrep documentation](https://semgrep.dev/docs/) for further details and best practices when writing custom rules【4:0†source】【4:1†source】【4:3†source】.