BasedBased on the context provided and the understanding of creating Semgrep SAST rules, here is an example set of rules to detect "Improper Certificate Validation (CWE-295) in Swift". This rule set covers various variations where improper certificate validation might occur, focusing on common Swift frameworks like `URLSession`, `NSURLConnection`, and `Alamofire`.

### Semgrep Rule for Improper Certificate Validation in Swift

```yaml
rules:
  - id: improper-certificate-validation-urlsession
    languages: [swift]
    message: "Improper certificate validation using URLSession"
    severity: ERROR
    patterns:
      - pattern: |
          let session = URLSession(configuration: .default, delegate: $DELEGATE, delegateQueue: nil)
      - pattern-sources:
          - pattern: |
              $DELEGATE.urlSession(_:didReceive:completionHandler:)
      - pattern-sinks:
          - pattern: |
              completionHandler(NSURLSession.AuthChallengeDisposition.useCredential, $CREDENTIAL)
    metadata:
      cwe: "CWE-295"
      description: "This rule detects improper certificate validation using URLSession by allowing any certificate without proper validation."
  
  - id: improper-certificate-validation-nsurlconnection
    languages: [swift]
    message: "Improper certificate validation using NSURLConnection"
    severity: ERROR
    patterns:
      - pattern: |
          func connection(_ connection: NSURLConnection, willSendRequestFor challenge: URLAuthenticationChallenge) {
              let credential = URLCredential($CREDENTIAL)
              challenge.sender?.use(credential, for: challenge)
          }
    metadata:
      cwe: "CWE-295"
      description: "This rule detects improper certificate validation using NSURLConnection."

  - id: improper-certificate-validation-alamofire
    languages: [swift]
    message: "Improper certificate validation using Alamofire"
    severity: ERROR
    patterns:
      - pattern: |
          let manager = Alamofire.SessionManager.default
          manager.delegate.sessionDidReceiveChallenge = { session, challenge in
              return (.useCredential, URLCredential(trust: challenge.protectionSpace.serverTrust!))
          }
    metadata:
      cwe: "CWE-295"
      description: "This rule detects improper certificate validation using Alamofire by allowing any certificate without proper validation."
```

### Explanation
1. **URLSession**:
   - This pattern looks for the creation of a `URLSession` with a delegate.
   - It checks the delegate's implementation of `urlSession(_:didReceive:completionHandler:)`.
   - The rule triggers if the challenge is completed without proper validation (using any credential).

2. **NSURLConnection**:
   - This pattern matches the `NSURLConnection` delegate method `connection(_:willSendRequestFor:)` to check if it uses credentials without proper validation.
   
3. **Alamofire**:
   - This pattern matches Alamofire's custom session manager where the delegate method `sessionDidReceiveChallenge` is implemented.
   - It specifically checks if the challenge is handled using `URLCredential(trust:)` without validating the server trust object.

By combining these patterns, we can capture common ways improper certificate validation may occur in Swift and popular frameworks, reducing false positives while ensuring we don't miss critical security issues.

### Usage
This rule set should be added to your Semgrep configuration to help identify and flag instances where improper certificate validation might occur in Swift projects. Make sure to test these rules in a controlled environment to refine them for your specific use case.

### References
- For additional information on writing Semgrep rules, please refer to the relevant parts of the documentation   .