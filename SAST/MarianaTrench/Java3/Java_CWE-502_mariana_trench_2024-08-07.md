###### Writing Mariana Trench SAST Rules for Deserialization of Untrusted Data (CWE-502) in Java

The goal is to create detailed Source-to-Sink (S2S) rules for identifying and mitigating the risks of CWE-502 in Java applications using Mariana Trench. We'll outline several source and sink models applicable to popular frameworks and libraries.

#### Source Models

1. **JDK/Standard Library:**
    - Any method that reads and converts a serialized object back into its original form should be considered a source of untrusted data.
    ```json
    {
      "model_generators": [
        {
          "find": "methods",
          "where": [
            {"constraint": "name", "pattern": "readObject"},
            {"constraint": "parent", "pattern": "java/io/ObjectInputStream"}
          ],
          "model": {
            "sources": [
              {"kind": "DeserializationInput", "port": "Return"}
            ]
          }
        },
        {
          "find": "methods",
          "where": [
            {"constraint": "name", "pattern": "readUnshared"},
            {"constraint": "parent", "pattern": "java/io/ObjectInputStream"}
          ],
          "model": {
            "sources": [
              {"kind": "DeserializationInput", "port": "Return"}
            ]
          }
        }
      ]
    }
    ```

2. **Apache Commons:**
    - For Apache Commons’ `SerializationUtils`, the `deserialize` method reads serialized data and should be flagged.
    ```json
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "deserialize"},
        {"constraint": "parent", "pattern": "org/apache/commons/lang3/SerializationUtils"}
      ],
      "model": {
        "sources": [
          {"kind": "DeserializationInput", "port": "Return"}
        ]
      }
    }
    ```

3. **Spring Framework:**
    - The method `fromMessage` in `DefaultJmsMessageConverter` converts serialized data in messages and should be marked as potentially dangerous.
    ```json
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "fromMessage"},
        {"constraint": "parent", "pattern": "org/springframework/jms/support/converter/DefaultJmsMessageConverter"}
      ],
      "model": {
        "sources": [
          {"kind": "DeserializationInput", "port": "Return"}
        ]
      }
    }
    ```

#### Sink Models

Considering the nature of deserialization vulnerabilities, common sinks are methods or frameworks that execute or manipulate the deserialized data in ways that could lead to dangerous behavior.

1. **Execution Methods:**
    - Methods that execute code or modify system/internal state based on inputs should be categorized as sinks.
    ```json
    {
      "model_generators": [
        {
          "find": "methods",
          "where": [
            {"constraint": "name", "pattern": "exec"},
            {"constraint": "parent", "pattern": "java/lang/Runtime"}
          ],
          "model": {
            "sinks": [
              {"kind": "RemoteCodeExecution", "port": "Argument(0)"}
            ]
          }
        },
        {
          "find": "methods",
          "where": [
            {"constraint": "name", "pattern": "load"},
            {"constraint": "parent", "pattern": "java/lang/System"}
          ],
          "model": {
            "sinks": [
              {"kind": "DynamicCodeLoading", "port": "Argument(0)"}
            ]
          }
        }
      ]
    }
    ```

3. **Spring Web:**
    - Controllers or service methods taking deserialized data as parameters can be significant sinks.
    ```json
    {
      "find": "methods",
      "where": [
        {"constraint": "name_pattern", "pattern": ".*"},
        {"constraint": "parent", "pattern": "org/springframework/.*Controller"}
      ],
      "model": {
        "sinks": [
          {"kind": "SpringMVC", "port": "Argument(0)"}
        ]
      }
    }
    ```

#### Defining Rules

Once the sources and sinks are defined, we need to connect these points with appropriate rules. These rules will focus on tracking the flow of data from deserialization inputs to potential dangerous sinks.

```json
{
  "rules": [
    {
      "name": "Deserialization of Untrusted Data leading to Remote Code Execution",
      "code": "CWE-502-RCE",
      "description": "Untrusted deserialization flow from source to sink that leads to RCE",
      "sources": [
        "DeserializationInput"
      ],
      "sinks": [
        "RemoteCodeExecution",
        "DynamicCodeLoading",
        "SpringMVC"
      ]
    }
  ]
}
```

### Conclusion

By leveraging the capabilities of Mariana Trench to define customized sources, sinks, and rules, we can effectively detect and mitigate risks associated with the deserialization of untrusted data in Java applications. Monitoring the flow from source points where data are deserialized to sink points where they can influence the system/state helps in pinpointing vulnerabilities with higher accuracy and lesser false positives/negatives.

For more detailed steps and examples on defining and working with Mariana Trench models, see the relevant sections on model generators and rule definitions【10:0†source】 .