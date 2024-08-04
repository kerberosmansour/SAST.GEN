BasedBased on the guidelines and examples provided in 'Semgrep.output.md', here is a set of Semgrep SAST rules to detect the "Cleartext Transmission of Sensitive Information (CWE-319)" in JavaScript, including variations that might occur in popular frameworks:

```yaml
rules:
  - id: js-cleartext-transmission
    languages: [javascript]
    message: "Cleartext transmission of sensitive information"
    severity: ERROR
    patterns:
      - pattern: request({
          url: $URL,
          ...,
          secure: false,
          ...
        })
      - pattern: fetch($URL, { ..., secure: false, ..., })
      - pattern: $.ajax({
          url: $URL,
          ..., 
          secure: false, 
          ...
        })
      - pattern: $HTTP.get($URL, { ..., secure: false, ..., });
    metadata:
      cwe: "CWE-319"
      description: "Detects use of HTTP or insecure requests for URLs where 'secure: false' is explicitly set."
      owasp: "A6:2021"

  - id: js-insecure-url
    languages: [javascript]
    message: "Cleartext transmission of sensitive information using HTTP"
    severity: ERROR
    patterns:
      - pattern: request({ url: /^http:/, ... })
      - pattern: fetch(/^http:\/\//, ...)
      - pattern: $.ajax({ url: /^http:\/\//, ... })
      - pattern: $HTTP.get(/^http:/, ...)
    metadata:
      cwe: "CWE-319"
      description: "Detects use of insecure HTTP for transmitting sensitive data."
      owasp: "A6:2021"

  - id: js-insecure-websockets
    languages: [javascript]
    message: "Cleartext transmission of sensitive information over ws://"
    severity: ERROR
    patterns:
      - pattern: new WebSocket('ws://...')
      - pattern: var $WS = new WebSocket('ws://...');
    metadata:
      cwe: "CWE-319"
      description: "Detects use of insecure WebSocket connections."
      owasp: "A6:2021"

  - id: js-axios-insecure
    languages: [javascript]
    message: "Cleartext transmission of sensitive information using Axios"
    severity: ERROR
    patterns:
      - pattern: axios.get(/^http:/, ...)
      - pattern: axios.post(/^http:/, ...)
      - pattern: axios.request({ url: /^http:/, ... })
    metadata:
      cwe: "CWE-319"
      description: "Detects use of insecure HTTP requests with Axios."
      owasp: "A6:2021"
```

These rules identify critical instances where sensitive information might be transmitted over cleartext channels or using insecure configurations. The rules include:

1. **General Request Patterns**: Identifying insecure usage in various libraries and frameworks.
2. **Insecure URL Pattern**: Detects URLs starting with `http://` which is not secure.
3. **Insecure WebSocket Pattern**: Identifying WebSocket connections using `ws://`.
4. **Axios Specific Rule**: To catch insecure requests made using Axios.

These patterns cover variations in how the vulnerabilities might be introduced in JavaScript applications using different mechanisms and popular libraries.

### References
Adapted from provided methodologies and examples in the Semgrep documentation【4:0†source】     .