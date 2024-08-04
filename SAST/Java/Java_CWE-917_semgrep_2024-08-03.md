ToTo create a Semgrep SAST rule for detecting "Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')" (CWE-917) in Java, you need to consider common scenarios in popular frameworks like Spring.

Here's an example of such a rule:

```yaml
rules:
  - id: expression-language-injection
    patterns:
      - pattern: |
          ${$VAR}
      - pattern: |
          <c:set var="$VAR" value="${...}" />
      - pattern: |
          render(${...})
    message: Potential Expression Language Injection (CWE-917)
    languages:
      - java
    severity: ERROR
    metadata:
      category: security
      cwe: CWE-917
```

This rule aims to match cases where untrusted input is evaluated by an expression language engine, which is a common scenario for EL injection vulnerabilities.

### Explanation:
1. **Patterns**: These patterns are looking for different ways expressions can be interpolated in JSP/EL context, for instance using `${...}` constructs, which are commonly exploited in EL injections.
2. **Metavariables**: Use `$VAR` and `...` to generalize the patterns. This helps in identifying various forms of injection points.
3. **Severity**: Set to `ERROR` to highlight the critical nature of this finding.

This is a simplified version, and you might need to extend it to cover all variations and specific contexts in your application. Make sure to test the rule thoroughly in the Semgrep playground and on your codebase to ensure it detects all potential issues correctly.

Consider using additional Semgrep features like `metavariable-pattern`, `metavariable-comparison`, `pattern-inside`, and `pattern-not-inside` for more complex rules and better accuracy【4:0†source】【4:7†source】【4:9†source】 .