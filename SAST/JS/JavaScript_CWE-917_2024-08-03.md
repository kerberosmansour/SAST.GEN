BasedBased on the gathered information, here is a custom Semgrep SAST rule for detecting Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') (CWE-917) in JavaScript. This rule covers variations in popular frameworks for the mentioned language, such as React, Angular, Vue.js, and others.

```yaml
rules:
  - id: expression-language-injection
    patterns:
      - pattern-either:
          # React
          - pattern: |
              function $FUNC(...) {
                return (
                  <div dangerouslySetInnerHTML={{__html: $DATA}} />
                );
              }
          # Angular
          - pattern: |
              <div [innerHTML]="$DATA"></div>
          - pattern: |
              element.innerHTML = $DATA;
          # Vue.js
          - pattern: |
              <div v-html="$DATA"></div>
      - metavariable-pattern:
          metavariable: $DATA
          patterns:
            - pattern-not: safeHtml($DATA)
    message: "Improper Neutralization of Special Elements used in an Expression Language Statement, leading to potential Expression Language Injection (CWE-917). Consider sanitizing the input using suitable libraries or methods."
    languages:
      - javascript
      - typescript
    severity: ERROR
    metadata:
      cwe: "CWE-917"
      owasp: "A1:2017 - Injection"
      description: "Improper Neutralization of Special Elements used in an Expression Language Statement in various JavaScript frameworks, leading to potential vulnerabilities."
      references:
        - "https://cwe.mitre.org/data/definitions/917.html"
    examples:
      - code: |
          // Improper usage example
          function renderContent(data) {
            return (
              <div dangerouslySetInnerHTML={{__html: data}} />
            );
          }
      - code: |
          // Proper usage example with sanitization
          function renderContent(data) {
            return (
              <div dangerouslySetInnerHTML={{__html: safeHtml(data)}} />
            );
          }
```

This rule leverages various techniques such as pattern matching specific to frameworks and the metavariable-pattern functionality. It aims to detect instances where special elements are used improperly without sanitization across different frameworks. The `pattern-either` clause helps to manage multiple variations, while `metavariable-pattern` ensures that safe practices like using a hypothetical `safeHtml` function are not flagged.

Feel free to adjust the patterns and metadata according to the specific needs and contexts of your projects. If you need further customization or more specific patterns, especially for other frameworks not listed, please let me know!