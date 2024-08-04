BasedBased on the context gathered from the uploaded file, here is a set of Semgrep SAST rules for detecting the **"Improper Link Resolution Before File Access (Link Following)" (CWE-059) in JavaScript**. This rule will cover various popular frameworks and scenarios.

### Semgrep SAST Rule for CWE-059 in JavaScript

```yaml
rules:
  - id: improper-link-resolution-before-file-access
    patterns:
      - pattern-either:
          # Basic filesystem access example
          - pattern: |
              fs.readFileSync($PATH, ...)
          # Express.js file access vulnerability
          - pattern: |
              app.get('/retrieve', (req, res) => {
                let filePath = req.query.path;
                fs.readFileSync(filePath, ...);
              });
          # HTTP file serving
          - pattern: |
              http.createServer((req, res) => {
                let filePath = url.parse(req.url).pathname;
                fs.readFileSync(filePath, ...)
              });
    severity: ERROR
    message: "Improper Link Resolution Before File Access leading to potential link following vulnerability (CWE-059)"
    languages: [javascript]
```

### Explanation
1. **Basic Filesystem Access:**
    - This pattern detects unsafe use of `fs.readFileSync` with any user-controllable path.
    ```yaml
    - pattern: |
        fs.readFileSync($PATH, ...)
    ```

2. **Express.js Framework:**
    - Detects the scenario in an Express.js application where `req.query.path` is directly passed to `fs.readFileSync`, which could be manipulated by an attacker.
    ```yaml
    - pattern: |
        app.get('/retrieve', (req, res) => {
          let filePath = req.query.path;
          fs.readFileSync(filePath, ...);
        });
    ```

3. **HTTP File Server:**
    - Detects the example of creating a basic HTTP server using the `http` module where `url.parse(req.url).pathname` is read directly, without proper validation.
    ```yaml
    - pattern: |
        http.createServer((req, res) => {
          let filePath = url.parse(req.url).pathname;
          fs.readFileSync(filePath, ...);
        });
    ```

Wherever `fs.readFileSync` is triggered with a variable or an expression that may depend on user input, a potential CWE-059 (Improper Link Resolution Before File Access) is considered dangerous and flagged.

Remember to verify and expand this rule with more specific cases based on different projects' context and the types of frameworks in use.

For more details on writing Semgrep rules, refer to the resources mentioned in the provided document, such as the [Semgrep documentation](https://semgrep.dev/docs/)【4:0†source】.