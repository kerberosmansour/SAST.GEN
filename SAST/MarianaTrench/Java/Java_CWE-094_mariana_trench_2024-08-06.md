###### Create Mariana Trench Rules for CWE-094 (Code Injection)

#### 1. Context Review

Reviewing the guidelines and best practices for writing Mariana Trench rules involves focusing on the structure, metadata usage, and relevant constructs specific to Java. This includes understanding sources, sinks, propagation rules, and shims within the context of the framework being used.

#### 2. Vulnerability Analysis

***CWE-094: Improper Control of Generation of Code ('Code Injection') in Java***

**Manifestations:**
- User-controlled input being executed as code (RCE - Remote Code Execution)
- Java Reflection API (e.g., `Class.forName`, `Method.invoke`)
- Script execution engines (e.g., `javax.script.ScriptEngineManager`)
- Dynamic language libraries (e.g., Apache Groovy)

**Common Coding Patterns:**
- Direct execution of user input
- Constructing code snippets from user input
- Use of dynamic class loading based on user input
- Reflective calls on classes/methods with user input as parameters

#### 3. Mariana Trench Rule Creation

Here, we will create the rules focusing on the `sources`, `sinks`, and `propagations`.

1. **Sources Definitions**:
   - Assume user input can come from `HttpServletRequest.getParameter()`, `HttpServletRequest.getReader()`, and similar methods.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "getParameter|getReader|getQueryString"
        },
        {
          "constraint": "parent",
          "pattern": "HttpServletRequest"
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
    }
  ]
}
```

2. **Sink Definitions**:
   - Identify key points where code injection might manifest, such as through `Runtime.exec()`, `ProcessBuilder.start()`, reflective invocations, script engine evaluations.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "exec|start|forName|loadClass|invoke|eval"
        },
        {
          "constraint": "parent",
          "pattern": "Runtime|ProcessBuilder|Class|Method|ScriptEngine"
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

3. **Propagation Rules**:
   - Methods can propagate tainted data from their input to their output or other outputs.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "call|actionPerformed|service|doGet|doPost|processRequest"
        },
        {
          "constraint": "parent",
          "pattern": ".*"
        }
      ],
      "model": {
        "propagation": {
          "input": "Argument(0)",
          "output": "Return"
        }
      }
    }
  ]
}
```

4. **Rules**:
   - Define the rule to catch the flow from `UserInput` sources to `CodeExecution` sinks.

```json
{
  "rules": [
    {
      "name": "User input flows into code execution (Code Injection)",
      "code": 1,
      "description": "Values from user-controlled source may eventually flow into code execution",
      "sources": [
        "UserInput"
      ],
      "sinks": [
        "CodeExecution"
      ]
    }
  ]
}
```

#### 4. Testing and Validation

**Test Cases**:

1. Simple Case:
    ```java
    public void execute(HttpServletRequest request) throws Exception {
        String input = request.getParameter("cmd");
        Runtime.getRuntime().exec(input); // This should be flagged
    }
    ```

2. Reflection:
    ```java
    public void invokeMethod(HttpServletRequest request) throws Exception {
        String className = request.getParameter("className");
        String methodName = request.getParameter("methodName");
        Class<?> clazz = Class.forName(className);
        Method method = clazz.getMethod(methodName);
        method.invoke(clazz.newInstance()); // This should be flagged
    }
    ```

3. Scripting:
    ```java
    public void executeScript(HttpServletRequest request) throws Exception {
        String script = request.getParameter("script");
        ScriptEngineManager manager = new ScriptEngineManager();
        ScriptEngine engine = manager.getEngineByName("groovy");
        engine.eval(script); // This should be flagged
    }
    ```

**Validation Strategy**:
- Use the Mariana Trench query console or GitHub Code Scanning to run these rules against different Java/Android projects.
- Validate that the rules catch all potential code injections with minimal false positives.

By following this structured approach, you ensure the created rules provide a strong balance minimizing both false positives and false negatives while leveraging the detailed capabilities of Mariana Trench's taint analysis framework【4:0†source】【4:2†source】【4:3†source】【4:7†source】【4:9†source】.