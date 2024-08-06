ToTo write effective Semgrep SAST (Static Application Security Testing) rules for detecting Cross-Site Request Forgery (CSRF) (CWE-352) in JavaScript, we need to understand various ways in which CSRF vulnerabilities can manifest in popular JavaScript frameworks such as Node.js with Express, Angular, and React.

### Understanding CSRF

CSRF vulnerabilities occur when an attacker tricks a user into performing actions they do not intend to perform. This usually happens through maliciously crafted URLs or forms. Common patterns include lack of anti-CSRF tokens, insecure iframes, and improper validation.

### Key Points for Detection

1. **Lack of Anti-CSRF Token**: Detecting absence or misuse of CSRF tokens in forms or requests.
2. **Insecure XHR**: Detecting unprotected XMLHttpRequests.
3. **Improper Validation**: Forms and request handlers should validate incoming CSRF tokens.

### Semgrep Rule Skeleton

1. **Pattern**: Identify JavaScript code blocks related to form submission, request handling, etc.
2. **Conditions**: Ensure the presence of anti-CSRF tokens.
3. **Framework Adaptations**: Separate rules for Express, Angular, and React.

### Example Rules

#### Detecting CSRF Vulnerability in Express.js

```yaml
rules:
  - id: express-csrf
    languages: [javascript]
    message: Ensure that CSRF protection middleware is used.
    patterns:
      - pattern: |
          app.use(...);
      - metavariable-pattern:
          metavariable: $X
          patterns:
            - pattern-not: |
                csrf(...)
    severity: ERROR
```

This rule looks at Express.js middleware usage and ensures that middleware for CSRF protection is applied.

#### Angular Form Validation

```yaml
rules:
  - id: angular-csrf
    languages: [typescript]
    message: Ensure that CSRF tokens are validated in Angular forms.
    patterns:
      - pattern: |
          this.http.post(..., ...);
      - metavariable-pattern:
          metavariable: $X
          patterns:
            - pattern-not: |
                'X-CSRF-Token'
    severity: ERROR
```

This rule ensures that outgoing HTTP POST requests in Angular contain an `X-CSRF-Token` header.

#### React Application

```yaml
rules:
  - id: react-csrf
    languages: [javascript, typescript]
    message: Ensure that CSRF tokens are included in forms or fetch requests.
    patterns:
      - pattern: |
          fetch(...);
      - metavariable-pattern:
          metavariable: $X
          patterns:
            - pattern-not: |
                'X-CSRF-Token'
    severity: ERROR
```

This rule ensures that `fetch` requests in React applications properly include an `X-CSRF-Token`.

### Explanation and Variations

1. **Express.js**: Ensures middleware for CSRF protection like `csurf` is used.
2. **Angular**: Checks if headers include CSRF tokens for HTTP requests made using Angular's HttpClient.
3. **React**: Ensures CSRF tokens are used in API requests made via `fetch`.

### Further Customization

These rules should be tailored according to specific project needs:
- Adjust paths and filenames if dealing with a specific structure.
- Include more patterns and metavariables as needed to match additional variations.

### Conclusion

These sample rules provide a starting point for detecting CSRF vulnerabilities in the mentioned JavaScript frameworks. You can extend these rules further to cover more specific scenarios or other frameworks as per your project's requirements.

For more complex scenarios and optimizations, refer to the detailed rule-writing guides and practices from the Semgrep documentation【4:0†source】  .