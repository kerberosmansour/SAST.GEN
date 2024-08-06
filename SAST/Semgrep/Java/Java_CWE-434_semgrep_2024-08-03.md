BasedBased on the rules and practices for writing Semgrep SAST rules, Sherif Mansour, I have generated a custom Semgrep rule to detect the vulnerability of "Unrestricted Upload of File with Dangerous Type (CWE-434)" in Java. This rule covers common patterns where such vulnerabilities can exist, including in popular Java frameworks such as Spring MVC or plain servlets.

Here’s how the rule is structured:

```yaml
rules:
- id: java-cwe-434-unrestricted-file-upload
  patterns:
    - pattern-either:
        - pattern: |
            @RequestMapping(...)
            @ResponseBody
            public $RET $FUNC(HttpServletRequest $REQ, HttpServletResponse $RESP) {
                ...
                $FILE = $REQ.getFile(...);
                ...
                $FILE.transferTo(...);
                ...
            }
        - pattern: |
            public class $CLASS {
                public void doPost(HttpServletRequest $REQ, HttpServletResponse $RES) throws ServletException, IOException {
                    ...
                    Part $PART = $REQ.getPart(...);
                    ...
                    $PART.write(...);
                    ...
                }
            }
  message: "Potential CWE-434: Unrestricted file upload detected."
  severity: ERROR
  languages:
    - java
  metadata:
    cwe: "CWE-434"
    description: "Unrestricted Upload of File with Dangerous Type (CWE-434)."
```

### Explanation:
- **Patterns**: The rule uses `pattern-either` to match multiple variations of potentially dangerous file upload handling.
  - One pattern targets Spring MVC controllers using `@RequestMapping` and the `MultipartFile` API.
  - Another pattern targets Java Servlets using `HttpServletRequest.getPart` and `Part.write`.
- **Message and Severity**: The `message` and `severity` fields communicate that this is a critical issue.
- **Languages**: The rule is applied to Java code.

This Semgrep rule checks for potential file upload vulnerabilities by identifying common methods used for handling file uploads. It highlights the risk when the file's type or destination is not sufficiently validated or restricted    . 

Please feel free to run this rule against your codebase to detect and rectify any potential instances of this vulnerability.