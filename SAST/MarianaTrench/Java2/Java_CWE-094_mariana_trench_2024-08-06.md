ToTo generate a set of Mariana Trench SAST rules for detecting Improper Control of Generation of Code ('Code Injection') (CWE-094) in Java, we will follow a structured approach based on the guidance provided in the Mariana Trench documentation. Here is a step-by-step method to define sources, sinks, and rules.

## Step-by-Step Method

### 1. Defining Sources
Sources in the context of CWE-094 could include any point where user input is introduced into the application. This can be via HTTP requests, database queries, file inputs, etc. Below are JSON model generators to define typical sources.

#### Example Source from HTTP Requests
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "getParameter"
        },
        {
          "constraint": "parent",
          "pattern": "javax.servlet.http.HttpServletRequest"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "UserControlled",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

### 2. Defining Sinks
Sinks for code injection in Java commonly include places where code might be dynamically executed, such as calls to `Runtime.exec()`, `ProcessBuilder.start()`, `ScriptEngine.eval()`, etc.

#### Example Sink for Dynamic Code Execution
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "exec"
        },
        {
          "constraint": "parent",
          "pattern": "java.lang.Runtime"
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
    }
  ]
}
```

### 3. Combining Sources and Sinks into Rules
A rule ties together the defined sources and sinks to detect the flow of potentially unsafe data from the source to the sink. 

```json
{
  "name": "User input flows into code execution (Code Injection)",
  "code": 1,
  "description": "Values from user-controlled source may eventually flow into code execution methods",
  "sources": [
    "UserControlled"
  ],
  "sinks": [
    "CodeExecution"
  ]
}
```

### 4. Specific Rules for Popular Frameworks
In a Java context, typical frameworks may include Spring, Hibernate, and Apache Struts. Below are some examples tailored to such frameworks.

#### Source from Spring Controller
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "parent",
          "pattern": "org.springframework.web.bind.annotation.RequestMapping"
        },
        {
          "constraint": "parameter",
          "inner": {
            "constraint": "type",
            "kind": "extends",
            "name": "javax.servlet.http.HttpServletRequest"
          }
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "UserControlled",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```

#### Sink in Apache Struts
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "parent",
          "pattern": "com.opensymphony.xwork2.ActionSupport"
        },
        {
          "constraint": "name",
          "pattern": "execute"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "CodeExecution",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

### Conclusion
Follow these steps to generate comprehensive, framework-specific SAST rules that should provide high accuracy in detecting potential code injection vulnerabilities. Always tailor your models to the specific methods and frameworks used in your environment to minimize false positives and false negatives.

For further information, the Mariana Trench documentation provides additional details on customizing sources, sinks, and rules【4:0†source】   .