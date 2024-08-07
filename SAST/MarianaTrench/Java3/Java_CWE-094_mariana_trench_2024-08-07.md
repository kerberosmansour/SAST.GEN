###### Writing Mariana Trench SAST Rules for "Improper Control of Generation of Code ('Code Injection')" (CWE-094) in Java

To generate effective Static Application Security Testing (SAST) rules for detecting "Improper Control of Generation of Code ('Code Injection')" (CWE-094) in Java using Mariana Trench, we need to:
1. Identify potential sources where tainted data may enter the application.
2. Identify sinks that can lead to code injection if tainted data reaches them.
3. Write model generators to create these sources and sinks.
4. Define the rules specifying the taint flow from sources to sinks.

We will keep false positives and negatives low by specifying exact matches and common patterns in popular Java frameworks.

#### Step 1: Identify Sources
Sources of tainted data usually include user inputs or any uncontrolled, potentially harmful data entering the application. In Java, these could include:
- HTTP request parameters
- User inputs from graphical UI
- Data from untrusted files

#### Step 2: Identify Sinks
Sinks are where the code evaluation or execution happens, such as:
- Methods/classes that compile or evaluate Java code at runtime (e.g., `javax.script.ScriptEngine` and `java.lang.reflect.Method.invoke`).

#### Step 3: Writing Model Generators for Sources and Sinks

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "signature_pattern",
          "pattern": "Ljavax/servlet/http/HttpServletRequest;->getParameter(Ljava/lang/String;)Ljava/lang/String;"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "UserControlledInput",
            "port": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "signature_pattern",
          "pattern": "Ljavax/servlet/http/HttpServletRequest;->getParameterValues(Ljava/lang/String;)[Ljava/lang/String;"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "UserControlledInput",
            "port": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "signature_pattern",
          "pattern": "Ljavax/script/ScriptEngine;->eval(Ljava/lang/String;)Ljava/lang/Object;"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "CodeExecution",
            "port": "Argument(0)"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "constraint": "signature_pattern",
          "pattern": "Ljava/lang/reflect/Method;->invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "CodeExecution",
            "port": "Argument(1)"
          }
        ]
      }
    }
  ]
}
```

#### Step 4: Define the Rule

```json
{
  "rules": [
    {
      "name": "User controlled input flows into code execution",
      "code": 1001,
      "description": "User-controlled input reaches code execution, leading to potential code injection vulnerability",
      "sources": [
        "UserControlledInput"
      ],
      "sinks": [
        "CodeExecution"
      ]
    }
  ]
}
```

### Explanation:

1. **Model Generators for Sources**
   - We capture user input from `HttpServletRequest.getParameter()` and `HttpServletRequest.getParameterValues()`, marking their return values as a source of type `UserControlledInput`.

2. **Model Generators for Sinks**
   - We identify methods like `ScriptEngine.eval()` and `Method.invoke()` where the data can be executed as code. Hence, we mark the relevant arguments of these methods as sinks of type `CodeExecution`.

3. **Rule Definition**
   - This rule tracks the taint flow from sources of type `UserControlledInput` to sinks of type `CodeExecution`. If any path is found where a user-controlled input reaches a code execution sink, it will flag this as a potential code injection vulnerability.

By specifying exact method signatures and considering common attack vectors in Java, this approach ensures the rules cover various possible sources and sinks, balancing between false positives and negatives effectively   .