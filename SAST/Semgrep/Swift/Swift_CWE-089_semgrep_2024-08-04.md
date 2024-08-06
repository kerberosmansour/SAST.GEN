BasedBased on the information from your file and applying best practices for writing Semgrep rules, below is a set of Semgrep SAST rules to detect SQL Injection vulnerabilities (CWE-089) in Swift, covering its variations across popular frameworks:

### Rule for Direct SQL Queries
This rule detects direct SQL queries executed within the code using raw strings. It uses the ellipsis operator `...` to generalize patterns and metavariables to improve flexibility and match different variations.

```yaml
rules:
  - id: swift-sql-injection-raw-query
    languages: [swift]
    message: "Potential SQL Injection in raw query execution"
    severity: WARNING
    patterns:
      - pattern: |
          let $query = "$SQL_QUERY"
      - metavariable-pattern:
          metavariable: $SQL_QUERY
          patterns:
            - pattern: ...$UNTRUSTED_INPUT...
    metadata:
      cwe: "CWE-89"
      owasp: "A1: Injection"
      reference: "https://semgrep.dev/docs/writing-rules/overview/"
```

### Rule for Unsafe String Interpolation in Queries
This rule catches unsafe string interpolation by checking interpolations of untrusted input within SQL query strings.

```yaml
rules:
  - id: swift-sql-injection-string-interpolation
    languages: [swift]
    message: "Potential SQL Injection via string interpolation in SQL query"
    severity: WARNING
    patterns:
      - pattern: |
          let $query = "SELECT ... \($UNTRUSTED_INPUT) ..."
      - pattern-inside: |
          executeQuery($query)
    metadata:
      cwe: "CWE-89"
      owasp: "A1: Injection"
      reference: "https://semgrep.dev/docs/writing-rules/overview/"
```

### Rule for Improper Use of ORM Methods
This rule detects improper use of ORM-like methods where raw SQL queries or dynamic query building using untrusted inputs are executed. 

```yaml
rules:
  - id: swift-sql-injection-orm-methods
    languages: [swift]
    message: "Potential SQL Injection in ORM method"
    severity: WARNING
    patterns:
      - pattern: |
          db.rawQuery("$QUERY_STRING")
      - metavariable-pattern:
          metavariable: $QUERY_STRING
          patterns:
            - pattern: ...$UNTRUSTED_INPUT...
    metadata:
      cwe: "CWE-89"
      owasp: "A1: Injection"
      reference: "https://semgrep.dev/docs/writing-rules/overview/"
```

### Rule for Vulnerable SQL Frameworks
This rule identifies known vulnerable SQL frameworks or insecure configurations commonly used in Swift applications.

```yaml
rules:
  - id: swift-sql-injection-vulnerable-framework
    languages: [swift]
    message: "Use of vulnerable SQL framework or insecure configuration"
    severity: WARNING
    patterns:
      - pattern-either:
          - pattern: |
              import SQLite
          - pattern: |
              useUnsafeParameter($PARAM)
    metadata:
      cwe: "CWE-89"
      owasp: "A1: Injection"
      reference: "https://semgrep.dev/docs/writing-rules/overview/"
```

### Rule for Dynamic SQL Query Construction
Detecting queries that are constructed dynamically by concatenating strings and variables which might include untrusted input.

```yaml
rules:
  - id: swift-sql-injection-dynamic-construction
    languages: [swift]
    message: "Potential SQL Injection in dynamic query construction"
    severity: WARNING
    patterns:
      - pattern: |
          let $query_part = "$PART1" + $UNTRUSTED_INPUT + "$PART2"
      - pattern-inside: |
          executeQuery($query_part)
    metadata:
      cwe: "CWE-89"
      owasp: "A1: Injection"
      reference: "https://semgrep.dev/docs/writing-rules/overview/"
```

These rules leverage the flexibility of Semgrep by using metavariables and the ellipsis operator, ensuring high accuracy and minimizing false positives. They are designed to catch various SQL injection patterns prevalent in different Swift frameworks.

For more about creating custom Semgrep rules, refer to the Semgrep documentation and example rules【4:0†source】   .