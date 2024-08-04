ToTo create Semgrep SAST rules for detecting "Access of Resource Using Incompatible Type ('Type Confusion')" (CWE-843) in Swift, it's essential to follow proper rule-writing techniques that minimize false positives and optimize performance. Based on the information from the uploaded document, here are some key points to consider while crafting the rules:

### Strategy and Approach

1. **Metavariable Usage**: Use metavariables to capture and track types and values across patterns.
2. **Pattern-Not and Pattern-Either**: Exclude known safe type conversions and handle alternative patterns that may represent the same type confusion.
3. **Contextual Matching**: Use pattern-inside and pattern-not-inside to contextualize where the pattern should or shouldn't match.

### Example Rule for Type Confusion in Swift

```yaml
rules:
  - id: swift-type-confusion
    patterns:
      - pattern-either:
        # Unsafe type cast patterns
        - pattern: |
            let $VAR: $TYPE_A = ...
            ...
            let $VAR2 = $VAR as! $TYPE_B
        - pattern: |
            let $VAR = ...
            ...
            if let $VAR2 = $VAR as? $TYPE_B { ... }
      - metavariable-pattern:
          metavariable: $TYPE_B
          pattern-not: $TYPE_A
    languages: [swift]
    severity: ERROR
    message: "Potential type confusion detected between $TYPE_A and $TYPE_B"
    metadata:
      cwe: "CWE-843"
    url: "https://cwe.mitre.org/data/definitions/843.html"

  - id: swift-type-confusion-array
    patterns:
      - pattern: |
          let $VAR: [$TYPE_A] = ...
          ...
          let $VAR2 = $VAR as! [$TYPE_B]
      - metavariable-pattern:
          metavariable: $TYPE_B
          pattern-not: $TYPE_A
    languages: [swift]
    severity: ERROR
    message: "Potential type confusion detected between array types $TYPE_A and $TYPE_B"
    metadata:
      cwe: "CWE-843"
    url: "https://cwe.mitre.org/data/definitions/843.html"

  - id: swift-type-confusion-dictionary
    patterns:
      - pattern: |
          let $VAR: [$KEY: $TYPE_A] = ...
          ...
          let $VAR2 = $VAR as! [$KEY: $TYPE_B]
      - metavariable-pattern:
          metavariable: $TYPE_B
          pattern-not: $TYPE_A
    languages: [swift]
    severity: ERROR
    message: "Potential type confusion detected between dictionary types $TYPE_A and $TYPE_B"
    metadata:
      cwe: "CWE-843"
    url: "https://cwe.mitre.org/data/definitions/843.html"
```

### Explanation and Variations Covered

1. **Rule 1**: Detects unsafe casts from one concrete type to another different type.
2. **Rule 2**: Specifically for array types, ensuring arrays maintain consistency in type.
3. **Rule 3**: Covers dictionaries, ensuring both key and value types are consistent and safe from type confusion.

### Advanced Techniques for Precision

- **Pattern-Not**: Used to ensure that the target type (`TYPE_B`) is not the same as the original type (`TYPE_A`).
- **Pattern-Either**: Used to handle different syntax forms for unsafe casts and optional casts.

By implementing these rules and leveraging techniques such as metavariables and pattern-not, the rules aim to accurately detect type confusions, thus providing a high false negative rate and low false positive rate as required.

This strategic application minimizes false positives by being explicit in type checks and using Swift's type system rules effectively.

### References
- Custom Semgrep rule tutorial and syntax examples【4:0†source】 .
- Usage of pattern-inside, pattern-not-inside, and metavariable techniques for effective rule writing 【4:0†source】 .

By following these guidelines, the Semgrep rules will effectively capture type confusion vulnerabilities in Swift projects.