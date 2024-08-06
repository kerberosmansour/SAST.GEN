HereHere is a Semgrep SAST rule to detect Integer Overflow or Wraparound (CWE-190) in Java:

```yaml
rules:
  - id: java-integer-overflow
    languages: [java]
    message: "Potential integer overflow detected"
    severity: ERROR
    patterns:
      - pattern: |
          $VAR = $X + $Y
      - pattern: |
          $VAR = $X - $Y
      - pattern: |
          $VAR = $X * $Y
      - metavariable-comparison:
          metavariable: $Y
          comparison: $Y > 0 || $Y < 0
```

Explanation:

- This rule detects potential integer overflow vulnerabilities by looking for arithmetic operations (`+`, `-`, `*`) where a variable is assigned the result.
- The `metavariable-comparison` ensures a variable used in the arithmetic operation is either positive or negative, which is a common condition for overflow scenarios.
- This rule can be applied to popular Java frameworks by searching for common variable assignments.

To ensure you are catching a variety of scenarios, you can expand the rule to include more patterns and refine the conditions as needed.

For deeper customization and optimization, refer to the detailed guide and examples on writing custom Semgrep rules【4:0†source】 .