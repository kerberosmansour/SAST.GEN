#### Secure Defaults and Recommendations for Mitigating Code Injection (CWE-094) in Java

### Secure Defaults and Remediation Code

To mitigate the risk of Code Injection vulnerabilities (CWE-094) in Java, it is critical to follow secure coding practices, validate all inputs, use secure libraries, and employ strong security controls. Here are detailed technical recommendations:

#### 1. Input Validation and Whitelisting

Always validate and sanitize user inputs. Restrict the allowed inputs to a well-defined set (whitelisting). Use input validation frameworks and libraries such as Apache Commons Validator or OWASP Java HTML Sanitizer.

```java
import org.apache.commons.lang3.StringUtils;

public class InputValidator {
    public static boolean isValidInput(String input) {
        // Define the allowed input patterns
        String allowedPattern = "^[a-zA-Z0-9]+$";
        return input != null && input.matches(allowedPattern);
    }

    public static void main(String[] args) {
        String userInput = "someInput";
        if (isValidInput(userInput)) {
            // proceed with business logic
        } else {
            // handle invalid input
        }
    }
}
```

#### 2. Avoiding Dynamic Code Execution

Never use `eval`, `Runtime.exec()`, or any similar methods to execute dynamically constructed code or commands. Instead, use safer APIs whenever possible.

**Insecure Code:**

```java
public void executeCommand(String command) {
    Runtime.getRuntime().exec(command); // Dangerous, potential code injection
}
```

**Secure Code:**

```java
public class SecureCommandExecutor {
    public static void execute(String command, String[] args) {
        if (command.equals("safeCommand") && InputValidator.isValidInput(args[0])) {
            ProcessBuilder pb = new ProcessBuilder(command, args);
            pb.start();
        } else {
            throw new IllegalArgumentException("Invalid command or arguments");
        }
    }

    public static void main(String[] args) {
        SecureCommandExecutor.execute("safeCommand", new String[]{"arg1"});
    }
}
```

#### 3. Using Prepared Statements

When dealing with database interactions, always use prepared statements with parameterized queries to prevent SQL injection.

**Insecure Code:**

```java
Statement stmt = connection.createStatement();
String query = "SELECT * FROM users WHERE username = '" + username + "'";
ResultSet rs = stmt.executeQuery(query);
```

**Secure Code:**

```java
PreparedStatement stmt = connection.prepareStatement("SELECT * FROM users WHERE username = ?");
stmt.setString(1, username);
ResultSet rs = stmt.executeQuery();
```

### Secure Library Recommendations

1. **OWASP Java Encoder**: Helps encode user data to prevent XSS and injection attacks.
2. **Hibernate Validator**: Provides annotation-based input validation in Java (useful for validating user inputs).
3. **Apache Commons Validator**: Provides a robust validation framework.
4. **OWASP Java HTML Sanitizer**: Sanitizes HTML to prevent XSS (especially useful if dealing with HTML content).

### Secure Configurations for Popular Java Frameworks

#### 1. Spring Framework

When using the Spring framework, secure your controllers and services by ensuring they are not exposed to unauthorized users.

**Insecure Code:**

```java
@DeleteMapping("/users/{id}")
public ResponseEntity<String> deleteUser(@PathVariable long id) {
    userService.deleteUser(id);
    return new ResponseEntity<>("User has been deleted!", HttpStatus.OK);
}
```

**Secure Code:**

```java
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/users/{id}")
public ResponseEntity<String> deleteUser(@PathVariable long id) {
    userService.deleteUser(id);
    return new ResponseEntity<>("User has been deleted!", HttpStatus.OK);
}
```

Employ security annotations like `@PreAuthorize` and ensure all endpoints are properly secured. Semgrep can be used to detect missing security annotations in Spring controllers.

#### Example Semgrep Rule to Detect Insecure Endpoints:

```yaml
rules:
  - id: spring-unauthenticated-route
    patterns:
      - pattern-inside: |
          @RestController
          class $CONTROLLER { ... }
      - pattern-inside: |
          @$MAPPING($ROUTE)
          $RET $METHOD(...) { ... }
      - metavariable-regex:
          metavariable: $MAPPING
          regex: (GetMapping|PostMapping|DeleteMapping|PutMapping|PatchMapping)
      - pattern-not: |
          @PreAuthorize(...)
          $METHOD(...) { ... }
    message: The route $ROUTE is exposed to unauthenticated users. Please verify this is expected behavior, otherwise add the proper authentication/authorization checks.
    languages:
      - java
    severity: WARNING
```

### Metadata for Semgrep Rules

Including metadata in Semgrep rules helps developers understand and address potential issues better:

```yaml
metadata:
  cwe: "CWE-94"
  confidence: "high"
  likelihood: "medium"
  impact: "high"
  subcategory: "vuln"
  author: "security-team@example.com"
```

**References:**
- Promoting secure alternatives like safe libraries and APIs  .
- Examples of Semgrep rule usage and metadata structure  .
- General concepts on detecting uninitialized routes in Spring   .

By following these practices and leveraging powerful tools like Semgrep for static analysis, you can significantly reduce the risks associated with code injection and other security vulnerabilities in your Java applications.