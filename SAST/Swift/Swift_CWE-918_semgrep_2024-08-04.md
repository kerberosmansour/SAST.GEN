BasedBased on the provided document on how to write Semgrep rules, here is a set of Semgrep SAST rules designed to detect Server-Side Request Forgery (SSRF) vulnerabilities in Swift across various frameworks. These rules are intent on achieving high detection accuracy with high false negatives and low false positives:

### Semgrep Rules for SSRF in Swift

#### Generic SSRF Pattern

```yaml
rules:
  - id: ssrf-urlsession
    languages: [swift]
    message: "Potential SSRF via URLSession"
    severity: ERROR
    patterns:
      - pattern: |
          URLSession.shared.dataTask(with: URL(string: $URL)!)
      - pattern-scope: $URL
        patterns:
          - pattern-not: "fixedURL"
    metadata:
      cwe: "CWE-918"
      owasp: "A10:2019"
```

#### Alamofire Framework

```yaml
rules:
  - id: ssrf-alamofire
    languages: [swift]
    message: "Potential SSRF via Alamofire"
    severity: ERROR
    patterns:
      - pattern: |
          AF.request($URL, ...)
      - pattern-scope: $URL
        patterns:
          - pattern-not: "fixedURL"
    metadata:
      cwe: "CWE-918"
      owasp: "A10:2019"
```

#### URLRequest with a Custom URL

```yaml
rules:
  - id: ssrf-urlrequest
    languages: [swift]
    message: "Potential SSRF via URLRequest"
    severity: ERROR
    patterns:
      - pattern: |
          let request = URLRequest(url: URL(string: $URL)!)
      - pattern-scope: $URL
        patterns:
          - pattern-not: "fixedURL"
    metadata:
      cwe: "CWE-918"
      owasp: "A10:2019"
```

#### Custom URL Sessions

```yaml
rules:
  - id: ssrf-custom-urlsession
    languages: [swift]
    message: "Potential SSRF via custom URLSession"
    severity: ERROR
    patterns:
      - pattern: |
          let session = URLSession(configuration: ...)
          session.dataTask(with: URL(string: $URL)!)
      - pattern-scope: $URL
        patterns:
          - pattern-not: "fixedURL"
    metadata:
      cwe: "CWE-918"
      owasp: "A10:2019"
```

### Explanation

1. **Metavariables and Nested Patterns**: These rules utilize metavariables to capture dynamic URL parameters which may be vulnerable to SSRF【4:1†source】【4:2†source】【4:3†source】【4:4†source】. By including `pattern-not` inside `pattern-scope`, we ensure that hardcoded URLs like `fixedURL` are excluded to reduce false positives.

2. **Specific Frameworks**: Specific rules for `URLSession`, `Alamofire`, and `URLRequest` are written to capture variations in how these frameworks handle URL requests【4:2†source】【4:3†source】【4:4†source】【4:10†source】.

3. **Severity and Metadata**: Each rule is tagged with a severity level and relevant metadata, including the CWE identifier and OWASP category, for better tracking and categorization【4:9†source】【4:10†source】.

4. **Custom URL Sessions**: Custom URL sessions are addressed with a separate rule to ensure that even non-standard usage patterns are caught【4:10†source】【4:12†source】.

These rules should provide a comprehensive initial set to detect SSRF vulnerabilities in Swift applications, particularly focusing on URL handling across different contexts and commonly used frameworks.