BasedBased on the details you provided and the examples from the context, here are simplified Semgrep SAST rules for identifying CSRF vulnerabilities in Swift. These rules aim to cover common patterns for CSRF vulnerabilities in popular Swift frameworks.

### Semgrep Rule for Detecting CSRF Vulnerability in Swift

1. **Basic Rule for Swift's URLSession**

CSRF vulnerabilities often involve HTTP requests without proper CSRF token validation. Here is a basic rule to detect such patterns in `URLSession`:

```yaml
rules:
  - id: csrf-detection-urlsession
    patterns:
      - pattern: |
          let $VAR = URLSession.shared.dataTask(with: $REQUEST)
      - pattern-either:
          - pattern-not: |
              $TASK.resume()
          - pattern-inside:
              - pattern: |
                  $REQUEST.addValue("X-CSRF-Token", forHTTPHeaderField: "X-CSRF-Token")
    message: HTTP request without CSRF protection.
    severity: WARNING
    languages: [swift]
```

2. **Advanced Rule for Alamofire**

Alamofire is a popular HTTP networking library for Swift. Here’s a rule for detecting POST requests using Alamofire without CSRF token validation:

```yaml
rules:
  - id: csrf-detection-alamofire
    patterns:
      - pattern: |
          AF.request($URL, method: .post, parameters: $PARAMS, encoding: JSONEncoding.default)
      - pattern-either:
          - pattern-not: |
              $REQUEST.headers = ["X-CSRF-Token": $TOKEN]
          - pattern-inside:
              - pattern: |
                  .validate(statusCode: 200..<300)
    message: POST request via Alamofire without CSRF token.
    severity: WARNING
    languages: [swift]
```

3. **Metavariable Pattern for Custom CSRF Headers**

This rule helps in identifying metavalues used without CSRF headers in custom network requests:

```yaml
rules:
  - id: csrf-detection-custom
    patterns:
      - pattern: |
          let $VAR = URLRequest(url: $URL)
      - pattern-not: |
          $VAR.setValue("X-CSRF-Token", forHTTPHeaderField: "X-CSRF-Token")
      - metavariable-pattern:
          metavariable: $VAR
          patterns:
            - pattern-either:
                - pattern: |
                    $VAR.httpMethod = "POST"
                - pattern: |
                    $VAR.httpMethod = "PUT"
    message: Custom URLRequest without CSRF token.
    severity: WARNING
    languages: [swift]
```

By using these rules, you should be able to detect various patterns of CSRF vulnerabilities in Swift code, covering both in-built `URLSession` and popular networking libraries like Alamofire. The goal is to minimize false negatives while reducing false positives through smart pattern usage and metavariable comparisons.

These details and example patterns are adapted from the information drawn from the Semgrep documentation on writing rules and various pattern examples provided【4:0†source】【4:1†source】【4:2†source】【4:3†source】【4:4†source】.