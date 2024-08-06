ToTo generate effective Semgrep SAST rules for detecting SQL Injection vulnerabilities (CWE-089) in JavaScript, we need to consider various patterns such as raw SQL queries, concatenation of SQL commands and user inputs, and the use of JavaScript frameworks like Node.js with databases such as MySQL, Sequelize, or MongoDB.

Here are different rule variations to cover these scenarios:

### Rule 1: Detect Raw SQL Queries
Detects the use of raw SQL queries within the JavaScript code.

```yaml
rules:
  - id: js-sqlinjection-raw-sql
    patterns:
      - pattern: connection.query($QUERY, ...)
      - pattern: client.query($QUERY, ...)
      - metavariable-pattern:
          metavariable: $QUERY
          patterns:
            - pattern-not: '... ? ...'
    languages: [javascript]
    message: "Possible SQL Injection vulnerability."
    severity: ERROR
    metadata:
      cwe: CWE-089
      owasp: A1:2017-Injection
```

### Rule 2: Detect SQL Queries with String Concatenation
Detects SQL queries that are concatenated with user input directly.

```yaml
rules:
  - id: js-sqlinjection-concat
    patterns:
      - pattern: |
          connection.query("SELECT ... FROM ... WHERE ... " + $USER_INPUT, ...)
      - pattern: |
          client.query("SELECT ... FROM ... WHERE ... " + $USER_INPUT, ...)
    languages: [javascript]
    message: "Possible SQL Injection via string concatenation."
    severity: ERROR
    metadata:
      cwe: CWE-089
      owasp: A1:2017-Injection
```

### Rule 3: Detect SQL Queries in Sequelize (Node.js ORM)
Identifies potentially unsafe raw SQL queries in Sequelize, a popular ORM for Node.js.

```yaml
rules:
  - id: js-sqlinjection-sequelize-raw
    patterns:
      - pattern: sequelize.query($QUERY, ...)
      - pattern: db.query($QUERY, ...)
      - metavariable-pattern:
          metavariable: $QUERY
          patterns:
            - pattern-not: '... ? ...'
    languages: [javascript]
    message: "Possible SQL Injection in Sequelize raw query."
    severity: ERROR
    metadata:
      cwe: CWE-089
      owasp: A1:2017-Injection
```

### Rule 4: Detect Use of `eval()` with SQL Commands
Checks if `eval()` is used to dynamically execute SQL commands, which is a serious vulnerability pattern.

```yaml
rules:
  - id: js-sqlinjection-eval
    patterns:
      - pattern: eval("...SQL...")
      - pattern: eval($SQL_COMMAND)
    languages: [javascript]
    message: "Use of eval() with SQL commands may lead to SQL Injection."
    severity: ERROR
    metadata:
      cwe: CWE-089
      owasp: A1:2017-Injection
```

### Rule 5: Detect MongoDB Injections
Identifies unsafe user input being used directly in MongoDB queries, which can lead to NoSQL injection.

```yaml
rules:
  - id: js-nosqlinjection-mongodb
    patterns:
      - pattern: |
          db.collection('${COLLECTION}')
            .find({ $CONDITION: $USER_INPUT })
      - pattern: |
          db.collection(${COLLECTION})
            .find({ $CONDITION: $USER_INPUT })
    languages: [javascript]
    message: "Possible NoSQL Injection vulnerability with MongoDB."
    severity: ERROR
    metadata:
      cwe: CWE-089
      owasp: A1:2017-Injection
```

### Conclusion
These rules utilize the concepts of metavariable-patterns, ellipses (`...`), and specific patterns for different frameworks and methods as demonstrated in the examples of writing custom Semgrep rules【4:0†source】   . By covering these variations, we aim to detect a wide range of potential SQL and NoSQL injections in JavaScript code, enhancing the security posture of applications using Semgrep.

Make sure to adapt these rules further depending on the specific frameworks and coding practices used in your projects.