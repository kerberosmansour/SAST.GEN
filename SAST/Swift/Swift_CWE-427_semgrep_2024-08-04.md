BasedBased on the provided context on how to write Semgrep SAST rules and the goal to detect Uncontrolled Search Path Element (CWE-427) in Swift, here is a set of comprehensive Semgrep rules. This set includes examples and variations that could occur in popular Swift frameworks, targeting high false negatives and low false positives.

### Rule for Detecting Uncontrolled Search Path Element in Swift

```yaml
rules:
  - id: uncontrolled-search-path-element-swift
    languages: [swift]
    message: "Potential uncontrolled search path element detected"
    severity: WARNING
    patterns:
      - pattern: |
          let envPaths = ProcessInfo.processInfo.environment["$KEY"]
      - pattern-either:
          - pattern: |
              let paths = ProcessInfo.processInfo.environment["$KEY"]?.components(separatedBy: ":")
          - pattern: |
              let path = ProcessInfo.processInfo.environment["$KEY"]
            
metavariable-regex:
  $KEY: '^PATH$|^DYLD_LIBRARY_PATH$|^DYLD_FRAMEWORK_PATH$'

metadata:
  cwe: "CWE-427"
  owasp: "A9:2021-Insecure Design"
  source: "https://example.com/cwe-427"
```

### Explanation of the Rule

1. **Pattern Matching Environment Variables**:
    - Match assignment of environment variables to constants with `ProcessInfo.processInfo.environment["$KEY"]`.
    - Covers various ways of retrieving and splitting the `PATH` environment variable.

2. **Metavariable Conditions**:
    - Limit the metavariable `$KEY` to common environment paths such as `PATH`, `DYLD_LIBRARY_PATH`, and `DYLD_FRAMEWORK_PATH`.

### Additional Patterns for Frameworks

Swift is often used with various frameworks like Vapor, Kitura, and Perfect. We need to ensure our rule is adapted to these frameworks as well.

#### Vapor Example

```yaml
- id: vapor-env-path-swift
  languages: [swift]
  message: "Uncontrolled search path element in Vapor framework"
  severity: WARNING
  patterns:
    - pattern: |
        let envPaths = Environment.get("$KEY")
    - pattern-either:
        - pattern: |
            let paths = Environment.get("$KEY")?.split(separator: ":")
        - pattern: |
            let path = Environment.get("$KEY")
          
metavariable-regex:
  $KEY: '^PATH$|^DYLD_LIBRARY_PATH$|^DYLD_FRAMEWORK_PATH$'

metadata:
  cwe: "CWE-427"
  owasp: "A9:2021-Insecure Design"
  source: "https://example.com/cwe-427"
```

#### Kitura Example

```yaml
- id: kitura-env-path-swift
  languages: [swift]
  message: "Uncontrolled search path element in Kitura framework"
  severity: WARNING
  patterns:
    - pattern: |
        let envPaths = ProcessInfo.processInfo.environment["$KEY"]
    - pattern-either:
        - pattern: |
            let paths = ProcessInfo.processInfo.environment["$KEY"]?.components(separatedBy: ":")
        - pattern: |
            let path = ProcessInfo.processInfo.environment["$KEY"]
          
metavariable-regex:
  $KEY: '^PATH$|^DYLD_LIBRARY_PATH$|^DYLD_FRAMEWORK_PATH$'

metadata:
  cwe: "CWE-427"
  owasp: "A9:2021-Insecure Design"
  source: "https://example.com/cwe-427"
```

#### Perfect Example

```yaml
- id: perfect-env-path-swift
  languages: [swift]
  message: "Uncontrolled search path element in Perfect framework"
  severity: WARNING
  patterns:
    - pattern: |
        let envPaths = PerfectEnv.getProcessInfo().environment["$KEY"]
    - pattern-either:
        - pattern: |
            let paths = PerfectEnv.getProcessInfo().environment["$KEY"]?.split(separator: ":")
        - pattern: |
            let path = PerfectEnv.getProcessInfo().environment["$KEY"]
          
metavariable-regex:
  $KEY: '^PATH$|^DYLD_LIBRARY_PATH$|^DYLD_FRAMEWORK_PATH$'

metadata:
  cwe: "CWE-427"
  owasp: "A9:2021-Insecure Design"
  source: "https://example.com/cwe-427"
```

### Summary
The above sets of rules follow the general principles for writing effective Semgrep rules by specifying:

- **Precise Patterns**: They utilize pattern-either to account for common variations in the way the environment paths are accessed.
- **Metavariable Filtering**: By using `metavariable-regex`, only specific environment variables are targeted, reducing false positives.
- **Framework Awareness**: The rules consider popular Swift frameworks ensuring more accurate and relevant detection in real-world scenarios.

### References
The context and methodologies for creating these rules were derived using best practice guidelines from the Semgrep documentation and related resources【4:0†source】【4:1†source】【4:2†source】【4:4†source】【4:5†source】. For more detailed examples and advanced usage, refer to the [Semgrep official documentation](https://semgrep.dev/docs/).