BasedBased on the provided guidelines on writing Semgrep SAST rules, here is a custom rule for detecting the Allocation of Resources Without Limits or Throttling (CWE-770) in Swift, along with its variations:

### Semgrep Rule for Swift (CWE-770)

```yaml
rules:
  - id: allocation-of-resources-without-limits-or-throttling
    languages: [swift]
    message: Allocation of resources without limits or throttling detected
    severity: WARNING
    patterns:
      - pattern: |
          let $RESOURCE = $FUNCTION($ARGS)
      - metavariable-pattern:
          metavariable: $FUNCTION
          patterns:
            - pattern: DispatchQueue.global
            - pattern: DispatchQueue.concurrentPerform
            - pattern: myFunction // Replace with a function that might be resource-intensive
      - metavariable-comparison:
          metavariable: $ARGS
          comparison: int($ARGS) > 1000 # Adjust the threshold value as needed considering typical safe limits
      - pattern-not: let throttledResource = $FUNCTION($ARGS)
```

### Explanation

1. **Pattern Matching Resource Allocation**:
   - `let $RESOURCE = $FUNCTION($ARGS)`: This pattern matches any assignment where a resource is allocated by calling a function with arguments.

2. **Metavariable Pattern for Function Names**:
   - This rule uses `metavariable-pattern` to target specific functions known for resource-intensive operations:
     - `DispatchQueue.global`
     - `DispatchQueue.concurrentPerform`
     - `myFunction` (Placeholder for custom functions that may cause issues)

3. **Metavariable Comparison for Arguments**:
   - The rule includes a `metavariable-comparison` clause to limit matches to cases where the number of arguments or some numeric parameter (resources being requested) exceeds a specified threshold.

4. **Pattern Not Conditions**:
   - The `pattern-not` clause is used to exclude cases where resource allocations are mitigated by specifying conditions such as controlled or limited allocations.

Use this rule to scan Swift codebases where potential allocations without proper throttling might occur. Adjust the patterns and threshold values based on the specific project's needs and known risky functions.

### References
These detailed components are based on the instructions for writing Semgrep rules and utilizing metavariables, pattern combining, and logical operators:

- **Metavariable-Pattern**: Useful for specifying patterns associated with particular functions or variables【4:0†source】【4:4†source】     .
- **Metavariable-Comparison**: Useful for comparing metavariable values to detect specific conditions【4:0†source】【4:8†source】 .
- **Pattern-Not**: Excludes specific patterns to reduce false positives【4:0†source】【4:11†source】   .

Ensure that this rule is tested and fine-tuned in the project-specific or typical Swift environments to maximize its effectiveness while maintaining low false positives and negatives rates.