ToTo create a set of Mariana Trench Static Application Security Testing (SAST) rules to detect Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') (CWE-917) in Java, you'll need to follow these steps:

1. **Identify Sources and Sinks**:
    - **Sources**: These are methods where tainted data (potential malicious input) can enter the application. For Expression Language Injection, sources typically include user inputs such as parameters from web requests, form inputs, cookies, etc.
    - **Sinks**: These are methods or points in the application where the tainted data gets executed or evaluated as part of an expression language.

2. **Specify Models in JSON**:
    - Models are JSON structures that describe sources, sinks, and propagations in Mariana Trench. They define which methods should be considered as sources, sinks, or have certain behaviors influencing taint analysis.

3. **Write Rules**:
    - Rules define how taint flows from sources to sinks. They are the core configurations that tell Mariana Trench what constitutes a security issue.

### Step-by-Step Guide:

#### 1. Define Sources:
Identify methods (APIs) that could receive user-provided data. In a web application context, these sources might be parameters of HTTP requests or properties of request objects in popular Java frameworks like Spring or Struts.

Example Source Configuration:

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "any_parameter",
          "inner": {
            "constraint": "type",
            "name": "javax.servlet.http.HttpServletRequest"
          }
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "UserInput",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```

#### 2. Define Sinks:
Identify points where expression languages evaluate the user-provided data. Typically, this might involve methods using libraries for evaluating expressions like JSTL, EL, or Spring's SpEL.

Example Sink Configuration:

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "evaluate"
        },
        {
          "constraint": "parent",
          "inner": {
            "constraint": "name",
            "pattern": "javax.el.ELProcessor"
          }
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "ExpressionLanguageSink",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```

#### 3. Define Propagations:
Propagations describe how taint from one part of the application flows to another. An example propagation is transferring taint from one method argument to another method's return value.

Example Propagation:

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "any_parameter",
          "inner": {
            "constraint": "type",
            "name": "javax.servlet.http.HttpServletRequest"
          }
        }
      ],
      "model": {
        "propagation": [
          {
            "input": "Argument(0)",
            "output": "Return"
          }
        ]
      }
    }
  ]
}
```

#### 4. Define Rules:
Finally, specify rules that connect sources and sinks to form the basis for identifying potential vulnerabilities.

Example Rule:

```json
{
  "name": "User Input to EL Injection",
  "code": 1,
  "description": "User controlled input flows to EL evaluation method.",
  "sources": [
    "UserInput"
  ],
  "sinks": [
    "ExpressionLanguageSink"
  ]
}
```

### Additional Considerations:
- **Framework-Specific Variations**: Depending on the framework in use (e.g., Spring, Struts), you may need additional sources and sinks configurations.
- **Sanitizers and Taint Tracking Enhancements**: Use sanitizers to stop taints from propagating in known-safe contexts and define propagations to accurately track taint flow.

### References and Examples:
- Check [Mariana Trench's usage documentation](https://github.com/facebook/mariana-trench/blob/main/documentation/usage.md) for details on running the tool.
- Review the [default rules.json configuration](https://github.com/facebook/mariana-trench/blob/main/configuration/rules.json) for examples of existing rules【6:0†source】  .

By carefully defining sources, sinks, and rules as shown, you can create a robust set of SAST rules for detecting Expression Language Injection vulnerabilities with high accuracy.