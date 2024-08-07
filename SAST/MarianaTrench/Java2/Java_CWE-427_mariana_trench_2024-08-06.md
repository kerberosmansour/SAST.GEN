ToTo write Mariana Trench SAST (Static Application Security Testing) rules for detecting the Uncontrolled Search Path Element vulnerability (CWE-427) in Java, we need to follow the steps to define methods as sources, sinks, and propagations in JSON format. This involves specifying the types of sources and sinks that could lead to such a vulnerability, such as classpaths and dynamic library loading methods. Also, we have to consider the relevant methods in popular Java frameworks and libraries.

Here is a comprehensive set of Mariana Trench SAST rules targeting the CWE-427 vulnerability:

### Sources

First, we need to specify possible sources of untrusted input like user inputs or environment variables.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {
              "constraint": "name",
              "pattern": "javax.servlet.http.HttpServlet"
            }
          }
        },
        {
          "constraint": "name",
          "pattern": "getParameter"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "UserInput",
            "port": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "getenv"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "java.lang.System"}}
      ],
      "model": {
        "sources": [
          {
            "kind": "EnvironmentVariable",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

### Sinks

Next, relevant sinks associated with dynamic loading in Java should be defined.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "loadLibrary"
        },
        {
          "constraint": "parent",
          "inner": {
            "constraint": "name",
            "pattern": "java.lang.System"
          }
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "DynamicLibraryLoading",
            "port": "Argument(1)"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "class\.forName"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "ClassLoading",
            "port": "Argument(1)"
          }
        ]
      }
    }
  ]
}
```

### Propagation

Lastly, we define how the untrusted inputs could propagate through the application.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "valueOf"
        },
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {
              "constraint": "name",
              "pattern": "java.lang.String"
            }
          }
        }
      ],
      "model": {
        "propagations": [
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

### Rule Definition

Finally, let's define the rule that catches flows from these sources to these sinks.

```json
{
  "rules": [
    {
      "name": "Uncontrolled Search Path Element",
      "code": 427,
      "description": "Potential uncontrolled search path element vulnerability (CWE-427)",
      "sources": [
        "UserInput",
        "EnvironmentVariable"
      ],
      "sinks": [
        "DynamicLibraryLoading",
        "ClassLoading"
      ]
    }
  ]
}
```

We instruct Mariana Trench to read from these custom model generators and update the `rules.json` with the new rule definition to capture flows that match this rule.

### Integration

To integrate this, these JSON rules need to be added to the model-generator configuration file and rules configuration:

1. Add JSON model generator definitions to the relevant configuration files.
2. Ensure the custom rules are added to `rules.json`.

These steps ensure that Mariana Trench will identify the data flow paths from sources to vulnerable sinks related to CWE-427 in Java frameworks accurately and efficiently.

For more details on writing model generators and rules, refer to the Mariana Trench documentation【4:0†source】  .