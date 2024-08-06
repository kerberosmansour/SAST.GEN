ToTo generate CodeQL Static Application Security Testing (SAST) Rules for Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') (CWE-917) in Java, follow these detailed steps:

### 1. **Context Review**
#### Review on Writing CodeQL Rules
The structure of `.ql` files and relevant QL constructs typically includes import statements, class definitions, predicates, and `select` statements. Here's a basic structure often followed:
```ql
/**
 * @name <query name>
 * @description <query description>
 * @kind <problem|path-problem>
 * @id <unique id>
 * @tags <security, correctness, convention>
 */

import java

class <CustomClass> extends <BaseClass> {
  // Define class members and predicates
  ...
}

predicate <PredicateName>(...) {
  // Define logical conditions
  ...
}

from <variable declarations>
where <conditions>
select <expressions>
```
Basic metadata should include the name, description, kind, unique ID, and relevant tags for the query. More detailed structure includes path queries, usage of `defining-the-results-of-a-query` module, control of query output, and more【4:0†source】【4:1†source】【4:3†source】【4:4†source】【4:9†source】【4:10†source】.

### 2. **Vulnerability Analysis**
#### Expression Language Injection in Java
Improper Neutralization of Special Elements in Expression Language Statements (CWE-917) arises when user inputs are evaluated as code within expression languages (e.g., OGNL, MVEL, SpEL) without proper sanitization. This can lead to remote code execution. 

Common scenarios include:
- Using user inputs directly in expression evaluations.
- Evaluating expressions in web applications using frameworks like Spring with Spring EL or Apache Struts using OGNL.
  
Potential code patterns leading to this vulnerability involve:
```java
// Vulnerable code example
String userInput = request.getParameter("userInput");
ExpressionParser parser = new SpelExpressionParser();
Expression exp = parser.parseExpression(userInput);
exp.getValue(); // dangerous if userInput is not sanitized
```

Popular frameworks/libraries where this is observed:
- **Spring Framework** (Spring EL)
- **Apache Struts** (OGNL)
- **MVEL** (MVEL2.0)

### 3. **CodeQL Rule Creation**
#### Define Custom Classes and Predicates
Define custom classes for common expressions in these frameworks, such as `SpelExpression`, `OgnlExpression`, and relevant methods that evaluate expressions.

```ql
/**
 * @name Expression Language Injection in Java
 * @description Improper Neutralization of Special Elements in Expression Language Statements (CWE-917) identification in Java code.
 * @kind path-problem
 * @id java.expression.language.injection
 * @tags security, external/cwe/cwe-917
 */
import java
import semmle.code.java.frameworks.Spring
import semmle.code.java.dataflow.TaintTracking

class SpelExpression extends Method {
  SpelExpression() {
    this.getDeclaringType().hasQualifiedName("org.springframework.expression.spel.standard", "SpelExpressionParser") and
    this.getName() = "parseExpression"
  }
}

class OgnlExpression extends Method {
  OgnlExpression() {
    this.getDeclaringType().hasQualifiedName("ognl.Ognl", "Ognl") and
    this.getName() = "parseExpression"
  }
}

predicate taintedExpression(MethodCall call) {
  exists(Method m |
    call.getMethod() = m and
    (m instanceof SpelExpression or m instanceof OgnlExpression)
  )
}

from MethodCallSource source, MethodCall call, DataFlow::PathNode sourceNode, DataFlow::PathNode sinkNode
where
  taintedExpression(call) and
  TaintTracking::exprTaint(source.getSource(), call.getAnArgument()) and
  TaintTracking::localFlow(sourceNode, sinkNode)
select sinkNode.getNode(), "Potential Expression Language Injection detected in " + source.getNode()
```

### 4. **Testing and Validation**
#### Test Cases
Create test cases simulating various expressions and ensuring that the query catches improper neutralization correctly, while minimizing false positives:

**Test Cases:**
- Non-sanitized input used directly in expression evaluation.
- Properly sanitized inputs.
- Different forms of taint propagation.

**Example Test Case Code:**
```java
import org.springframework.expression.spel.standard.SpelExpressionParser;

public class ExpressionLanguageInjectionTest {
  public void unsafe(String userInput) {
    SpelExpressionParser parser = new SpelExpressionParser();
    parser.parseExpression(userInput).getValue(); // Should be flagged
  }
  
  public void safe() {
    SpelExpressionParser parser = new SpelExpressionParser();
    parser.parseExpression("safeExpression").getValue(); // Should not be flagged
  }
}
```

**Validation Approach:**
- Use CodeQL query console to run the above rules on a Java project codebase.
- Conduct unit tests for Taint Tracking and ensure that tests cover edge cases using assertions.
- Validate the rules by running them on open-source projects using GitHub Code Scanning or CodeQL CLI【4:0†source】【4:6†source】【4:13†source】【4:14†source】【4:15†source】.

This detailed approach should help in accurately identifying CWE-917 vulnerabilities while minimizing false positives and negatives.