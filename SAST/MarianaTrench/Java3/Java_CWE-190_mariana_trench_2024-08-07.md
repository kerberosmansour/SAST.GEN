###### Writing SAST Rules for Integer Overflow or Wraparound (CWE-190) in Java

To detect integer overflow or wraparound (CWE-190) vulnerabilities in Java using Mariana Trench, we need to specify the detection of tainted data flows that may cause these vulnerabilities. Mariana Trench's rules and models will help us define sources, propagations, and sinks that match the patterns leading to such vulnerabilities. Here is a detailed explanation based on the provided references from the Mariana Trench knowledge base    .

#### Step-by-Step Process

1. **Identify Common Sources of Tainted Data**:
   These include user inputs, network inputs, file reads, and other external data sources.

2. **Define Propagation Patterns**:
   This involves how tainted data can flow through the application. For integer overflow, we need to detect operations such as additions, subtractions, multiplications, and other arithmetic operations.

3. **Identify Sinks where Overflows Might Happen**:
   Sinks typically include variables holding critical values in arithmetic operations, method parameters expecting integer values, etc.

4. **Write Model Generators**:
   This involves specifying JSON model generators and corresponding rules. The models define what constitutes sources, propagations, and sinks.

#### Example SAST Rules and Models

##### Define the Source Models
We'll create source models for common tainted data sources:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "getText|read|parseInt" }
      ],
      "model": {
        "sources": [
          { "kind": "UserInput", "port": "Return" }
        ]
      }
    }
  ]
}
```

##### Propagation Model
We'll define propagation for methods that perform arithmetic operations:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "add|multiply|subtract|divide" }
      ],
      "model": {
        "propagation": [
          {
            "input": "Argument(0)",
            "output": "Return"
          },
          {
            "input": "Argument(1)",
            "output": "Return"
          }
        ]
      }
    }
  ]
}
```

##### Define the Sink Models
We'll identify sinks related to arithmetic operations and critical values handling:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "setValue|store|process" }
      ],
      "model": {
        "sinks": [
          { "kind": "CriticalValueSink", "port": "Argument(0)" }
        ]
      }
    }
  ]
}
```

##### Define the Rules
Finally, we’ll define the rules to catch the flow from sources to sinks, ensuring we detect potential integer overflow vulnerabilities:
```json
{
  "rules": [
    {
      "name": "UserInput flows into arithmetic operations",
      "code": 101,
      "description": "Detect potential integer overflow from user input",
      "sources": [
        "UserInput"
      ],
      "sinks": [
        "CriticalValueSink"
      ]
    }
  ]
}
```

### Considerations for Variations and Frameworks
- **Common Java Frameworks**: Include popular packages like `java.util`, `java.io`, `javax.servlet`, etc.
- **Anti-Patterns**: Identify specific frameworks' methods prone to misuse leading to overflows.
- **Integer Types**: Consider Java's `int`, `long`, and `BigInteger` types.
- **Arithmetic Operations**: Include direct operations and their chained calls or combined arithmetic functions.

### Review Examples for False Positives/Negatives Reduction
By leveraging examples from CWE-190 and testing against real-world applications, we can fine-tune our rules and models to reduce false positives and negatives, ensuring higher accuracy.

By following this structure, and continuously refining and testing the models and rules against various applications and frameworks, we can generate effective SAST rules to detect integer overflow or wraparound vulnerabilities in Java.

For more details on model configurations and examples, see the provided references    .