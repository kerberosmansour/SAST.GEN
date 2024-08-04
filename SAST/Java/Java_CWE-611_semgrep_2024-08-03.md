BasedBased on the context given in the document `/Users/sherif/Documents/GitHub/SVPS/Semgrep.output.md`, here's a custom Semgrep SAST rule to detect Improper Restriction of XML External Entity Reference (CWE-611) in Java. This rule includes patterns for popular frameworks like JAXP, SAX, and DOM:

```yaml
rules:
  - id: java-xxe-cwe-611
    languages:
      - java
    message: "Improper Restriction of XML External Entity Reference (XXE) in Java"
    severity: ERROR
    patterns:
      - pattern-either:
          # Detecting XXE in JAXP
          - pattern: |
              DocumentBuilderFactory $DBF = DocumentBuilderFactory.newInstance();
              $DBF.setFeature("http://javax.xml.XMLConstants/feature/secure-processing", false);
          - pattern: |
              DocumentBuilderFactory $DBF = DocumentBuilderFactory.newInstance();
              $DBF.setFeature("http://apache.org/xml/features/disallow-doctype-decl", false);
          - pattern: |
              SAXParserFactory $SPF = SAXParserFactory.newInstance();
              $SPF.setFeature("http://javax.xml.XMLConstants/feature/secure-processing", false);
          - pattern: |
              SAXParserFactory $SPF = SAXParserFactory.newInstance();
              $SPF.setFeature("http://apache.org/xml/features/disallow-doctype-decl", false);
          # Detecting vulnerable usage in DOM or SAX Parsing without proper features
          - pattern-not: |
              $DBF.setFeature("http://javax.xml.XMLConstants/feature/secure-processing", true);
          - pattern-not: |
              $SPF.setFeature("http://javax.xml.XMLConstants/feature/secure-processing", true);
    metadata:
      cwe: "CWE-611"
      references:
        - "https://cwe.mitre.org/data/definitions/611.html"
```

### Explanation
- **patterns**: Series of patterns that match specific code instances leading to XXE vulnerabilities.
- **pattern-either**: Used to specify multiple alternative patterns.
- **pattern**: Specific patterns including common misconfigurations of `DocumentBuilderFactory` and `SAXParserFactory` leading to XXE.
- **pattern-not**: Ensures proper configurations are not flagged.

Deploy this rule using Semgrep to scan Java codebases for XXE vulnerabilities. Trying it in a Semgrep Playground or your local environment can help validate and refine the rule.

### References
- The provided snippets showed how to optimize Semgrep rules, manage pattern exclusions, and write patterns to detect certain programming issues      .

Feel free to ask for any further details or assistance, Sherif Mansour!