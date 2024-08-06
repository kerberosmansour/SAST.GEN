BasedBased on the context provided in the document, here's how you can create Semgrep rules to detect instances of "Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')" (CWE-022) in Swift. 

### Semgrep Rule Example

#### Rule 1: Detecting Explicit Unsafe Path Operations

```yaml
rules:
- id: swift-path-traversal-explicit
  languages: [swift]
  message: |
    Unsafe path traversal detected. Input paths should be validated to ensure they do not contain traversal sequences or other unsafe content.
  severity: ERROR
  patterns:
    - pattern: |
        let $PATH = ...
        ... FileManager.default.contents(atPath: $PATH)
    - metavariable-pattern:
        metavariable: $PATH
        patterns:
          - pattern: ... + "../" + ...
          - pattern: ... + "..\\" + ...
```

#### Rule 2: Detecting Web Framework Unvalidated Path Access
For detecting common variations in popular frameworks like Vapor, Kitura, and Perfect.

**Vapor Framework Example:**

```yaml
rules:
- id: swift-path-traversal-vapor
  languages: [swift]
  message: |
    Potential path traversal vulnerability in a Vapor route. Validate and sanitize incoming 'file' parameter.
  severity: ERROR
  pattern-either:
    - pattern: |
        app.get("download", ":file") { req -> EventLoopFuture<Response> in
            let file = try req.parameters.require("file")
            ...
            return ...
    - pattern: |
        app.post("upload", ":file") { req -> EventLoopFuture<Response> in
            let file = try req.parameters.require("file")
            ...
            return ...
```

**Kitura Framework Example:**

```yaml
rules:
- id: swift-path-traversal-kitura
  languages: [swift]
  message: |
    Potential path traversal vulnerability in a Kitura route. Validate and sanitize incoming 'file' parameter.
  severity: ERROR
  patterns:
    - pattern: |
        router.get("/download/:file") { request, response, next in
            let file = request.parameters["file"] ?? ""
            ...
            next()
    - pattern: |
        router.post("/upload/:file") { request, response, next in
            let file = request.parameters["file"] ?? ""
            ...
            next()
```

### Explanation
1. **Rule 1 – Explicit Path Operations**:
   - This rule targets raw path operations where user-provided input could include path traversal sequences like `../` or `..\`. The use of `metavariable-pattern` ensures that the rule matches the paths that contain traversal sequences.

2. **Rule 2 – Common Frameworks (Vapor and Kitura)**:
   - These rules inspect route handlers in web frameworks, where user-input parameters could be used to directly access filesystem paths. The rules focus on potential vulnerabilities in request parameters like `:file` that are used in path operations.
   
### Variations

To further adapt these rules to new frameworks or patterns:
- **Adjust the patterns** to include more route definitions, URL path parameters, and other typical path usages.
- **Refine metavariable patterns** to ensure higher precision in matching potential unsafe path concatenations or operations.

These rules can help identify common CWE-022 instances in Swift by capturing both explicit file operations and framework-specific vulnerabilities【4:0†source】【4:1†source】【4:2†source】 .