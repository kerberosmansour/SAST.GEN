###### Writing Mariana Trench SAST Rules for CWE-843 in Java

#### Overview

Creating effective static application security testing (SAST) rules involves identifying potential sources, sinks, and paths of data propagation that could lead to vulnerabilities. For CWE-843 (Type Confusion) in Java, the goal is to detect cases where a resource is accessed using an incompatible type, potentially leading to unintended behavior or security issues.

Mariana Trench allows defining sources and sinks and specifying rules to catch specific taint flows through JSON configurations  . The following sections outline the steps and JSON configurations required to create SAST rules to identify variations of Type Confusion in Java.

### Defining the Model Generators

To begin, we will define a model generator to identify methods in various popular frameworks that could potentially lead to type confusion. 

#### Example Model Generator
The model generator identifies methods with certain signatures that are likely sources or sinks of type confusion.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "signature_match",
          "pattern": ".*\\.getParameter(String)"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "TypeConfusionSource",
            "port": "Return"
          }
        ],
        "sinks": [
          {
            "kind": "TypeConfusionSink",
            "port": "Argument(1)"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "signature_match",
          "pattern": ".*\\.getAttribute(String)"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "TypeConfusionSource",
            "port": "Return"
          }
        ],
        "sinks": [
          {
            "kind": "TypeConfusionSink",
            "port": "Argument(1)"
          }
        ]
      }
    }
  ]
}
```

This generator targets specific method signatures (`getParameter` and `getAttribute`), marking their return values as sources of type confusion and identifying potential sinks where such sources are used.

### Defining the Rules

The next step is to define rules that describe the flow from sources to sinks which can lead to type confusion vulnerabilities.

#### Example Rules 
The rules define flows from identified sources to sinks and assign a specific code and description.

```json
{
  "rules": [
    {
      "name": "Type Confusion Source to Sink",
      "code": 1001,
      "description": "Type Confusion vulnerability: A resource is accessed using an incompatible type.",
      "sources": [
        "TypeConfusionSource"
      ],
      "sinks": [
        "TypeConfusionSink"
      ]
    }
  ]
}
```

### Verbosity & Debugging

To ensure the model generators are working correctly, use high verbosity in the model to troubleshoot and verify that methods are being captured  . 

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [ /* constraints */ ],
      "model": {
        /* model definition */
      },
      "verbosity": 1
    }
  ]
}
```

### Heuristics and Collapsing
Consider configuring heuristic parameters and collapsing for performance optimization and precision  :

#### Example Heuristics Configuration:

```json
{
    "join_override_threshold": 100,
    "android_join_override_threshold": 100,
    "generation_max_port_size": 10,
    "generation_max_output_path_leaves": 30,
    "parameter_source_max_port_size": 10,
    "parameter_source_max_output_path_leaves": 30,
    "sink_max_port_size": 10,
    "sink_max_input_path_leaves": 30,
    "call_effect_source_max_port_size": 10,
    "call_effect_source_max_output_path_leaves": 30,
    "call_effect_sink_max_port_size": 10,
    "call_effect_sink_max_input_path_leaves": 30,
    "max_number_iterations": 300,
    "max_depth_class_properties": 30,
    "max_call_chain_source_sink_distance": 30,
    "propagation_max_input_path_size": 10,
    "propagation_max_input_path_leaves": 10
}
```

### Conclusion

By following these guidelines and using the provided JSON examples, you can create effective SAST rules for detecting type confusion issues in Java, ensuring robust application security with minimal false positives and negatives. These rules will help identify any misuse of object types which could lead to dangerous vulnerabilities.