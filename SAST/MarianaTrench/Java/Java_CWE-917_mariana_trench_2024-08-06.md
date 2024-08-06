#### Context Review
### Structure of Mariana Trench Rules
Mariana Trench (MT) rules consist of **sources**, **sinks**, and **propagations** which describe how taint flows through the program. The rules utilize a Domain-Specific Language (DSL) to define these elements within JSON files, typically called **model generators**. These generators specify methods or fields as sources, sinks, or methods that propagate taint. Here is a detailed breakdown of each component:
1. **Source Definitions**: Identify where taint originates in the application. This could be user inputs or other untrusted data.
2. **Sink Definitions**: Specify where the taint should not propagate. Sinks are typically sensitive operations like executing code or accessing sensitive data.
3. **Propagation Rules**: Define how taint propagates through methods and their parameters or return values.
4. **Shim Definitions**: Use shims to model third-party or abstracted methods accurately.
5. **Rules**: Specify data flow from specific sources to specific sinks and define conditions for such flows.

### Example Rule and Structure
```json
{
  "name": "Sensitive data transmitted via HTTP",
  "code": 1,
  "description": "Sensitive data sent over unencrypted HTTP connections",
  "sources": [
    "UserPassword",
    "CreditCardNumber"
  ],
  "sinks": [
    "HttpSink"
  ]
}
```
The example above defines a rule that identifies a flow from sensitive data sources like "UserPassword" and "CreditCardNumber" to an HTTP sink. It detects if sensitive data is transmitted over unencrypted connections    .

## Vulnerability Analysis: CWE-917 in Java
**Expression Language Injection** in Java occurs when user-controlled input is interpreted as an expression by the Expression Language (EL) engine, potentially leading to the execution of arbitrary code. This vulnerability commonly manifests in web applications using JSP expressions but can be present in any system interpreting user inputs as code.

### Common Patterns and Entry Points
1. **User Inputs**: Data from user-generated content or HTTP requests which may be used directly as expressions.
2. **Expression Engine Execution**: Instances where the application processes input through an EL engine, such as JSP.
3. **Reflection and Dynamic Execution**: Methods involving reflection or dynamically executed scripts potentially influenced by untrusted input.

### Example Vulnerable Code
```java
String expression = request.getParameter("expression");
ExpressionFactory factory = new ExpressionFactoryImpl();
SimpleContext context = new SimpleContext();
Object result = factory.createValueExpression(context, expression, Object.class).getValue(context);
```
In the example above, user input from `request.getParameter("expression")` directly flows into an expression engine, risking EL injection.

## Mariana Trench Rule Creation
### Source Definitions
Define sources where user input might come from:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": {
        "constraint": "name",
        "pattern": "getParameter"
      },
      "model": {
        "sources": [
          {
            "kind": "UserInput",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```
This rule defines methods matching `getParameter` as sources of `UserInput`.

### Sink Definitions
Define sinks where the EL injection might occur:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": {
        "constraint": "name",
        "pattern": "createValueExpression"
      },
      "model": {
        "sinks": [
          {
            "kind": "ExpressionLanguageInjection",
            "port": "Argument(1)"
          }
        ]
      }
    }
  ]
}
```
This rule identifies `createValueExpression` method calls as potential sinks for EL Injection via its second argument.

### Propagation Rules
Define how taint can propagate:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [{
        "constraint": "name",
        "pattern": "setAttribute"
      }],
      "model": {
        "propagation": [
          {
            "input": "Argument(1)",
            "output": "Variable"
          }
        ]
      }
    }
  ]
}
```
This rule specifies that the second argument of `setAttribute` can propagate taint to a variable    .

### Rule Definition
Combine sources, sinks, and propagation into a coherent rule:
```json
{
  "name": "Expression Language Injection",
  "code": 1001,
  "description": "User input flowing into expression language evaluation leading to EL Injection",
  "sources": [
    "UserInput"
  ],
  "sinks": [
    "ExpressionLanguageInjection"
  ],
  "transforms": []
}
```

## Testing and Validation
To test these rules, create test cases covering both typical and edge scenarios. For example:
1. **Positive Test Case**: `UserInput` directly used in `createValueExpression`.
2. **Negative Test Case**: Valid inputs not leading to EL injection.

### Usage of Mariana Trench
To validate these rules, perform the following steps:
1. **Run Analysis**: Execute Mariana Trench on the codebase with the rules.
2. **Review Results**: Review identified flows and adjust rules to minimize false positives and negatives.
3. **Continuous Integration**: Integrate Mariana Trench in CI to regularly scan for this and other vulnerabilities    .

By carefully defining sources, sinks, and propagation paths, and by extensively testing, you can create effective Mariana Trench rules for detecting Expression Language Injection with high accuracy and low false positives/negatives.