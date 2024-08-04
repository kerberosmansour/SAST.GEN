To generate Semgrep SAST rules for detecting "Improper Restriction of XML External Entity Reference (CWE-611)" in Swift, we'll design a few rules that aim to cover common scenarios and variations commonly seen in popular frameworks and libraries. These rules will focus on identifying patterns that can reveal vulnerabilities related to insecure handling of XML external entities.

### Steps to Write Semgrep SAST Rules

1. **Define the Pattern Syntax**: We need to identify common patterns that can be abstracted using `metavariable-pattern`, `pattern-inside`, `pattern-not-inside`, and `ellipsis` (`...`) operators.
2. **Targeted Languages**: Ensure that the rules are specified for the Swift language.
3. **False Positives and False Negatives**: Aim to minimize false positives by being as specific as possible.

### Example Rules

#### Rule 1: Direct XML Parsing with External Entity References

```yaml
rules:
  - id: swift-xml-external-entity
    patterns:
      - pattern: |
          let $VAR = XMLParser(contentsOf: URL(string: $URL)!)
      - pattern: |
          let $VAR = XMLParser(data: $DATA)
    message: "XML Parser is used with external entity references enabled, which might lead to CWE-611"
    languages: [swift]
    severity: ERROR
    metadata:
      cwe: CWE-611
```

#### Rule 2: XML Parsing in Common Swift Libraries

```yaml
rules:
  - id: swift-nosir-classes
    patterns:
      - pattern: |
          let $VAR = XMLParser(contentsOf: URL(string: $URL)!)
        - pattern: |
            xmlParser.shouldResolveExternalEntities = true
    message: "Potential CWE-611: Found XML parsing with external entity resolution enabled"
    languages: [swift]
    severity: ERROR
    metadata:
      cwe: CWE-611
```

#### Rule 3: External Library with Default Configuration

```yaml
rules:
  - id: swift-nsxml-document
    patterns:
      - pattern: |
          let $VAR = XMLDocument(contentsOf: URL(string: $URL)!)            
    message: "Using XMLDocument with external entities enabled might lead to CWE-611 vulnerability"
    languages: [swift]
    severity: ERROR
    metadata:
      cwe: CWE-611
```

#### Rule 4: Secure Setting for XML Parsing

```yaml
rules:
  - id: swift-xml-disable-external-entities
    patterns:
      - pattern: |
          $XMLPARSER.shouldResolveExternalEntities = false
    message: "Ensure external entities are disabled for secure XML processing"
    languages: [swift]
    severity: INFO
    metadata:
      cwe: CWE-611
```

#### Rule 5: Common XML Parsing Framework Usage (e.g., SWXMLHash)

```yaml
rules:
  - id: swift-swxmlhash-vulnerability
    patterns:
      - pattern: |
          let $VAR = SWXMLHash.parse($DATA)
    message: "SWXMLHash used without disabling external entities, investigate for CWE-611"
    languages: [swift]
    severity: WARNING
    metadata:
      cwe: CWE-611
```

### Explanation

1. **Patterns and Metavariables**: Use patterns to identify instances of XML parsing where external entities might be resolved. Metavariables (`$VAR`, `$URL`, `$DATA`) capture parts of the code that will be checked.
2. **Severity Levels**: Classify vulnerabilities into ERROR, WARNING, and INFO based on the criticality.
3. **Framework-Specific Rules**: Create targeted rules for different libraries and frameworks commonly used in Swift for XML parsing.
4. **Safe Configuration**: Include rules to ensure that the secure configuration (i.e., disabling external entities) is implemented.

### References

For more information on writing and testing Semgrep SAST rules, you can refer to the official documentation and examples:

- [Pattern Syntax Overview](https://semgrep.dev/docs/writing-rules/pattern-syntax) 
- [Writing Custom Rules](https://semgrep.dev/learn) 

You can experiment and refine these rules in the [Semgrep Playground](https://semgrep.dev/editor) to ensure they detect the appropriate vulnerabilities and minimize false positives and negatives. 

Would you like me to help you implement and test these rules in the playground?