###### Writing Mariana Trench SAST Rules for Integer Overflow or Wraparound (CWE-190) in Java

To effectively write SAST rules in Mariana Trench that focus on detecting Integer Overflow or Wraparound vulnerabilities in Java, follow these steps:

1. **Define the Methods to Scan:**
   Identify the methods where integer operations are carried out, specifically where inputs can be provided externally. This includes arithmetic operations that can result in overflows.

2. **Specify Sources and Sinks:**
   Sources will be user inputs or any data read from external or untrusted sources. Sinks will include the result of arithmetic operations that can cause overflows.

3. **Model Generation:**
   Use JSON model generators to define the methods and characteristics of both sources and sinks.

#### Example Model Generators JSON

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": ".*[^\\w]add.*|.*[^\\w]increment.*|.*[^\\w]multiply.*|.*[^\\w]divide.*|.*[^\\w]subtract.*"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "UserInput",
            "port": "Argument(0)"
          }
        ],
        "sinks": [
          {
            "kind": "ArithmeticOperation",
            "port": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {
              "constraint": "name",
              "pattern": "InputStream|Reader|BufferedReader|ServletRequest|HttpServletRequest"
            }
          }
        },
        {
          "constraint": "name",
          "pattern": "read|readLine|next|nextInt|nextDouble|nextLong|nextShort"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "ExternalInput",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

This JSON model generator defines various methods and parameters as sources and sinks based on the pattern of the method names and the classes they belong to.

#### Add Custom Rules

To add custom rules, you need to specify them in `rules.json`.

```json
{
  "rules": [
    {
      "name": "Integer Overflow Detection",
      "code": 190,
      "description": "Detection of potential integer overflows or wraparounds in arithmetic operations.",
      "sources": [
        "UserInput",
        "ExternalInput"
      ],
      "sinks": [
        "ArithmeticOperation"
      ]
    }
  ]
}
```

This JSON rule specifies that we want to detect flows from sources labeled as `UserInput` or `ExternalInput` to sinks labeled as `ArithmeticOperation`.

### Steps to Integrate the Rule

- **Create JSON Model Files:** Add the above JSON model generators into files with the `.models` extension and place them in the appropriate directory for Mariana Trench to find them.
- **Update Generator Config:** Ensure these model generator files are referenced in the `default_generator_config.json`.
- **Add Rules:** Add your rule JSON to the `rules.json` file so that Mariana Trench knows to look for these specific flows during analysis.

### Effectiveness Notes

- **High Precision (Low False Positive):** By narrowing down the method patterns and class types, the rules are designed to focus on places where integer overflows are likely, thus reducing false positives.
- **Detection Scope (Low False Negative):** The rule scans various typical input methods and arithmetic operation methods ensuring a broad detection capability.

### Verification

To verify that the model generator and rules are correctly processed:

1. **Run Analysis**: Execute Mariana Trench with verbosity settings to ensure the generator matches methods correctly:
   ```json
   {
     "model_generators": [
       {
         "find": "methods",
         "where": /* criteria */,
         "model": { /* model details */ },
         "verbosity": 1
       }
     ]
   }
   ```
   This will print matching methods during analysis.

2. **Inspect Output Models**: Check that the output models include the expected sources and sinks using `grep` commands. For example:
   ```sh
   grep SourceKind models@*
   ```

### Conclusion

Implementing these steps with the provided examples ensures that Integer Overflow or Wraparound cases are methodically identified in Java code using Mariana Trench, maintaining a balance between high detection accuracy and minimal false positives.

   