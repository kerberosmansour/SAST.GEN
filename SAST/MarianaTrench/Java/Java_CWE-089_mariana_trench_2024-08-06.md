###### Generating Mariana Trench SAST Rules for SQL Injection (CWE-089) in Java

#### 1. Context Review

To define effective SAST (Static Application Security Testing) rules for detecting SQL Injection vulnerabilities in Java using Mariana Trench, we need to focus on several key components as drawn from the documentation:

1. **Sources**: The origins of tainted data (e.g., user inputs).
2. **Sinks**: Functions or methods where tainted data should not flow into (e.g., SQL execution methods).
3. **Propagations**: How tainted data can be transferred from one location to another within the code (e.g., through method calls and object properties).
4. **Sanitizers**: Methods that can cleanse or neutralize the taint.

The general structure for writing Mariana Trench rules includes defining these in JSON format within model generators. The rules need to encapsulate finding specific methods or fields where the taint (unsafe data flow) might be present, specifying the taint sources, sinks, and how taint might propagate through various methods.

#### 2. Vulnerability Analysis

##### SQL Injection (CWE-089) in Java

**Common Sources**:
- User inputs via HTTP request parameters, servlet inputs, and other forms of input 
  ```java
  HttpServletRequest request = ...;
  String userInput = request.getParameter("input");
  ```

**Common Sinks**:
- Methods executing SQL commands directly using concatenated strings
  ```java
  Statement statement = connection.createStatement();
  ResultSet resultSet = statement.executeQuery("SELECT * FROM users WHERE userID = '" + userInput + "';");
  ```

**Common Sanitizers**:
- Parameterized queries or prepared statements
  ```java
  PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM users WHERE userID = ?");
  preparedStatement.setString(1, userInput);
  ```

**Propagation Paths**:
- Methods passing user input to other methods or services, potentially altering it
  ```java
  public String getUserID(HttpServletRequest request) {
      return request.getParameter("input");
  }
  ```

#### 3. Mariana Trench Rule Creation

We will create rules to detect tainted flows from the sources (user inputs) to sinks (SQL execution methods) while considering any propagation steps in between.

**Example Mariana Trench Rules JSON**:

```json
[
  {
    "name": "Detect SQL Injection",
    "code": 1001,
    "description": "Flow of user input to SQL execution methods causing potential SQL Injection vulnerability",
    "sources": [
      {
        "kind": "UserInput",
        "port": "Argument(1)"
      }
    ],
    "sinks": [
        {
          "kind": "SQLExecution",
          "port": "Argument(0)"
        }
    ],
    "propagations": [
      {
        "propagation": [
          {
            "input": "Argument(0)",
            "output": "Return"
          }
        ]
      }
    ],
    "sanitizers": [
      {
        "sanitize": "sources",
        "kinds": [
          {
            "kind": "PreparedStatements"
          }
        ]
      }
    ]
  }
]
```

**Explanation:**
1. **Sources**: 
   - Defined as input from user-related sources.
   - `HttpServletRequest.getParameter` is a common source in web applications.
   
2. **Sinks**:
   - Direct execution of SQL Commands via `Statement.executeQuery(String)` or similar methods.

3. **Propagations**:
   - How taint could travel from input methods to SQL execution methods.

4. **Sanitizers**:
   - Usage of `PreparedStatement` as a sanitizer to ensure the taint is neutralized before reaching the sink.

#### 4. Testing and Validation

**Test Cases**:

1. **Positive Test Case** (SQL Injection Present):
   ```java
   HttpServletRequest request = ...;
   String userInput = request.getParameter("userID");
   Statement statement = connection.createStatement();
   statement.executeQuery("SELECT * FROM users WHERE userID = '" + userInput + "';");
   ```

2. **Negative Test Case** (Proper Sanitization):
   ```java
   HttpServletRequest request = ...;
   String userInput = request.getParameter("userID");
   PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM users WHERE userID = ?");
   preparedStatement.setString(1, userInput);
   preparedStatement.executeQuery();
   ```

3. **Edge Case** (Indirect Propagation):
   ```java
   public String getUserID(HttpServletRequest request) {
       return request.getParameter("userID");
   }
   Statement statement = connection.createStatement();
   statement.executeQuery("SELECT * FROM users WHERE userID = '" + getUserID(request) + "';");
   ```

**Validation Methods**:

- Utilize Mariana Trench running on a real Java codebase, varying both simple and complex code structures to ensure broad yet precise rule application.
- Use GitHub Code Scanning or a continuous integration (CI) environment to automate the detection process.
- Constantly refine rules based on the results obtained from testing different code repositories to reduce false positives and false negatives.

**Running the Rules in Mariana Trench**:

1. **Include the Custom Rules**:
   Add the custom rule JSON to the `rules.json` file in Mariana Trench's configuration:
   ```json
   "rules_paths": [
     "path/to/custom/rules.json",
     // other rule paths
   ]
   ```

2. **Run the Analysis**:
   Execute the Mariana Trench analyzer on the Java project:
   ```shell
   $ mariana-trench --apk-path path/to/android_app.apk --rules-paths path/to/custom/rules.json --output-directory output_path/
   ```

3. **Review Results**:
   Access the results and review the data flows identified by Mariana Trench using the web interface or through JSON output files for further analysis.

By following this method, we can effectively use Mariana Trench to detect SQL Injection vulnerabilities in Java applications with minimized false positives and false negatives.

#### References
- Mariana Trench Documentation【4:0†source】【4:1†source】【4:5†source】【4:6†source】【4:10†source】