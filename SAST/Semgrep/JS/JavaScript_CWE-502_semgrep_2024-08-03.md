ToTo create a set of Semgrep Static Application Security Testing (SAST) rules for detecting Deserialization of Untrusted Data (CWE-502) in JavaScript, the following rules will cover this vulnerability and its variations across popular JavaScript frameworks like Express.js, Angular, and basic JavaScript.

### Rule 1: Basic JavaScript Deserialization with `eval`
This rule targets plain JavaScript code that uses `eval`, which can evaluate and potentially execute untrusted data.

```yaml
rules:
  - id: js-eval-deserialization
    languages: [javascript]
    message: "Deserialization of untrusted data using eval can lead to Remote Code Execution."
    severity: ERROR
    patterns:
      - pattern: |
          eval($UNTRUSTED_INPUT)
```

### Rule 2: `JSON.parse` on Untrusted Data
This rule targets scenarios where `JSON.parse` is applied to potentially untrusted input, representing a common pattern of deserialization.

```yaml
rules:
  - id: js-json-parse-deserialization
    languages: [javascript]
    message: "Deserialization of untrusted data using JSON.parse can lead to security vulnerabilities."
    severity: WARNING
    patterns:
      - pattern: |
          JSON.parse($UNTRUSTED_INPUT)
```

### Rule 3: Angular `HttpClient` with `responseType` as JSON
This rule targets Angular applications where deserialization can occur via the HTTP client with a JSON response type.

```yaml
rules:
  - id: angular-httpclient-json-deserialization
    languages: [javascript, typescript]
    message: "Deserialization of untrusted data using Angular HttpClient with responseType as 'json' can be risky."
    severity: WARNING
    patterns:
      - pattern: |
          this.httpClient.get($URL, { responseType: 'json' })
```

### Rule 4: Express.js `bodyParser`
This rule targets Express.js middleware `bodyParser` used for parsing JSON bodies from HTTP requests, which could be untrusted.

```yaml
rules:
  - id: expressjs-bodyparser-deserialization
    languages: [javascript]
    message: "Deserialization of untrusted data using bodyParser can lead to security vulnerabilities."
    severity: ERROR
    patterns:
      - pattern-inside: |
          app.use(...);
      - metavariable-pattern:
          metavariable: $X
          patterns:
            - pattern-not: |
                $X.json()
```

### How to Use These Rules
Save each of the above YAML snippets in a `.yml` file, then you can run Semgrep as follows:

```bash
semgrep --config PATH_TO_YOUR_RULES.yml PATH_TO_YOUR_CODE/
```

Each of these rules leverages the powerful matching capabilities of Semgrep, including pattern matching, metavariables, and `pattern-inside` constructs to detect usages of deserialization that could lead to security issues.

For further enhancements, refer to the detailed Semgrep documentation on crafting custom rules and patterns【4:0†source】 .