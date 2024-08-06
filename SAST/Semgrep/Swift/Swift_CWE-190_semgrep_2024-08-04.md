BasedBased on the information from your file about writing Semgrep rules, here are some key strategies for creating effective Semgrep SAST rules:

1. **Metavariables & Patterns**: Utilize metavariables to represent parts of the code that can change. Combining multiple patterns ensures that rules are both specific and flexible.
2. **Ellipsis Operator**: Use the ellipsis operator to match zero or more characters, statements, or parameters, which helps to handle variations in code.
3. **Optimize for Performance**: Focus on reducing false positives and false negatives by narrowing down the context where rules apply (e.g., using `pattern-inside`, `pattern-not-inside`, etc.)     .

### Semgrep Rule for Integer Overflow or Wraparound (CWE-190) in Swift:

Here is a Semgrep rule designed to catch potential Integer Overflow or Wraparound vulnerabilities in Swift code. The rule includes variations to handle different contexts and usages of integer operations.

```yaml
rules:
  - id: swift-integer-overflow
    languages: [swift]
    message: "Possible Integer Overflow or Wraparound detected. Ensure bounds checking is performed."
    severity: WARNING
    patterns:
      - pattern: |
          ... = $X + $Y
      - metavariable-pattern:
          metavariable: $X
          patterns:
            - pattern: $A.max
            - pattern: UInt8.max
            - pattern: UInt16.max
            - pattern: UInt32.max
            - pattern: UInt64.max
            - pattern: Int8.max
            - pattern: Int16.max
            - pattern: Int32.max
            - pattern: Int64.max
      - pattern-not-inside:
          - pattern: if $CONDITION {
                         $CHECK
                     }
  - id: swift-integer-wraparound-multiplication
    languages: [swift]
    message: "Possible Integer Wraparound in multiplication detected. Ensure proper bounds checking."
    severity: WARNING
    patterns:
      - pattern: |
          ... = $X * $Y
      - metavariable-pattern:
          metavariable: $X
          patterns:
            - pattern: $A.max
            - pattern: UInt8.max
            - pattern: UInt16.max
            - pattern: UInt32.max
            - pattern: UInt64.max
            - pattern: Int8.max
            - pattern: Int16.max
            - pattern: Int32.max
            - pattern: Int64.max
      - pattern-not-inside:
          - pattern: if $CONDITION {
                         $CHECK
                     }
  - id: swift-integer-overflow-subtraction
    languages: [swift]
    message: "Possible Integer Overflow or Wraparound in subtraction detected. Ensure bounds checking."
    severity: WARNING
    patterns:
      - pattern: |
          ... = $X - $Y
      - metavariable-pattern:
          metavariable: $X
          patterns:
            - pattern: $A.min
            - pattern: UInt8.min
            - pattern: UInt16.min
            - pattern: UInt32.min
            - pattern: UInt64.min
            - pattern: Int8.min
            - pattern: Int16.min
            - pattern: Int32.min
            - pattern: Int64.min
      - pattern-not-inside:
          - pattern: if $CONDITION {
                         $CHECK
                     }
  - id: swift-integer-overflow-division
    languages: [swift]
    message: "Possible Integer Overflow or Wraparound in division detected. Ensure bounds checking."
    severity: WARNING
    patterns:
      - pattern: |
          ... = $X / $Y
      - metavariable-pattern:
          metavariable: $X
          patterns:
            - pattern: 0
          patterns-not:
            - pattern: if $Y != 0
```

### Explanation:

1. **`patterns`**:
    - Different arithmetic operations (addition, multiplication, subtraction, division) are covered separately to improve specificity.
    - `$X` and `$Y` are used as metavariables representing operands.
    - Specific patterns handle operations involving max and min values for various integer types (to detect overflow).

2. **`pattern-not-inside`**:
    - Ensures that checks within conditional statements are not flagged if bounds checking is already performed.

3. **`metavariable-pattern`**:
    - Use this to ensure integers are checked against known max or min values for their types, helping improve the precision of the detection.

By following these patterns, the rule aims to maintain high accuracy by reducing the rate of false positives while ensuring that potential overflows and wraparounds are effectively caught    .