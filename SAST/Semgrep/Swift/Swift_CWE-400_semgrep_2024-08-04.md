To write Semgrep SAST rules for detecting Uncontrolled Resource Consumption (CWE-400) in Swift, one can follow the best practices and examples found in the document. Here is a set of Semgrep rules that aim to provide high false-negative and low false-positive rates for this vulnerability, covering variations across popular Swift frameworks.

### Overview:
These rules will match patterns that can lead to uncontrolled resource consumption such as unbounded loops, unbounded recursion, and unbounded memory allocations.

### Rule: Detecting Unbounded Loops
This rule detects unbounded loops, which can lead to uncontrolled resource consumption.

```yaml
rules:
  - id: swift-unbounded-loop
    languages: [swift]
    message: "Unbounded loop detected which may cause uncontrolled resource consumption (CWE-400)"
    severity: WARNING
    patterns:
      - pattern-inside: |
          while ...
            ...
      - metavariable-pattern:
          metavariable: $LOOP_CONDITION
          patterns:
            - pattern-not: |
                $LOOP_CONDITION <= ...
            - pattern-not: |
                $LOOP_CONDITION < ...
```

### Rule: Detecting Unbounded Recursion
This rule identifies unbounded recursive function calls.

```yaml
rules:
  - id: swift-unbounded-recursion
    languages: [swift]
    message: "Unbounded recursion detected which may cause uncontrolled resource consumption (CWE-400)"
    severity: WARNING
    patterns:
      - pattern: |
          func $FUNC(...) {
              ...
              $FUNC(...)
              ...
          }
      - metavariable-pattern:
          metavariable: $FUNC
          patterns:
            - pattern-not: |
                ...
```

### Rule: Detecting Unbounded Memory Allocation
This rule identifies potential unbounded memory allocations.

```yaml
rules:
  - id: swift-unbounded-memory-allocation 
    languages: [swift]
    message: "Unbounded memory allocation detected which may cause uncontrolled resource consumption (CWE-400)"
    severity: WARNING
    patterns:
      - pattern-inside: |
          let $VAR = [Int](repeating: 0, count: ...)
      - metavariable-pattern:
          metavariable: $COUNT
          patterns:
            - pattern-not: |
                0...1000
```

### Key Points from Semgrep Documentation:
1. **Use of Metavariable Patterns:**
   - Employ `metavariable-pattern` to refine the search and avoid false positives by excluding safe patterns【4:0†source】 .
   
2. **Pattern Composition Techniques:**
   - Utilize `pattern-inside` and `pattern-either` to handle complex patterns and variations within the frameworks  .

3. **Recursive Patterns:**
   - Identify recursive functions that could lead to infinite recursion if not terminated properly .

4. **Optimizing Rules:**
   - Focus on pinpointing resource-intensive operations and ensure the pattern is precise to avoid high false positives    .

These rules cover common scenarios for uncontrolled resource consumption issues in Swift applications. Continue refining the patterns based on your specific codebase and the libraries used to improve accuracy further.