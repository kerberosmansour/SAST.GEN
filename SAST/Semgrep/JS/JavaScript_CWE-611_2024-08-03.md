ToTo write a Semgrep SAST rule for detecting Improper Restriction of XML External Entity Reference (CWE-611) in JavaScript, we need a rule that can handle various ways of loading or parsing XML data across different frameworks. Here is how you can create such a Semgrep rule:

```yaml
rules:
  - id: improper-xxe-JS
    patterns:
      - pattern: >
          const parser = new $PARSER({
            ...
          });
          ...
          parser.parse(...);
    patterns-inside:
      - pattern-not: new $PARSER({
            expand_entities: true,
            ...
          });

    message: Improper restriction of XML external entity reference (XXE) detected. Ensure that `expand_entities` is set to `true`.
    languages: [javascript]
    severity: ERROR
    metadata:
      cwe: "CWE-611"
      confidence: HIGH
      likelihood: HIGH
      impact: HIGH
      subcategory: vulns
```

### Explanation of the Rule Components:
1. **`id`**: A unique identifier for the rule.
2. **`patterns`**: Specifies patterns to look for in the code. Here we're looking for instances where an XML parser object is initialized with potentially risky properties.
3. **`pattern-not`**: This clause ensures that the rule does not match when the secure option `expand_entities: true` is set, thereby ignoring false positives where the mitigation is already applied.
4. **`message`**: Message displayed when a match is found.
5. **`languages`**: Specifies that this rule is for JavaScript.
6. **`severity`**: Sets the severity level of the issue.
7. **`metadata`**: Includes additional context for the rule, such as the relevant CWE, confidence, likelihood, impact, and subcategory.

### Context Supported:
- **XML parsers across different frameworks**: You may need to generalize the patterns to cover other specific libraries like `xml2js`, `xmldom`, `fast-xml-parser`, etc.

### Ensure to Test Variations:
- For example, testing with xml2js might look like:
  ```javascript
  const parser = new xml2js.Parser({
    ...
  });
  parser.parseString(...);
  ```

Replace the `PARSER` with the different parsers used in the frameworks you are targeting.

For more detailed information and examples on custom rule writing syntax, you can refer to the `Semgrep.output.md` provided .