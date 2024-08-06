###### Writing SAST Rules for SQL Injection in Java Using Mariana Trench

Based on the provided information in the file `'KnowledgeBase/Mariana_Trench.md'`, we'll create a set of Specific and Generalized SAST rules to capture SQL Injection vulnerabilities in Java. These rules will target different Java frameworks and highlight the stages at which a security lapse might occur.

#### Rule Strategy

1. **Define Sources:** Identify points of user input.
2. **Define Sinks:** Identify the database interaction points where the input could become a security threat.
3. **Create Rules:** Define how data flows from sources to sinks.

#### Example Rule Implementation for Popular Java Frameworks

- **Spring Framework**
- **JDBC**
- **Hibernate**

Here is an example of how you might configure the rules for SQL Injection detection:

### JSON Configuration

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": ".*Controller.*"},
        { "constraint": "name", "pattern": ".*Service.*"}
      ],
      "model": {
        "sources": [
          { "kind": "UserProvidedInput", "port": "Argument(0)" }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "executeQuery|prepareStatement|createQuery|createNativeQuery" },
        { "constraint": "parent", "inner": { "constraint": "extends", "inner": { "constraint": "name", "pattern": "JdbcTemplate|EntityManager|Session" }, "include_self": true } }
      ],
      "model": {
        "sinks": [
          { "kind": "SQLSink", "port": "Argument(0)" }
        ]
      }
    }
  ],
  "rules": [
    {
      "name": "SQL Injection",
      "code": 101,
      "description": "Potential SQL Injection detected.",
      "sources": [
        "UserProvidedInput"
      ],
      "sinks": [
        "SQLSink"
      ]
    }
  ]
}
```

#### Explanation
1. **Sources**:
   - **User Input** (`UserProvidedInput`): Inputs typically come from controllers and services in the form of method arguments. The generic pattern `.*Controller.*` and `.*Service.*` is used to match common names of controller or service classes where inputs are received.

2. **Sinks**:
   - **Spring JDBC Template** (`JdbcTemplate`): Methods like `executeQuery`, `prepareStatement` can be dangerous if improperly handled.
   - **Hibernate EntityManager** (`EntityManager`, `Session`): Methods like `createQuery`, `createNativeQuery` are potential sinks.

3. **Rules**:
   - The rule named `"SQL Injection"` (code `101`) specifies that any data flow from `UserProvidedInput` to `SQLSink` should be flagged as a potential SQL Injection vulnerability.

### Final Considerations
For high precision (low false positives) and high recall (low false negatives):
- **Precision Improvements**:
  - Add more specific method and class constraints based on known secure practices.
  - Apply filters and features such as input sanitization checks or use parameterized query checks.

- **Recall Improvements**:
  - Ensure all potential sources and sinks are comprehensively listed, including custom query builders.
  - Update models to include new frameworks or APIs as they are adopted.

By carefully engineering these rules and iterating based on analysis results, one can maintain a robust security posture against SQL Injection vulnerabilities in Java applications.

This example covers a single vulnerability; for complete coverage, similar detailed rules would need to be written for other common vulnerabilities and frameworks.

### Citations
This configuration strategy and framework-specific guidance were based on detailed references provided from the given `Mariana_Trench.md` document     .