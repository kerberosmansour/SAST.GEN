###### Writing Semgrep SAST Rules for "Cleartext Transmission of Sensitive Information (CWE-319)" in Swift

Based on the guidelines and examples from your provided context, let's write a set of Semgrep SAST rules to cover the vulnerability of cleartext transmission of sensitive information in Swift. This involves creating rules that identify instances where sensitive information might be transmitted without encryption across various popular frameworks.

#### Basic Rule Structure

1. **Setup Basic Rule Properties**

```yaml
rules:
  - id: cwe-319-cleartext-transmission
    languages: [swift]
    message: "Cleartext transmission of sensitive information"
    severity: ERROR
    patterns:
```

2. **Identify Insecure Transfer Functions**

- Check for usage of URLSession without HTTPS
- Validate the use of WebSockets (NSURLSession)
- Ensure sensitive headers or parameters are not sent via HTTP

3. **Common Vulnerable Patterns**

- URLSession data tasks or web sockets connecting to non-secure URLs (http:// instead of https://)
- Transmission of sensitive headers (e.g., Authorization, API Keys) over HTTP

#### Detailed Rule Examples

**Pattern 1: URLSession Data Tasks with HTTP URLs**

```yaml
rules:
  - id: cleartext-urlsession-datatask
    languages: [swift]
    message: "Sensitive data transmitted over HTTP via URLSession"
    severity: ERROR
    patterns:
      - pattern: URLSession.shared.dataTask(with: URL(string: "$URL")!)
      - metavariable-comparison:
          metavariable: $URL
          comparison: $URL.startswith("http:")
```

**Pattern 2: WebSocket Connections to HTTP URLs**

```yaml
rules:
  - id: cleartext-websocket
    languages: [swift]
    message: "Sensitive data transmitted over an unencrypted WebSocket connection"
    severity: ERROR
    patterns:
      - pattern: URL(string: "$URL")
      - metavariable-comparison:
          metavariable: $URL
          comparison: $URL.startswith("ws:")
```

**Pattern 3: Sensitive Headers in HTTP Requests**

```yaml
rules:
  - id: sensitive-headers-http
    languages: [swift]
    message: "Sensitive headers sent over HTTP"
    severity: ERROR
    patterns:
      - pattern: URLRequest(url: URL(string: "$URL")!)
      - metavariable-pattern:
          metavariable: $URL
          patterns:
            - pattern: |
                http://
      - pattern-inside: |
          request.setValue($VALUE, forHTTPHeaderField: $HEADER)
      - metavariable-pattern:
          metavariable: $HEADER
          patterns:
            - pattern: Authorization
            - pattern: ApiKey
            - pattern: X-Api-Key
```

In these rules:
- The patterns match specific code patterns in Swift where URLSession, WebSocket, or URLRequest are used.
- Metavariables (`$URL`, `$HEADER`) are used to capture parts of the code and apply further conditions.
- `metavariable-comparison` and `metavariable-pattern` are used to ensure that the captured URL starts with "http:" or the header field contains sensitive information.

These rules help ensure that sensitive information is not transmitted in an unencrypted manner, thereby maintaining the security and privacy of data transmitted by the application.

### Sources
Here are the relevant parts and principles used from the context to create these rules:

- **Metavariables and Comparisons**: Used for holding specific values and conditions.
- **Pattern Inside**: Ensures context-specific matches (e.g., headers are checked inside the URLRequest context).
- **Pattern Examples**: Adapted from provided examples to fit the new context of Swift【4:0†source】【4:1†source】【4:2†source】【4:3†source】 .

This approach ensures that our Semgrep rules identify variations of CWE-319 vulnerability with high specificity and low false positives.