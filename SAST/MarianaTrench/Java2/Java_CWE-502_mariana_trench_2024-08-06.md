ToTo create Mariana Trench SAST rules for the Deserialization of Untrusted Data (CWE-502) vulnerability in Java, we will leverage the provided details to minimize false positives and false negatives. Here’s a step-by-step guide to drafting comprehensive rules:

1. **Identify Sources and Sinks:**
   - **Source**: Untrusted data that can be deserialized.
   - **Sink**: Methods that perform deserialization.

2. **Develop JSON Model Generators:**
   - We'll identify methods that are typically used for deserialization in Java, such as:
     - `java.io.ObjectInputStream.readObject()`
     - `java.beans.XMLDecoder.readObject()`
     - Libraries or frameworks that might provide deserialization methods, e.g., Jackson's `ObjectMapper.readValue()`.

3. **Write Custom Rules:**
   - Define new model generators to capture these sources and sinks.
   - Implement these rules in a JSON format compatible with Mariana Trench.

### Example JSON Model Generators and Rules

#### Model Generators

We need to create models to find deserialization calls. Here’s an example JSON configuration:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "readObject"
        },
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {
              "constraint": "name",
              "pattern": "java.io.ObjectInputStream"
            }
          }
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "DeserializationSink",
            "port": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "readObject"
        },
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {
              "constraint": "name",
              "pattern": "java.beans.XMLDecoder"
            }
          }
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "DeserializationSink",
            "port": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "readValue"
        },
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {
              "constraint": "name",
              "pattern": "com.fasterxml.jackson.databind.ObjectMapper"
            }
          }
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "DeserializationSink",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

#### Rules Configuration

After defining the model generators, we need to create a rule that captures flows from the source (where data comes from user input or network) to the deserialization methods (sinks).

```json
{
  "rules": [
    {
      "name": "Deserialization of Untrusted Data",
      "code": 502,
      "description": "Deserialization of untrusted data can lead to remote code execution or data tampering. This rule tracks untrusted sources to deserialization sinks.",
      "sources": [
        "UntrustedInput"
      ],
      "sinks": [
        "DeserializationSink"
      ]
    }
  ]
}
```

### Adding to Configuration
The above model generators and rules need to be added to the respective configuration files in Mariana Trench:
- Add the model generators JSON file to the model generators configuration path:
  - `configuration/model-generators/untrusted_deserialization.models`
- Add the rules JSON content to the existing `configuration/rules.json` or include it as a new rule file path.

### Verification
To ensure the rules are working correctly, you can execute Mariana Trench and check for any matches with the specified models and rules. Adjustments to verbosity can help debug any mismatches or issues.

#### Notes
- Always validate the models and rules with real application code for potential false positives and negatives.
- Keep the potential variations of the deserialization methods by adding more specific checks as needed.

By following these guidelines, you can effectively create focused and precise SAST rules using Mariana Trench to detect deserialization vulnerabilities in Java【4:0†source】【4:2†source】【4:6†source】【4:10†source】【4:12†source】【4:13†source】【4:15†source】【4:16†source】【4:17†source】【4:18†source】【4:19†source】.