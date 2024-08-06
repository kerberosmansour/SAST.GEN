CertainlyCertainly, Sherif. Below is a Semgrep rule specifically crafted to detect the vulnerability of "Access of Resource Using Incompatible Type ('Type Confusion')" (CWE-843) in JavaScript. This rule is designed to cover variations in popular frameworks like Node.js, React, and Vue.js:

```yaml
rules:
  - id: type-confusion-js
    description: Detects Type Confusion vulnerabilities in JavaScript
    languages: [javascript]
    severity: ERROR
    message: Access of resource using incompatible type ('Type Confusion') detected
    metadata:
      cwe: CWE-843
    patterns:
      - pattern: |
          function $FUNC($ARG) {
            ...
            if ($ARG.$FIELD !== undefined) {
              $VAR = $ARG.$FIELD;
            }
            ...
          }
      - metavariable-pattern:
          metavariable: $FIELD
          pattern: string|number|object|boolean
    pattern-either:
      - pattern: |
          $OBJ = { $FIELD: $VAL };
          $FUNC($OBJ);
      - pattern: |
          $FUNC({ $FIELD: $VAL });
    pattern-not:
      pattern: |
        typeof $ARG.$FIELD !== typeof $VAR
    message: Potential Type Confusion: "$FIELD" is being accessed with inconsistent types
    severity: HIGH
    paths:
      include:
        - "**/*.js"
        - "**/*.jsx"
        - "**/*.ts"
        - "**/*.tsx"
    metadata:
      cwe: CWE-843
      confidence: HIGH
      impact: HIGH
      likelihood: MEDIUM
      subcategory: vuln
```

### Explanation of the Rule Components:

- **id**: A unique identifier for the rule.
- **description**: Provides a brief explanation of the rule.
- **languages**: Specifies the target language for the rule, which is JavaScript in this case.
- **severity**: Sets the severity level of the detected issue.
- **message**: The alert message that will be shown when the rule is matched.
- **metadata**: Additional information about the rule, including the CWE identifier, confidence, impact, likelihood, and subcategory.
- **patterns**: Defines the main pattern to identify potential type confusion issues.
- **metavariable-pattern**: Filters the `$FIELD` metavariable to ensure it matches common types (string, number, object, boolean).
- **pattern-either**: Allows the rule to match either object instantiation method.
- **pattern-not**: Ensures the rule does not match if type checking is performed correctly.
- **paths**: Specifies the file extensions to include in the scan.

This rule attempts to identify and catch scenarios where a property of an object might be accessed with an inconsistent type, specifically to prevent type confusion vulnerabilities.

Feel free to customize or refine the rule according to the specific requirements and context of your project. For reference, you can check some of the approaches used for related rules in the provided example document【4:0†source】【4:1†source】【4:6†source】【4:8†source】【4:13†source】【4:14†source】.