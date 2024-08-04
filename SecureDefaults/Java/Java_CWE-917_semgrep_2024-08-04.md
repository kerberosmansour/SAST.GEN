###### Secure Defaults, Remediation Code, and Library Recommendations for Java Expression Language Injection (CWE-917)

#### Overview

Expression Language (EL) injection happens when user-controllable data is used in an expression language statement without proper validation and escaping. This can lead to unauthorized access, data exposure, or code execution. Below are detailed recommendations to mitigate EL Injection in Java applications, with a focus on popular frameworks.

---

### General Recommendations

1. **Input Validation and Sanitization:**
   - Always validate and sanitize user inputs.
   - Use a well-known validation library like Apache Commons Validator.

2. **Safe Expression Evaluation:**
   - Avoid evaluating user inputs directly in expressions.
   - Use safe methods or libraries to handle expressions.

3. **Least Privilege:**
   - Run applications with the least privileges necessary.

4. **Security-focused Libraries:**
   - Use libraries providing built-in protection against EL injection.

---

### Secure Defaults and Remediation Code

#### Spring Framework

**Problematic Usage:**
```java
import org.springframework.web.bind.annotation.*;
import javax.servlet.http.*;

@RestController
public class ExampleController {

    @GetMapping("/evaluate")
    public String evaluate(@RequestParam String expression, HttpServletRequest request) {
        // Dangerous: directly using user input in an expression
        return evaluateExpression(expression);
    }

    private String evaluateExpression(String expr) {
        // Some complex EL evaluation logic
        return expr; 
    }
}
```

**Secure Version:**
```java
import org.springframework.web.bind.annotation.*;
import org.springframework.expression.spel.standard.*;
import org.springframework.expression.spel.support.StandardEvaluationContext;

@RestController
public class ExampleController {

    @GetMapping("/evaluate")
    public String evaluate(@RequestParam String expression, HttpServletRequest request) {
        // Safely evaluate the expression
        return safeEvaluateExpression(expression);
    }

    private String safeEvaluateExpression(String expr) {
        StandardEvaluationContext context = new StandardEvaluationContext();
        SpelExpressionParser parser = new SpelExpressionParser();

        // Whitelist allowed fields/methods
        parser.getEvaluationContext().setPropertyAccessors(new LimitedPropertyAccessor());
        return parser.parseExpression(expr).getValue(context, String.class);
    }
}
```

**Explanation:**
- Use SpelExpressionParser but limit access to properties using a custom `LimitedPropertyAccessor`.

---

#### JSF (JavaServer Faces)

**Problematic Usage:**
```xhtml
<h:outputText value="#{request.getParameter('input')}" />
```

**Secure Version:**
```xhtml
<h:outputText value="#{secureBean.processedInput}" />
```
```java
import javax.faces.bean.ManagedBean;
import javax.faces.context.FacesContext;

@ManagedBean
public class SecureBean {
    public String getProcessedInput() {
        String input = FacesContext.getCurrentInstance().getExternalContext().getRequestParameterMap().get("input");
        // Apply input validation/sanitization logic here
        return sanitizeInput(input);
    }

    private String sanitizeInput(String input) {
        // Whitelist-based sanitation
        return input.replaceAll("[^\\w\\s]", "");
    }
}
```

**Explanation:**
- SecureBean manages input sanitization and ensures inputs are sanitized before evaluation.

---

### Library Recommendations

1. **Expression Language:**
   - Use **Apache Commons JEXL** instead of raw evaluation methods.
   - **SpEL (Spring Expression Language)** with explicit context control and restricted evaluation.

2. **Input Sanitation and Validation:**
   - **OWASP Java Encoder**: Ensures outputs are correctly escaped.
   - **ESAPI (Enterprise Security API)**: Offers comprehensive input validation and encoding.

3. **General Security Libraries:**
   - **Apache Shiro**: Ensures overall application security.
   - **Spring Security**: Comprehensive security services for enterprise applications.

---

### Example Semgrep Rule for Detection

**Usage:**
```yaml
rules:
  - id: expression-language-injection
    pattern-either:
      - pattern: |
          ${...}
      - pattern: |
          *<%= ... %>*
    message: "Potential EL Injection"
    languages:
      - java
      - jsp
    severity: ERROR
    metadata:
      cwe: "CWE-917"
      confidence: "high"
      likelihood: "medium"
      impact: "high"
```

**Explanation:**
- Detects common expression patterns indicating possible EL injection risks.

---

### Additional Tips

- **Education and Awareness:** Train developers on secure coding practices and dangers of EL injection.
- **Code Reviews and SAST:** Regularly perform code reviews and use Static Application Security Testing (SAST) tools, such as Semgrep, to identify vulnerabilities.

By following these guidelines, you can significantly reduce the risk of Expression Language Injection vulnerabilities in your Java applications while ensuring a good developer experience with high false negative and low false positive rates【4:0†source】【4:1†source】【4:2†source】【4:3†source】【4:7†source】【4:8†source】【4:9†source】【4:11†source】【4:13†source】【4:16†source】【4:18†source】.