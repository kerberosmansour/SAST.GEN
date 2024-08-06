###### Mariana Trench SAST Rules for Cross-Site Request Forgery (CSRF) in Java

#### 1. **Context Review**

The provided documentation explains guidelines for creating sources, sinks, and other constructs for writing rules in Mariana Trench. Here are some key points:

- **Sources and Sinks**: Sources denote the entry points of tainted data, while sinks represent the dangerous function calls where taint should not reach .
- **Model Generators**: These are JSON files specifying patterns to identify methods as sources or sinks   .
- **Rules**: Defined in `rules.json`, specifying taint flows from sources to sinks   .
- **Taint Propagation**: Defines how taint can spread through methods, specifying input-output relationships  .
- **Attach_to constructs**: Advanced features to aid in accurate taint analysis by attaching conditions to sources, sinks, and propagations   .
  
#### 2. **Vulnerability Analysis: Cross-Site Request Forgery (CSRF)**

Cross-Site Request Forgery (CSRF) (CWE-352) is a vulnerability that allows malicious websites to perform actions on behalf of an authenticated user on another site. In Java web applications, this typically manifests through unprotected endpoints or methods that perform state-changing operations without verifying the origin of the request.

#### 3. **Mariana Trench Rule Creation**

##### Source Definitions

These represent where the tainted data (potential CSRF tokens) might enter the application.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "^getParameter$"
        },
        {
          "constraint": "within_class",
          "prefix": "javax.servlet.http.HttpServletRequest"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "UntrustedRequestParameter",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

##### Sink Definitions

These indicate where the vulnerability can manifest, typically via state-changing methods that do not validate CSRF tokens.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": ".*"},
        {"constraint": "within_file", "pattern": "Controller"}
      ],
      "model": {
        "sinks": [
          {
            "kind": "CSRFDangerousOperation",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```

##### Propagation Definitions

These rules define how taint could propagate through methods, for instance, how a tainted request parameter might propagate to a dangerous method call.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "^processRequest$"},
        {"constraint": "within_file", "pattern": ".*Controller"}
      ],
      "model": {
        "propagation": [
          {
            "input": "Argument(0)",
            "output": "Return"
          }
        ]
      }
    }
  ]
}
```

##### Rule Definitions

Bringing it all together, the rule definition specifying the flow from sources to sinks.

```json
{
  "rules": [
    {
      "name": "Detect CSRF Vulnerability",
      "code": 1001,
      "description": "Detect potential CSRF vulnerabilities",
      "sources": ["UntrustedRequestParameter"],
      "sinks": ["CSRFDangerousOperation"]
    }
  ]
}
```

#### 4. **Testing and Validation**

##### Test Cases

1. **Typical CSRF Scenario:**
    - **Code**:
    ```java
    @Servlet
    public class ExampleController {
        protected void doPost(HttpServletRequest request, HttpServletResponse response) {
            String token = request.getParameter("csrf_token");
            // Potentially dangerous operation without CSRF token validation
            updateData(token);
        }
    }
    ```

2. **Non-CSRF Safe Method:**
    - **Code**:
    ```java
    @WebServlet
    public class AnotherController {
        protected void doGet(HttpServletRequest request, HttpServletResponse response) {
            String id = request.getParameter("id");
            executeDangerousOperation(id);
        }
    }
    ```

##### Test Strategy

- **Unit Tests**: Create mock servlets and controllers to simulate scenarios where CSRF might occur and verify rule detection.
- **Integration Tests**: Deploy the application in a controlled environment with CSRF testing tools (like OWASP ZAP) to see if the rules successfully detect vulnerabilities.
- **Mariana Trench Console**: Use the query console to simulate running the rules against the codebase, inspecting the logs to ensure correct source-sink mappings.
- **GitHub Code Scanning**: Integrate rules as part of CI pipeline for continuous validation against new code changes.

This approach ensures thorough coverage by defining possible entry points (sources), dangerous operations (sinks), propagation rules, and validating through comprehensive testing strategies, thus minimizing false positives and negatives.