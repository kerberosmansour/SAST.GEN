ToTo write SAST rules in Mariana Trench for detecting SQL Injection (CWE-89) vulnerabilities in Java, we need to define sources where tainted data may enter the application and sinks where this tainted data can cause security issues. Based on the gathered information, here’s how you can write effective Mariana Trench SAST rules with a focus on SQL Injection detection:

### Overview of SQL Injection Detection

**Sources:** 
- User inputs via HTTP requests, socket connections, or other means can be considered as sources.
- Interactions with databases via ORMs like Hibernate, JPA, or direct JDBC calls can be points where tainted data flows into the system.

**Sinks:** 
- Methods involving SQL execution such as `Statement.executeQuery()`, `Statement.executeUpdate()`, or any ORM methods executing SQL queries.

### Writing the Rules

1. **Define Sources:**
   Create a file named `inputs.models.json` for identifying tainted sources such as user inputs.

   ```json
   {
     "model_generators": [
       {
         "find": "methods",
         "where": [
           {"constraint": "name", "pattern": "getParameter|getQueryString|getInputStream|readLine|nextElement"}
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

2. **Define Sinks:**
   Create a file named `sinks.models.json` for identifying SQL execution points.

   ```json
   {
     "model_generators": [
       {
         "find": "methods",
         "where": [
           {"constraint": "name", "pattern": "executeQuery|executeUpdate|createQuery|createSQLQuery|find|persist"}
         ],
         "model": {
           "sinks": [
             {
               "kind": "SQLExecution",
               "port": "Argument(0)"
             }
           ]
         }
       }
     ]
   }
   ```

3. **Define Propagations:**
   To capture the flow of user input to the SQL execution points, we may define propagations. For example:

   ```json
   {
     "model_generators": [
       {
         "find": "methods",
         "where": [{"constraint": "name", "pattern": "setParameter"}],
         "model": {
           "propagation": [
             {
               "input": "Argument(1)",
               "output": "Argument(0)"
             }
           ]
         }
       }
     ]
   }
   ```

4. **Create the Detection Rule:**
   Finalize by creating a rule in `rules.json` to tie the sources to the sinks. 

   ```json
   {
     "rules": [
       {
         "name": "SQL Injection",
         "code": 1001,
         "description": "User input can flow into SQL execution leading to SQL Injection",
         "sources": ["UserInput"],
         "sinks": ["SQLExecution"]
       }
     ]
   }
   ```

### Implementing and Testing the Rules

**Step-by-Step Approach:**
1. **Define Models:** Write your JSON model definitions for sources, sinks, and propagations.
2. **Update Configuration:** Ensure your model JSON files are referenced in `configuration/default_generator_config.json`.
3. **Run Analysis:** Use Mariana Trench to analyze the Java application based on the rules defined.
4. **Verify Results:** Inspect the results to fine-tune and ensure both high accuracy (low false positives and negatives).

### Example Usage in Java

```java
public void vulnerableMethod(HttpServletRequest request) throws SQLException {
    String userId = request.getParameter("userId");
    String query = "SELECT * FROM users WHERE user_id = " + userId; // This is vulnerable to SQL Injection
    Statement stmt = connection.createStatement();
    ResultSet rs = stmt.executeQuery(query);
}
```

In this example, `request.getParameter` is a source and `stmt.executeQuery(query)` is a sink. The SAST rule should detect the flow from `userId` (tainted user input) to `executeQuery` (SQL execution).

By carefully defining these sources, sinks, and their connecting propagations, you can create effective SAST rules in Mariana Trench that minimize false positives and false negatives.

Refer to the guides and examples in the [Mariana Trench documentation](https://github.com/facebook/mariana-trench) and adjust model patterns according to your specific application needs to enhance detection accuracy   .