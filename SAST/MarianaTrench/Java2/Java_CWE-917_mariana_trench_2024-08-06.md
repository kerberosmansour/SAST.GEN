WhenWhen writing Mariana Trench SAST rules for detecting the Improper Neutralization of Special Elements used in an Expression Language Statement (`Expression Language Injection`, CWE-917) in Java, you need to design comprehensive rules that identify potential sources of untrusted input and sinks where this input could be dynamically evaluated, leading to injection vulnerabilities. Here are the detailed steps and example rules based on the Mariana Trench documentation:

### Steps to Create SAST Rules for Expression Language Injection in Mariana Trench

1. **Identify Sources**: Determine methods that could receive untrusted input from users.

2. **Identify Sinks**: Determine methods or evaluations in frameworks that can execute dynamically evaluated expressions.

3. **Configure Model Generators**: Write JSON files to specify these sources and sinks.

4. **Define Rules**: Establish rules that identify flows from these sources to sinks.

### Example Configuration

#### 1. Source Identification

Let's identify common methods in Java that receive user input which might be manipulated for exploitation:
- `HttpServletRequest::getParameter`
- `HttpServletRequest::getHeader`
- `HttpServletRequest::getCookies`

#### 2. Sink Identification

Potential sinks where EL injection could be exploited include, but are not limited to:
- `javax.el.ELContext::setVariable`
- Any method using `javax.el.ExpressionFactory` to create and evaluate expressions:
  - `ExpressionFactory::createValueExpression`
  - `ExpressionFactory::createMethodExpression`

#### 3. Model Generators for Sources and Sinks

**Sources Models:**

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "getParameter"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "HttpServletRequest"}}
      ],
      "model": {
        "sources": [
          {"kind": "UserInput", "port": "Return"}
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "getHeader"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "HttpServletRequest"}}
      ],
      "model": {
        "sources": [
          {"kind": "UserInput", "port": "Return"}
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "getCookies"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "HttpServletRequest"}}
      ],
      "model": {
        "sources": [
          {"kind": "UserInput", "port": "Return"}
        ]
      }
    }
  ]
}
```

**Sinks Models:**

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "setVariable"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "ELContext"}}
      ],
      "model": {
        "sink": [
          {"kind": "ExpressionLanguageSink", "port": "Argument(1)"}
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "createValueExpression"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "ExpressionFactory"}}
      ],
      "model": {
        "sink": [
          {"kind": "ExpressionLanguageSink", "port": "Argument(2)"}
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "createMethodExpression"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "ExpressionFactory"}}
      ],
      "model": {
        "sink": [
          {"kind": "ExpressionLanguageSink", "port": "Argument(3)"}
        ]
      }
    }
  ]
}
```

#### 4. Rule Definitions

Now, define the rules that look for flows from `UserInput` sources to `ExpressionLanguageSink` sinks:

```json
{
  "rules": [
    {
      "name": "User input to EL Injection",
      "code": 1001,
      "description": "Potential Expression Language Injection from user input",
      "sources": ["UserInput"],
      "sinks": ["ExpressionLanguageSink"]
    }
  ]
}
```

### Putting It Together

1. Create the necessary model generator JSON files defining sources and sinks.
2. Define the rules in `rules.json`.
3. Integrate these model generators and rules into the Mariana Trench configuration.

**Model Generator Configuration Example:**

```json
{
  "model_generator_configuration_paths": ["source_generators.json", "sink_generators.json"]
}
```

**Rules Configuration Example:**

```json
{
  "rules_paths": ["rules.json"]
}
```

### Validating Your Configuration

1. **Run Mariana Trench** on your codebase:
   ```bash
   mariana-trench --model-generator-configuration-paths=/path/to/your/config.json --rules-paths=/path/to/your/rules.json --apk-path=/path/to/your/app.apk
   ```

2. **Analyze the results** using SAPP or another result processing tool to verify the detection of EL injection vulnerabilities      .

These configurations maximize the detection of EL injection points while lowering false positives ensuring a practical and reliable SAST solution using Mariana Trench for Java applications.