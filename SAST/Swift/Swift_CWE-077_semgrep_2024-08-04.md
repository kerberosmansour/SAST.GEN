BasedBased on your requirements to write Semgrep SAST rules for detecting "Improper Neutralization of Special Elements used in a Command ('Command Injection')" (CWE-077) in Swift, and including variations relevant to popular frameworks, I've utilized the information from the document you provided to generate the following detailed Semgrep rules. These rules aim for high accuracy with lower false-positive rates by leveraging different Semgrep constructs.

### Semgrep Rule Template for Command Injection in Swift

```yaml
rules:
  - id: swift-command-injection
    languages: [swift]
    message: "Potential Command Injection found due to improper handling of command-line inputs"
    severity: ERROR
    patterns:
      - pattern: $COMMAND = Process()
      - pattern-inside: |
          func $FUNC(...) {
            ...
            $COMMAND.launchPath = $PATH
            $COMMAND.arguments = [...]
            ...
            $COMMAND.launch()
            ...
          }
      - pattern-not: |
          $COMMAND.arguments = [
            ...
            $SAFE_INPUT,
            ...
          ]
    metavariable-comparison:
      - metavariable: $SAFE_INPUT
        comparison: $SAFE_INPUT != safeUserInput($ANY)
      
  - id: shell-command-exec-method
    languages: [swift]
    message: "Direct call to shell command execution detected, which could lead to command injection"
    severity: WARNING
    pattern: |
      Process.launchedProcess(launchPath: $PATH, arguments: [$ARG, ...])
    metavariable-pattern:
      metavariable: $ARG
      patterns:
        - pattern-not: safeUserInput($ANY)

  - id: command-injection-hardcoding-check
    languages: [swift]
    message: "Hardcoded command execution found, review to prevent command injection"
    severity: WARNING
    pattern: |
      $COMMAND = Process()
      $COMMAND.launchPath = $HARDCODED_PATH

  - id: tainted-data-injection
    languages: [swift]
    message: "Potential use of tainted data in command execution, review for command injection risk"
    severity: ERROR
    pattern: |
      let $INJECTED_DATA = $TAINTED_SOURCE
      ...
      $COMMAND = Process()
      ...
      $COMMAND.arguments = [
        ...
        $INJECTED_DATA,
        ...
      ]
    patterns:
      - pattern: let $INJECTED_DATA = $TAINTED_SOURCE
    metavariable-pattern:
      metavariable: $TAINTED_SOURCE
      patterns:
        - pattern-either:
            - pattern: unsafeUserInput(...)
            - pattern: taintedData(...)

```

### Explanation and Framework Coverage

#### Rule 1: Command Injection through Properties of `Process`
This rule checks whether `Process` instances are initialized with unsafe paths or arguments. It matches against `launchPath` and `arguments` properties being set and verifies that arguments are not safely derived.

#### Rule 2: Direct Shell Execution
This rule specifically catches direct calls to `Process.launchedProcess`, a common way to execute commands with parameters. It ensures that such calls are safely parameterized.

#### Rule 3: Hardcoded Path
Detects instances where `launchPath` is hardcoded within `Process`, which might not be parametrized properly and can lead to injections if not handled carefully.

#### Rule 4: Tainted Data Usage
This rule looks for command arguments constructed from potentially tainted data sources, ensuring to catch instances where unsafe user input can reach command execution.

### Considerations
- **Metavariables**: `$COMMAND`, `$PATH`, `$ARG`, etc., are used to capture variable names and their values, allowing flexible pattern matching.
- **Patterns & Metavariable Comparisons**: Utilizing patterns like `pattern-inside`, `pattern-not`, and `metavariable-comparison` to fine-tune matches and reduce false positives.
- **Contexts**: By incorporating `pattern-inside`, it ensures the context of function to see where commands are set and launched.

These rules are designed based on best practices from the Semgrep documentation to minimize false positives while accurately identifying potential command injection vulnerabilities in Swift code    .