BasedBased on the context provided in the document [`Semgrep.output.md`], here is a set of Semgrep SAST rules to detect "Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')" (CWE-917) in JavaScript. This set of rules covers various popular frameworks that could potentially be affected by this vulnerability.

## Semgrep Rules

### 1. Detecting Directly Evaluated Input Using `eval`

```yaml
rules:
  - id: javascript-eval-injection
    languages: [javascript]
    message: "Detected potential Expression Language Injection via eval."
    severity: ERROR
    patterns:
      - pattern: |
          eval($EXPR)
      - metavariable-pattern:
          metavariable: $EXPR
          patterns:
            - pattern-inside: |
                $OBJ.$PROP
            - pattern-inside: |
                $OBJ[$PROP]
    metadata:
      cwe: "CWE-917"
      owasp: "A1: Injection"
```

### 2. Detecting `Function` Constructor Injection

```yaml
rules:
  - id: javascript-function-constructor-injection
    languages: [javascript]
    message: "Detected potential Expression Language Injection via Function constructor."
    severity: ERROR
    patterns:
      - pattern: |
          new Function($ARGS)
      - metavariable-pattern:
          metavariable: $ARGS
          patterns:
            - pattern-inside: |
                $OBJ.$PROP
            - pattern-inside: |
                $OBJ[$PROP]
    metadata:
      cwe: "CWE-917"
      owasp: "A1: Injection"
```

### 3. Detecting `setTimeout` Injection

```yaml
rules:
  - id: javascript-settimeout-injection
    languages: [javascript]
    message: "Detected potential Expression Language Injection via setTimeout."
    severity: ERROR
    patterns:
      - pattern: |
          setTimeout($EXPR, $TIME)
      - metavariable-pattern:
          metavariable: $EXPR
          patterns:
            - pattern-inside: |
                $OBJ.$PROP
            - pattern-inside: |
                $OBJ[$PROP]
    metadata:
      cwe: "CWE-917"
      owasp: "A1: Injection"
```

### 4. Detecting `setInterval` Injection

```yaml
rules:
  - id: javascript-setinterval-injection
    languages: [javascript]
    message: "Detected potential Expression Language Injection via setInterval."
    severity: ERROR
    patterns:
      - pattern: |
          setInterval($EXPR, $TIME)
      - metavariable-pattern:
          metavariable: $EXPR
          patterns:
            - pattern-inside: |
                $OBJ.$PROP
            - pattern-inside: |
                $OBJ[$PROP]
    metadata:
      cwe: "CWE-917"
      owasp: "A1: Injection"
```

### 5. Detecting AngularJS `$eval` Method Injection

```yaml
rules:
  - id: angularjs-eval-injection
    languages: [javascript]
    message: "Detected potential Expression Language Injection via $eval in AngularJS."
    severity: ERROR
    patterns:
      - pattern: |
          $scope.$eval($EXPR)
      - metavariable-pattern:
          metavariable: $EXPR
          patterns:
            - pattern-inside: |
                $OBJ.$PROP
            - pattern-inside: |
                $OBJ[$PROP]
    metadata:
      cwe: "CWE-917"
      owasp: "A1: Injection"
```

### 6. Detecting VueJS `v-on` Directives

```yaml
rules:
  - id: vuejs-von-injection
    languages: [javascript]
    message: "Detected potential Expression Language Injection via v-on directive in VueJS."
    severity: ERROR
    patterns:
      - pattern: |
          v-on="$EXPR"
      - metavariable-pattern:
          metavariable: $EXPR
          patterns:
            - pattern-inside: |
                $OBJ.$PROP
            - pattern-inside: |
                $OBJ[$PROP]
    metadata:
      cwe: "CWE-917"
      owasp: "A1: Injection"
```

### References:
- Semgrep SAST Rule Writing Guidelines【4:0†source】.
- Additional Custom Rule Examples   .

These rules are adaptable and can be extended further to cover other frameworks and patterns as needed. Ensure to test these rules in your specific environment to confirm they accurately capture false positives and true positives effectively.