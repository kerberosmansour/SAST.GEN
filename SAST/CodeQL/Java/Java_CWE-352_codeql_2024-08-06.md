###### Writing CodeQL Rules for Cross-Site Request Forgery (CSRF) (CWE-352) in Java

#### 1. Context Review:
To create CodeQL rules for CSRF detection in Java, one should become familiar with:
- The structure of `.ql` files.
- The use of metadata.
- QL constructs relevant for detecting CSRF.

CodeQL, the querying language used by CodeQL, provides capabilities for data flow analysis, taint tracking, and control flow analysis, which are critical for detecting security vulnerabilities like CSRF.

#### 2. Vulnerability Analysis:

**Cross-Site Request Forgery (CSRF) in Java**:
CSRF vulnerabilities arise when a malicious website can induce users to perform actions on another web application where they are authenticated. Common targets for CSRF include state-changing operations such as login, account modifications, etc. CSRF attacks typically exploit HTTP GET and POST requests.

**Manifestations Across Different Frameworks**:
1. **Spring MVC**:
   - HTTP endpoints that accept state-changing requests without validating anti-CSRF tokens.
2. **Struts**:
   - Actions performing state changes without any CSRF token validation.

**Common Coding Practices Leading to CSRF**:
- Forms without CSRF tokens.
- Absence of token validation in request handlers.

#### 3. CodeQL Rule Creation:

The rules should:
- Identify sources (points where data originating from HTTP requests enters the system).
- Define sinks (critical operations that leave the system, e.g., database operations).
- Track taint propagation from sources to sinks.
- Use predicates to define trusted sources and sinks.

**Sample Rule for Identifying CSRF Vulnerabilities in Spring MVC**:

```ql
import java
import semmle.code.java.dataflow.TaintTracking
import DataFlow::PathGraph

/**
 * Detects missing CSRF tokens in HTTP handlers
 */
class CsrfTaintTrackingConfig extends TaintTracking::Configuration {
  CsrfTaintTrackingConfig() { this = "CsrfTaintTrackingConfig" }

  override predicate isSource(DataFlow::Node source) {
    source.asExpr() instanceof Parameter and
    source.asExpr().(Parameter).getDeclaringCallable().hasAnnotation("org.springframework.web.bind.annotation.RequestMapping")
  }

  override predicate isSink(DataFlow::Node sink) {
    exists(Call c |
      c.getTarget().hasName("save", "update", "delete") and
      sink.asExpr() = c.getArgument(0)
    )
  }
}

from CsrfTaintTrackingConfig cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), "Potential CSRF vulnerability: Unprotected state-changing operation."
```

**Explanation**:
- `CsrfTaintTrackingConfig` defines sources as parameters from methods annotated with `@RequestMapping` (indicating they handle HTTP requests).
- Sinks are defined as calls to common state-changing methods (`save`, `update`, `delete`).

**Sanitizers**:
To reduce false positives, the rule should recognize legitimate CSRF protections:
```ql
class CsrfSanitizer extends TaintTracking::Sanitizer {
  CsrfSanitizer() { this = "CsrfSanitizer" }

  override predicate isSanitizer(DataFlow::Node node) {
    exists(Call c |
      c.getTarget().hasName("isCsrfValid", "validateCsrfToken") and
      node.asExpr() = c.getArgument(0)
    )
  }
}
```

#### 4. Testing and Validation:
Create test cases covering a variety of frameworks like Spring MVC and Struts.

**Testing in Spring MVC**:
```java
@Controller
public class ExampleController {
  @RequestMapping(value = "/update", method = RequestMethod.POST)
  public String update(@RequestParam("data") String data, HttpServletRequest request) {
    // Missing CSRF token validation
    updateData(data);
    return "success";
  }
}
```

**Testing**:
1. Create test scenarios with and without CSRF tokens.
2. Use CodeQL's query console or GitHub Code Scanning to scan real codebases.

**Validation**:
Run the rules against known vulnerable and non-vulnerable repositories to assess the precision (minimizing false positives) and recall (minimizing false negatives) of the custom CodeQL query.

Tools like the CodeQL query console can facilitate extensive testing and validation on diverse projects:
- Ensure the query identifies all known CSRF vulnerabilities.
- Verify no legitimate operations are flagged unless necessary CSRF validations are missing.

Incorporating CSRF-specific configurations and extending the query to recognize additional frameworks will ensure comprehensive coverage and higher accuracy.

**References**:
- Best practices for writing CodeQL rules【4:0†source】【4:1†source】.
- Handling of sinks and sources in CodeQL rules【4:0†source】【4:1†source】【4:5†source】.

These steps and queries provide a strong foundation for identifying CSRF vulnerabilities with minimal false positives and false negatives.