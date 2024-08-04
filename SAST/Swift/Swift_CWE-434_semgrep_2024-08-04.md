ToTo create Semgrep SAST rules for the vulnerability "Unrestricted Upload of File with Dangerous Type (CWE-434) in Swift", we use patterns that match instances where file uploads are allowed without proper validation. Here's how to write these rules, covering variations in popular Swift frameworks like Vapor and Kitura:

```yaml
rules:
  - id: unrestricted-file-upload
    languages: [swift]
    message: "Unrestricted Upload of File with Dangerous Type (CWE-434)"
    severity: ERROR
    patterns:
      - pattern-either:
          # Vapor framework - checking filename extensions
          - pattern: |
              func uploadHandler(_ req: Request) throws -> EventLoopFuture<String> {
                  let data = try req.content.decode(FileUpload.self)
                  if ![".jpg", ".png", ".gif"].contains(data.filename.fileExtension) {
                      throw Abort(.badRequest, reason: "Invalid file type")
                  }
                  // code to save file
              }
          # Vapor framework - missing file type validation
          - pattern: |
              func uploadHandler(_ req: Request) throws -> EventLoopFuture<String> {
                  let data = try req.content.decode(FileUpload.self)
                  // Missing file type validation
                  // code to save file
              }
          # Kitura framework - checking filename extensions
          - pattern: |
              router.post("/upload") { request, response, next in
                  guard let files = request.files, files.count > 0 else {
                      response.status(.badRequest)
                      return next()
                  }
                  for file in files {
                      guard [".jpg", ".png", ".gif"].contains(file.type) else {
                          response.status(.badRequest).send("Invalid file type")
                          return next()
                      }
                      // code to save file
                  }
                  response.status(.OK)
                  next()
              }
          # Kitura framework - missing file type validation
          - pattern: |
              router.post("/upload") { request, response, next in
                  guard let files = request.files, files.count > 0 else {
                      response.status(.badRequest)
                      return next()
                  }
                  // Missing file type validation
                  for file in files {
                      // code to save file
                  }
                  response.status(.OK)
                  next()
              }
```

### Explanation:
1. **Vapor Framework:**
   - Example of correct usage includes checking file extension.
   - Example of missing file type validation.
   
2. **Kitura Framework:**
   - Example of correct usage includes checking file extension.
   - Example of missing file type validation.

### Concepts Covered:
- **Pattern-Either:** Ensures that multiple code patterns can trigger the rule.
- **Severity and Message:** Defines the severity of the rule and the message that will be shown when the rule is triggered.

By properly implementing this, we can effectively detect and prevent instances of CWE-434 in Swift projects using popular frameworks.

For further details and examples on writing custom Semgrep rules, consult the official documentation and resources provided in the extracted documents【4:0†source】 .