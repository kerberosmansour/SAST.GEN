ToTo create Semgrep SAST rules for identifying occurrences of "Uncontrolled Resource Consumption (CWE-400)" in JavaScript, we need to capture instances where the code might perform expensive operations repeatedly or without controls. We will use Semgrep’s pattern syntax and capabilities to handle variations across popular JavaScript frameworks.

Here's a set of Semgrep rules designed to detect variations of this vulnerability:

```yaml
rules:
  - id: detect-recursive-calls
    languages: [javascript, typescript]
    message: "Potential uncontrolled resource consumption due to recursive calls"
    severity: ERROR
    patterns:
      - pattern: |
          function $FUNC(...) {
            ...
            $FUNC(...)
            ...
          }
      - pattern-not: |
          function $FUNC(...) {
            if (...) {
              return ...;
            }
            $FUNC(...)
          }

  - id: detect-infinite-loops
    languages: [javascript, typescript]
    message: "Potential infinite loop causing uncontrolled resource consumption"
    severity: ERROR
    patterns:
      - pattern: |
          while (true) {
            ...
          }
      - pattern: |
          for (;;) {
            ...
          }

  - id: detect-uncontrolled-iterations
    languages: [javascript, typescript]
    message: "Uncontrolled resource consumption due to excessive iterations"
    severity: ERROR
    patterns:
      - pattern: |
          for (let $VAR = 0; $VAR < $EXPR; $VAR++) {
            ...
          }
      - metavariable-comparison:
          metavariable: $EXPR
          comparison: $EXPR > 10000

  - id: detect-no-rate-limit-axios
    languages: [javascript, typescript]
    message: "Uncontrolled resource consumption due to missing rate limiting with axios"
    severity: ERROR
    patterns:
      - pattern: |
          axios.get($URL).then($RESPONSE => {
            ...
            axios.get($URL)
            ...
          })

  - id: detect-no-throttle-debounce
    languages: [javascript, typescript]
    message: "Potential uncontrolled resource consumption due to missing throttle/debounce"
    severity: WARNING
    patterns:
      - pattern: |
          $OBJ.$METHOD = function(...) {
            ...
            window.addEventListener($EVENT, $FUNC)
            ...
          }
      - pattern-not: |
          $OBJ.$METHOD = function(...) {
            ...
            window.addEventListener($EVENT, _.throttle($FUNC, ...))
            ...
          }
      - pattern-not: |
          $OBJ.$METHOD = function(...) {
            ...
            window.addEventListener($EVENT, _.debounce($FUNC, ...))
            ...
          }
```

### Explanation:
1. **detect-recursive-calls**: Detects functions where there is a potential for uncontrolled recursive calls without any base case to terminate the recursion.
2. **detect-infinite-loops**: Catches common cases of infinite loops using `while (true)` and `for (;;)` patterns.
3. **detect-uncontrolled-iterations**: Flags `for` loops iterating for a very high number of times, which could cause performance issues.
4. **detect-no-rate-limit-axios**: Specifically looks for axios HTTP requests in promise chains without implementing any form of rate limiting.
5. **detect-no-throttle-debounce**: Checks for event listeners potentially causing high-frequency function calls without throttling or debouncing.

These rules cover various scenarios and frameworks, ensuring a broad capture of potential uncontrolled resource consumption issues.