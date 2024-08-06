ToTo write Semgrep SAST rules and cover the vulnerability of Cross-Site Request Forgery (CSRF) (CWE-352) in Java, you can create a Semgrep rule to detect patterns across popular Java frameworks like Spring.

Here's an example Semgrep rule to detect CSRF vulnerability in a Spring application where CSRF protection might be disabled. This rule will help identify cases where `@EnableWebSecurity` and `csrf().disable()` or other similar configurations are improperly set.

### Semgrep Rule Example for CSRF (CWE-352):

```yaml
rules:
  - id: spring-disable-csrf
    patterns:
      - pattern-inside: |
          @Configuration
          @EnableWebSecurity
          public class $CLASS_NAME extends WebSecurityConfigurerAdapter {
            @Override
            protected void configure(HttpSecurity http) throws Exception {
              ...
              $DISABLE_CSRF_CALL
              ...
            }
      - metavariable-pattern:
          metavariable: $DISABLE_CSRF_CALL
          pattern: |
            http.csrf().disable()
    message: "CSRF protection is disabled in the Web Security configuration."
    languages: [java]
    severity: WARNING
```

### Explanation:
- **id**: A unique identifier for the rule.
- **patterns**: This section combines several patterns using logical AND to identify the vulnerable code structure.
  - **pattern-inside**: This pattern ensures the check is inside a class annotated with `@Configuration` and `@EnableWebSecurity`.
  - **metavariable-pattern**: This ensures that inside the `configure` method, there's a call to `http.csrf().disable()`.
- **message**: Provides a message explaining the issue detected.
- **languages**: Specifies that this rule applies to Java.
- **severity**: Indicates the severity level of the detected issue.

Using the above rule, Semgrep will search for any Spring Security configuration class that disables CSRF protection, which is a common CSRF vulnerability point.

### Usage:
To use this rule with Semgrep, save it into a file (e.g., `spring_disable_csrf.yaml`) and run Semgrep with this config:

```bash
semgrep --config spring_disable_csrf.yaml /path/to/your/java/code
```

This will scan your Java codebase and report places where `http.csrf().disable()` is used, indicating potential CSRF vulnerabilities.

For more detailed guidance on writing Semgrep rules, you can refer to the Semgrep documentation     .