###### Context Review

The guidelines for writing CodeQL rules outline essential elements such as the structure of `.ql` files, use of metadata, and specific QL constructs related to SQL Injection vulnerabilities, particularly in Java.

### Structure of `.ql` Files and Metadata 

The general structure of CodeQL `.ql` files includes:
1. **Import Statements**: Importing necessary CodeQL libraries.
2. **Class Definitions**: Defining classes for specific purposes, such as modeling sinks, sources, and flows.
3. **Predicates**: Defining predicates to specify the conditions necessary to identify vulnerabilities.
4. **Data Flow Configurations**: Using data flow libraries and configurations to track the flow of data through the program.
5. **Select Statement**: Final selection criteria for identifying vulnerabilities and specifying how they should be reported【4:0†source】【4:1†source】【4:2†source】【4:3†source】【4:4†source】.

### Key Elements for SQL Injection (CWE-089)

CodeQL for SQL Injection should focus on identifying:
1. **Sinks**: Methods that execute SQL queries.
2. **Sources**: Points where user input is received.
3. **Flows**: Data flows from sources to sinks, tracking how untrusted data reaches SQL execution points.

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') in Java occurs when user input is used to construct SQL queries without proper sanitization or escaping. Typical methods to protect against this include:
- Using prepared statements or parameterized queries.
- Whitelisting allowed input.
- Escaping special characters where dynamic queries are unavoidable.

### Creation of CodeQL Rules

To detect SQL Injection in Java, we will implement the following CodeQL rule. This rule will perform taint tracking to find potential SQL Injection vulnerabilities by identifying untrusted user input reaching SQL execution methods.

#### Step 1: Define the Source
Identify user input sources, such as parameters of request handling methods.

```ql
import java
import semmle.code.java.dataflow.TaintTracking

class UserInputSource extends Source {
  UserInputSource() {
    this =
      any(Method m).getAnInput()
      and m.hasName(["doGet", "doPost", "doPut", "doDelete"])
      and m.getDeclaringType().getPackage().hasName("javax.servlet.http")
  }
}
```

#### Step 2: Define the Sink
Identify SQL query execution methods.

```ql
class SQLSink extends Sink {
  SQLSink() {
    this =
      any(MethodAccess ma)
      and ma.getMethod().hasName("executeQuery", "executeUpdate")
      and ma.getMethod().getDeclaringType().getPackage().hasName("java.sql")
  }
}
```

#### Step 3: Configure Taint Tracking
Specify how data flows from sources to sinks.

```ql
class SQLInjectionConfig extends TaintTracking::Configuration {
  SQLInjectionConfig() { this = "SQLInjectionConfig" }

  override predicate isSource(DataFlow::Node source) {
    source.asParameter() = any(UserInputSource uis).getParameter(0)
  }

  override predicate isSink(DataFlow::Node sink) {
    exists(SQLSink ss | sink.asExpr() = ss.getExpr())
  }
}
```

#### Step 4: Create the Query 
Combine all elements to form the CodeQL query.

```ql
/**
 * @name SQL injection
 * @description Detects SQL injection vulnerabilities where user input is concatenated to SQL queries.
 * @kind path-problem
 * @problem.severity error
 * @id java/sql-injection
 * @security-severity 5.0
 * @precision high
 * @tags security
 *       external/user-provided
 */

import java

from DataFlow::PathNode source, DataFlow::PathNode sink
where SQLInjectionConfig::instance().hasFlowPath(source, sink)
select sink, source, "SQL injection vulnerability."
```

### Testing and Validation

**Test Cases**:
- **Positive test cases**: Include scenarios where user input is used in SQL queries without using prepared statements.
- **Negative test cases**: Ensure that scenarios where prepared statements or proper sanitization mechanisms are used do not trigger the rule.

**Validation Process**:
1. **Locally**: Use the CodeQL CLI or Visual Studio Code extension to run the queries against a repository containing the test cases.
2. **Automated Scanning**: Integrate the rules into a CI/CD pipeline using GitHub Code Scanning to ensure new vulnerabilities are detected automatically.
3. **Coverage Report**: Analyze the results to ensure all potential injection points are covered and verify low rates of false positives and false negatives.

By following these steps, we can create effective CodeQL rules that accurately detect SQL Injection vulnerabilities in Java with low rates of false positives and false negatives.【4:6†source】【4:9†source】【4:14†source】【4:18†source】.

Ensure to review any changes from recent releases of CodeQL to stay updated with the latest methods and improvements for writing effective queries【4:10†source】【4:11†source】.