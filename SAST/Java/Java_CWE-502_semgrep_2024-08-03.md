BasedBased on the guidelines and examples provided for writing Semgrep SAST (Static Application Security Testing) rules, here is a custom Semgrep rule for detecting the deserialization of untrusted data (CWE-502) in Java within different frameworks:

```yaml
rules:
  - id: deserialization-of-untrusted-data
    languages: [java]
    message: "Potential deserialization of untrusted data. Avoid deserializing data from untrusted sources to prevent security vulnerabilities."
    severity: ERROR
    patterns:
      - pattern: |
          ObjectInputStream ois = new ObjectInputStream($INPUT);
          $OBJECT = ($CAST) ois.readObject();
      - metavariable-pattern:
          metavariable: $INPUT
          patterns:
            - pattern-either:
                - pattern: SocketInputStream
                - pattern: ServletInputStream
                - pattern: FileInputStream
                - pattern: ByteArrayInputStream
    metadata:
      cwe: "CWE-502"
      owasp: "A8:2017-Insecure Deserialization"
    examples:
      - code: |
          import java.io.FileInputStream;
          import java.io.ObjectInputStream;
          
          public class Main {
              public static void main(String[] args) {
                  try {
                      FileInputStream fileIn = new FileInputStream("data.ser");
                      ObjectInputStream in = new ObjectInputStream(fileIn);
                      Object obj = in.readObject();
                      in.close();
                      fileIn.close();
                  } catch (Exception e) {
                      e.printStackTrace();
                  }
              }
          }
        message: "Avoid deserialization of untrusted data using FileInputStream"
        result: ERROR
      - code: |
          import java.io.ByteArrayInputStream;
          import java.io.ObjectInputStream;
          
          public class Main {
              public static void main(String[] args) {
                  try {
                      byte[] data = "some data".getBytes();
                      ByteArrayInputStream byteIn = new ByteArrayInputStream(data);
                      ObjectInputStream in = new ObjectInputStream(byteIn);
                      Object obj = in.readObject();
                      in.close();
                      byteIn.close();
                  } catch (Exception e) {
                      e.printStackTrace();
                  }
              }
          }
        message: "Avoid deserialization of untrusted data using ByteArrayInputStream"
        result: ERROR
```

### Explanation and Application:

1. **Pattern Matching**:
   - The rule looks for common scenarios where deserialization is performed using `ObjectInputStream`.
   - It checks the patterns where an `ObjectInputStream` is created over various input streams like `SocketInputStream`, `ServletInputStream`, `FileInputStream`, and `ByteArrayInputStream`.

2. **Severity**: 
   - The severity is set to `ERROR` indicating that this is a high-priority security issue.

3. **Message**:
   - The message explains the potential risk and advises avoiding deserialization of untrusted data.

4. **Metadata**:
   - The metadata includes the relevant CWE (Common Weakness Enumeration) identifier and OWASP (Open Web Application Security Project) reference, enhancing the rule’s traceability and aligning it with widely recognized security standards.

5. **Examples**:
   - Examples provided under the `examples` section show the context where the deserialization might be misused, and how those instances will be flagged by the rule.

### Steps to Implement the Rule:

1. Save the YAML configuration for the rule into a file, e.g., `cwe-502-deserialization.yaml`.
2. Run the rule using Semgrep:
   ```bash
   semgrep --config cwe-502-deserialization.yaml
   ```
3. Review the findings in the codebase and take appropriate action.

This rule helps in flagging situations where deserialization of untrusted data may occur in Java applications, helping developers to proactively secure their code against such vulnerabilities【4:0†source】.