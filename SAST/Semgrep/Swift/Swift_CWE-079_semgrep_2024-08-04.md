ToTo create Semgrep SAST rules for detecting Cross-site Scripting (XSS) vulnerabilities (CWE-079) in Swift, you should leverage the concepts like `patterns`, `metavariable-patterns`, and `pattern-either` for comprehensive and precise detection.

### Semgrep SAST Rule Example for XSS in Swift

The following example constructs a set of rules for identifying potential XSS vulnerabilities in Swift, covering different frameworks and variations to maintain a balance of low false positives and false negatives.

#### Rule Structure:

1. **Direct Usage of Unsafe APIs (UIWebView, WKWebView etc.)**
2. **Unencoded Output in Templates (e.g., Vapor's Leaf templates)**

### 1. Detect Unsafe APIs

**ID:** swift-xss-webview

```yaml
rules:
  - id: swift-xss-webview
    languages: [swift]
    message: "Potential XSS vulnerability: Usage of UIWebView or WKWebView without proper input sanitization"
    severity: ERROR
    patterns:
      - pattern-either:
          - pattern: |
              let $WEBVIEW = ... as? UIWebView
              ...
              $WEBVIEW.loadHTMLString($HTML, baseURL: ...)
          - pattern: |
              let $WEBVIEW = ... as? WKWebView
              ...
              $WEBVIEW.loadHTMLString($HTML, baseURL: ...)
    metadata:
      cwe: CWE-079
      owasp: A7
    severity: WARNING
    patterns:
      - pattern-either:
        - pattern: |
             [$WEBVIEW loadHTMLString:$HTML baseURL:$BASEURL];
        - pattern: |
             let $WEBVIEW = WKWebView()
             webView.loadHTMLString($HTML, baseURL: $BASEURL)    
```

### 2. Detect Unencoded Output in Templates

**ID:** swift-xss-leaf-template

```yaml
rules:
  - id: swift-xss-leaf-template
    languages: [swift]
    message: "Potential XSS vulnerability: Unencoded output in Leaf template"
    severity: ERROR
    pattern: |
      try render($TEMPLATE, $CONTEXT)
      ...
      $TEMPLATE = "<html>\($USERINPUT)</html>"
    metadata:
      cwe: CWE-079
      owasp: A7
    severity: ERROR    
```

### Explanation and Coverage:

1. **WebView XSS:** Detects instances where an HTML string is directly loaded into a `UIWebView` or `WKWebView` without input sanitization.
2. **Template XSS:** Detects instances where unencoded user input is embedded directly into HTML in Vapor's Leaf templates.

#### Additional Checks:

You can add further patterns for other frameworks or different variations of unsafe HTML rendering to extend detection coverage.

### Tips for Writing Effective Semgrep Rules:

1. **Pattern-Specific Metadata:** Use to provide more context and improve rule management.
2. **Patterns Inside Patterns:** Useful to specify context and reduce false positives.
3. **Regular Testing in Semgrep Playground:** For refining and ensuring rules cover all use cases.

For more detailed steps and additional examples on writing and optimizing Semgrep rules, refer to the official documentation and tutorials:
- [Semgrep Documentation](https://semgrep.dev/docs/writing-rules/)
- [Semgrep Playground](https://semgrep.dev/playground)

By leveraging these guidelines, you ensure your SAST rules effectively detect XSS vulnerabilities in Swift applications while minimizing false positives and negatives   .