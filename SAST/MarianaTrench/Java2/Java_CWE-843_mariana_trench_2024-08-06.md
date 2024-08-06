ToTo write effective Mariana Trench SAST rules for detecting **Access of Resource Using Incompatible Type ('Type Confusion') (CWE-843) in Java**, we need to focus on identifying sources (where unsafe or incorrect types might come from) and sinks (where these values get used improperly). The steps involve:

1. **Identify Sources:**
   - These would be methods or APIs that can provide data of an inappropriate or untrusted type.
   - Common sources can be deserialization methods, user inputs, or external libraries, whose output type might be unchecked.

2. **Identify Sinks:**
   - These are places where the type confusion vulnerability can be exploited. Such sinks include methods or operations that expect objects of a certain type.
   - Common sinks can be method parameters where the type is presumed to be safe.

### Example Sources:
1. Unchecked deserialization methods.
2. Methods returning objects casted from a more generic type (like `Object`).

### Example Sinks:
1. Methods that use the potentially confused types without proper checks.
2. Java Reflection API usage where the type is assumed to be a specific class type.

Using the guidelines and examples from Mariana Trench's documentation, we can write the JSON rules as follows:

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "deserialize|readObject|UnsafeInput"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "TypeConfusionSource",
            "port": "Return"
          },
          {
            "kind": "TypeConfusionSource",
            "port": "Argument(0)"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "cast|asSubclass|getField|getMethod"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "TypeConfusionSink",
            "port": "Argument(0)"
          },
          {
            "kind": "TypeConfusionSink",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

### Rules:
To detect flows from `TypeConfusionSource` to `TypeConfusionSink`, the relevant rule would be:

```json
{
  "name": "Type Confusion Vulnerability",
  "code": 843,
  "description": "Values from a source of type confusion may flow into a critical method leading to type mismatch.",
  "sources": [
    "TypeConfusionSource"
  ],
  "sinks": [
    "TypeConfusionSink"
  ]
}
```

### Detailed Points:
1. **Sources**: We define sources as methods that can potentially give rise to type confusion, like deserialization or unsafe object creation methods.
2. **Sinks**: Sinks are defined at points where these potentially unsafe types are used without verification (e.g., casting methods or reflective calls).
3. **Rule Explanation**: The rule ties a source (`TypeConfusionSource`) to a sink (`TypeConfusionSink`), facilitating Mariana Trench to flag instances where such type confusions could lead to vulnerabilities.

Ensure to include details about configurations, as mentioned in the Mariana Trench guidelines.
- Update the `rules.json` and `model-generators` configuration to recognize these models and rules in your analysis setup.

For further refining:
- Test these rules on sample code bases that purposely include type confusion vulnerabilities to fine-tune the detection and reduce false positives and negatives.

References:
- Customizing models and rules setup【4:0†source】  

This approach should help in achieving a high precision (low false positives) and recall (low false negatives) in identifying type confusion vulnerabilities in Java applications using Mariana Trench.