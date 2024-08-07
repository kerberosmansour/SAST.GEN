ToTo write effective Mariana Trench SAST rules for identifying "Improper Neutralization of Special Elements used in a Command ('Command Injection')" (CWE-77) in Java, we need to consider the following steps:

1. **Identify Sources**: Methods that take user input which can be exploited for command injection.
2. **Identify Sinks**: Methods that execute system commands.
3. **Define Propagation Rules**: Ways taint can propagate from sources to sinks.
4. **Write JSON Model Generators and Rules**: Use Mariana Trench's DSL to generate models and rules.

### Sources and Sinks
#### 1. Identify Sources
These methods typically take input from the user which is then utilized elsewhere in the code:
- `java.lang.String System.console().readLine()`
- `java.lang.String javax.servlet.http.HttpServletRequest.getParameter(String name)`
- `java.lang.String javax.servlet.http.HttpServletRequest.getQueryString()`
- `java.util.Scanner.nextLine()`

#### 2. Identify Sinks
These commands execute system commands which, if compromised by user input, can lead to command injection:
- `java.lang.Runtime.exec(String command)`
- `java.lang.Runtime.exec(String[] cmdarray)`
- `java.lang.ProcessBuilder.start()`

### Example JSON Rule
We will create a rule that identifies data flows from the aforementioned sources to the sinks.

#### 3. Define Propagation Rules
We have to describe how taint propagates through methods.

#### JSON Model Generator for Sources
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "readLine" },
        { "constraint": "parent", "inner": { "constraint": "type", "name": "System.console" } }
      ],
      "model": { "sources": [{ "kind": "UserInput", "port": "Return" }] }
    },
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "getParameter|getQueryString" },
        { "constraint": "parent", "inner": { "constraint": "type", "name": "javax.servlet.http.HttpServletRequest" } }
      ],
      "model": { "sources": [{ "kind": "UserInput", "port": "Return" }] }
    },
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "nextLine" },
        { "constraint": "parent", "inner": { "constraint": "type", "name": "java.util.Scanner" } }
      ],
      "model": { "sources": [{ "kind": "UserInput", "port": "Return" }] }
    }
  ]
}
```

#### JSON Model Generator for Sinks
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "exec" },
        { "constraint": "parent", "inner": { "constraint": "type", "name": "java.lang.Runtime" } },
        { "constraint": "parameter", "idx": 0, "inner": { "constraint": "type", "name": "java.lang.String" } }
      ],
      "model": { "sinks": [{ "kind": "CommandExec", "port": "Argument(0)" }] }
    },
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "start" },
        { "constraint": "parent", "inner": { "constraint": "type", "name": "java.lang.ProcessBuilder" } },
        { "constraint": "parameter", "idx": 0, "inner": { "constraint": "type", "name": "java.util.List" } }
      ],
      "model": { "sinks": [{ "kind": "CommandExec", "port": "Argument(0)" }] }
    }
  ]
}
```

#### JSON Rule for Command Injection
```json
{
  "name": "User input flows into command execution",
  "code": 1,
  "description": "Values from user-controlled sources may eventually flow into system command execution, leading to potential command injection.",
  "sources": ["UserInput"],
  "sinks": ["CommandExec"]
}
```

### Additional Details
- **Sources and Sinks Configuration**: Ensure the model generators and rules are referenced in `default_generator_config.json` as per the Mariana Trench documentation  .
- **Heuristics Configuration**: Adjust heuristic parameters to balance performance and precision, as documented  .

By following these guidelines and utilizing the sample JSON configurations, you can effectively create Mariana Trench SAST rules to detect command injection vulnerabilities in Java applications with high accuracy and low false positives/negatives.