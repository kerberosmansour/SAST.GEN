ToTo generate effective Semgrep rules with high true positive and low false positive rates for the Improper Link Resolution Before File Access ('Link Following') vulnerability in Swift (CWE-059), we can follow these guidelines and steps derived from your provided document on writing Semgrep SAST rules.

### Steps to Create Semgrep SAST Rules

1. **Identify Vulnerable Code Patterns:**
   - Understand how link following vulnerability manifests in Swift.
   - Gather common patterns in popular Swift frameworks.

2. **Use Metavariables and Comparisons:**
   - Use metavariables to generalize specific code elements.
   - Apply metavariable-comparison and -patterns to refine the search.

3. **Combine Multiple Patterns:**
   - Use `pattern-either` and `pattern-inside` for detailed context matching.
   - Use `pattern-not` to exclude known safe variants.

4. **Optimize for Context:**
   - Ensure high performance by narrowing the focus to specific contexts applicable to the vulnerability.

### Example Rule for Link Following in Swift

```yaml
rules:
  - id: link-following-vulnerability
    languages: [swift]
    message: |
      Potential improper link resolution before file access.
    patterns:
      - pattern-either:
          # Usage of fileManager.fileExists with unsafe link following
          - pattern: |
              if FileManager.default.fileExists(atPath: $PATH) {
                ...
                // Unsafe resolution or follow-up of symlink
                ...
                _ = try? FileManager.default.destinationOfSymbolicLink(atPath: $LINK_PATH)
                ...
              }
          # Usage of realpath with unsafe link handling
          - pattern: |
              let fullPath = realpath($PATH, nil)
              ...
              // Unsafe resolution
              ...
              _ = $LINK.followSymlink(atPath: $LINK_PATH)
          # Typical use in common Swift frameworks
          - pattern: |
              let contents = try $FILEMAN.default.contentsOfDirectory(atPath: $DIRECTORY)
              for $ITEM in contents {
                ...
                if FileManager.default.isDeletableFile(atPath: $ITEM) {
                  let destination = try FileManager.default.destinationOfSymbolicLink(atPath: $ITEM)
                  ...
                }
              }
    severity: WARNING
    metadata:
      cwe: "CWE-059"
      references:
        - "https://cwe.mitre.org/data/definitions/59.html"
```

### Explanation of the Rule

1. **ID and Description:**
   - The `id` field provides a unique identifier for the rule.
   - The `message` field explains the nature of the detected issue.

2. **Patterns:**
   - `patterns` field lists multiple `pattern-either` blocks to match different variations of the vulnerability.
   - Metavariables (`$PATH`, `$LINK_PATH`, `$DIRECTORY`, etc.) are used to generalize file paths and directory contents.

3. **Pattern Contexts:**
   - The rule considers typical actions in the Swift language like `fileExists`, `realpath`, and common file operations in Swift frameworks. 

4. **Severity:**
   - The `severity` field rates the criticality of the detected issue.

By adhering to these detailed steps and using the provided formats   , you can create effective SAST rules to identify CWE-059 in Swift applications.

Please verify these against real-world Swift code and frameworks in controlled environments to fine-tune the rule settings.