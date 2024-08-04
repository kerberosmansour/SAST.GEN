ToTo effectively mitigate and prevent Command Injection (CWE-077) vulnerabilities in Java applications, developers should adopt secure defaults and remediation code. Recommendations also include using secure libraries that help in sanitizing inputs and preventing injection attacks. Here are guidelines and secure defaults that aim for a high developer experience while maintaining low false negative and positive rates:

### Variations in Vulnerability Contexts
Command injection vulnerabilities can occur in numerous ways across Java applications, including but not limited to:
- Usage of `Runtime.getRuntime().exec()`
- Usage of `ProcessBuilder`
- SQL queries constructed with user input
- Shell scripts or other command line utilities invoked with user input

### Secure Defaults
1. **Use Parameterized Input**:
    - Always use parameterized input for commands, SQL queries, and other user inputs to prevent injection attacks.
    
    ```java
    ProcessBuilder pb = new ProcessBuilder("/bin/sh", "-c", sanitizedCommand);
    Process p = pb.start();
    ```
    
2. **Sanitize Input**:
    - Ensure that user inputs are sanitized to remove or escape dangerous characters.

    ```java
    public static String sanitizeInput(String input) {
        return input.replaceAll("[^a-zA-Z0-9]", ""); // Adjust regex based on requirements
    }
    ```

3. **Whitelisting**:
    - Use whitelisting for input validation. This is safer compared to blacklisting since new dangerous patterns might not be captured by blacklists.
    
    ```java
    public static String whitelistInput(String input) {
        if(input.matches("[a-zA-Z0-9]+")) {
            return input;
        } else {
            throw new IllegalArgumentException("Invalid input!");
        }
    }
    ```

4. **Least Privilege**:
    - Run commands under the minimum necessary privilege level. Avoid running as root or administrator.

### Remediation Code Example
To prevent command injection using Java's `ProcessBuilder`, you can encapsulate potentially dangerous inputs and ensure proper validation and sanitization:

```java
import java.util.List;

public class SafeCommandExecutor {

    public static void executeCommand(String userInput) throws Exception {
        String safeInput = sanitizeInput(userInput);
        List<String> commands = List.of("/bin/sh", "-c", safeInput);
        
        ProcessBuilder processBuilder = new ProcessBuilder(commands);
        processBuilder.environment().put("SOME_VAR", "VALUE"); // Secure environment settings
        
        Process process = processBuilder.start();
        // Handle process input/output accordingly
    }

    private static String sanitizeInput(String input) {
        if (input == null) {
            throw new IllegalArgumentException("Input cannot be null.");
        }
        return input.replaceAll("[^a-zA-Z0-9]", ""); // Allow only alphanumeric characters
    }
}
```

### Secure Library Recommendations
- **OWASP Java Encoder Project**:
    - Use the OWASP security libraries to encode and sanitize input. The OWASP Encoder can be used to escape characters:
    ```java
    import org.owasp.encoder.Encode;

    String safeInput = Encode.forJava(userInput);
    ```

- **Apache Commons Text**:
    - For string escaping and handling special characters securely:
    ```java
    import org.apache.commons.text.StringEscapeUtils;

    String safeInput = StringEscapeUtils.escapeJava(userInput);
    ```

### Semgrep Rules for Detection
Use Semgrep (static analysis tool) to detect occurrences of potential command injections and ensure code safety proactively:
```yaml
rules:
  - id: command-injection-detection
    patterns:
      - pattern: |
          ProcessBuilder pb = new ProcessBuilder($COMMAND);
      - pattern-either:
          - pattern-regex: .*(\$.*\$.*)
          - pattern-regex: .*\${.*}.* # Detects command expansions
    message: Avoid using unsanitized user input in command executions.
    languages: [java]
    severity: ERROR
```
This Semgrep rule highlights potential risky calls to `ProcessBuilder` containing user input which might be unsafe.

### Conclusion

By adopting these secure coding practices, including whitelisting, sanitizing inputs, appropriately using libraries, and leveraging static analysis tools like Semgrep, Java developers can significantly reduce the risk of Command Injection vulnerabilities in their applications. Combining these practices ensures a high level of security with minimal disruption to the development workflow.

【4:0†Semgrep.output.md】