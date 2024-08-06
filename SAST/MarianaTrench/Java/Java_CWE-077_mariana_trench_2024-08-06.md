###### Creating Mariana Trench SAST Rules for Command Injection Vulnerability

---

#### **1. Context Review**
The Mariana Trench static analysis platform follows a structured approach for writing rules:

1. **Specify Models & Model Generators:** Models describe methods or fields as sources, sinks, or propagations. Models are usually defined in JSON based on the Domain-Specific Language (DSL).
2. **Rules Definition:** Rules describe data flows to catch specific vulnerabilities.

A comprehensive rule definition includes:
- **Sources:** Entry points for taint (e.g., user inputs)
- **Sinks:** Critical points where taint needs to be flagged (e.g., code execution functions)
- **Propagations:** How taint flows through the codebase
- **Sanitizers:** Methods that neutralize or sanitize taint

#### **2. Vulnerability Analysis**
**Vulnerability Description:** Improper Neutralization of Special Elements used in a Command ('Command Injection'), CWE-077.

Common usage patterns leading to command injection involve:
- Passing user input directly to command execution methods without sanitization.
- Popular Java methods include `Runtime.exec()`, `ProcessBuilder.start()`.

#### **3. Mariana Trench Rule Creation**
Here's a set of Mariana Trench rules that might help detect command injection vulnerabilities:

**a. Source Definitions:**
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "doGet|doPost|doPut|doDelete"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "UserInput",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```
- **Explanation:** Identifies servlet methods commonly receiving user input【4:0†source】.

**b. Sink Definitions:**
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "exec|start"
        },
        {
          "constraint": "parent",
          "pattern": "java/lang/Runtime|java/lang/ProcessBuilder"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "CommandExecution",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```
- **Explanation:** Identifies critical APIs used for command execution where tainted data might cause command injection【4:0†source】【4:8†source】.

**c. Propagation Definitions:**
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "has_annotation",
          "pattern": "RequestMapping"
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
- **Explanation:** Captures propagation of user input through methods annotated with `@RequestMapping`【4:0†source】【4:8†source】【4:16†source】.

**d. Rule Definition:**
```json
{
  "name": "User input flows into command execution",
  "code": 101,
  "description": "User input flows into methods that execute system commands.",
  "sources": [
    "UserInput"
  ],
  "sinks": [
    "CommandExecution"
  ]
}
```
- **Explanation:** This rule ties together the defined sources and sinks to flag tainted data flows from user inputs to command execution methods【4:0†source】【4:8†source】【4:16†source】.

---

#### **4. Testing and Validation**

**Test Cases:**

1. **Positive Test Case:**
   ```java
   public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
       String userInput = request.getParameter("cmd");
       Runtime.getRuntime().exec(userInput);
   }
   ```
   - **Expected Result:** The rule should flag the `exec()` call as receiving tainted data from `request.getParameter()`.

2. **Negative Test Case:**
   ```java
   public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
       String userInput = request.getParameter("cmd");
       String sanitizedInput = sanitize(userInput);
       Runtime.getRuntime().exec(sanitizedInput);
   }
   public String sanitize(String input) {
       // Implement input sanitization logic
       return input;
   }
   ```
   - **Expected Result:** The rule should not flag the `exec()` call if proper sanitization is identified.

3. **Edge Case:**
   ```java
   public String complexProcessing(String input) {
       // Complex logic manipulating user input
       return input + "processed";
   }
   public void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
       String userInput = request.getParameter("cmd");
       String processedInput = complexProcessing(userInput);
       Runtime.getRuntime().exec(processedInput);
   }
   ```
   - **Expected Result:** The rule should correctly trace taint through the `complexProcessing` method to the `exec()` call.

---

**Validation Process:**
1. **Mariana Trench Query Console:**
   - Use the query console to inspect how taint is flowing through the codebase based on defined rules.
2. **Code Scanning with GitHub:**
   - Integrate with GitHub Code Scanning to automatically check for command injection vulnerabilities across codebases.
3. **Adjust Heuristics:**
   - Fine-tune heuristics parameters to balance false positives and negatives based on real-world data flows【4:0†source】【4:8†source】【4:16†source】【4:19†source】.

By following these steps and using the provided configurations, you should be able to effectively create and validate Mariana Trench rules to detect command injection vulnerabilities with high accuracy.