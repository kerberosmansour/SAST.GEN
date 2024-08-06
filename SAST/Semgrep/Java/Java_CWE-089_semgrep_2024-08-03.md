ToTo create a Semgrep rule for detecting SQL Injection vulnerabilities (CWE-089) in Java, consider the following custom rule based on the context provided:

### Semgrep Rule for SQL Injection in Java

1. **Rule Structure**:
   - **id**: A unique identifier for the rule.
   - **languages**: Specify the language (in this case, Java).
   - **message**: A brief description of the vulnerability identified.
   - **patterns**: Define the patterns that outline how the code should look to match potential vulnerabilities.
   - **severity**: The severity level of the rule.

2. **Patterns**:
   - Match SQL query constructions using concatenation of user inputs.
   - Match instances where `PreparedStatement` is used without parameterized queries.
   - Consider popular frameworks like JDBC and Spring JDBC.

### Example Rule

```yaml
rules:
  - id: java-sql-injection
    languages:
      - java
    message: "Potential SQL Injection vulnerability"
    severity: ERROR
    patterns:
      - pattern-either:
          # Detect concatenation of user input in SQL queries.
          - pattern: |
              String $QUERY = "..." + $INPUT + "...";
          - pattern: |
              String $QUERY = "SELECT ... FROM ... WHERE ..." + $INPUT + "...";
      - pattern-either:
          # Detect unsafe usage of PreparedStatement.
          - pattern: |
              $STMT = $CONN.createStatement();
              $RS = $STMT.executeQuery("SELECT ... FROM ... WHERE ..." + $INPUT + "...");

          - pattern: |
              $STMT = $CONN.createStatement();
              $RS = $STMT.executeQuery("..." + $INPUT + "...");
      - pattern-not:
          # Exclude safe practices with parameterized queries.
          - pattern: |
              $STMT.setString(..., ...);

          - pattern: |
              $PS.setInt(..., ...);
```

### Explanation
- The rule encompasses variations of SQL injection vulnerabilities including string concatenation and unsafe query execution.
- It captures both basic concatenation patterns and those that involve executing queries with input directly passed to `executeQuery`.
- Using `pattern-not`, it excludes patterns where parameterized queries are employed, which are considered safe practices.

### Resources
Refer to the documentation for more details on writing custom Semgrep rules and optimizations:
- **Writing custom rules**: Detailed guidance on writing effective custom rules  .
- **Common patterns**: Understanding pattern syntax and usage in various scenarios     .

By utilizing the provided guidelines and examples, you can create comprehensive Semgrep rules to detect potential SQL Injection vulnerabilities across different contexts and frameworks in Java.