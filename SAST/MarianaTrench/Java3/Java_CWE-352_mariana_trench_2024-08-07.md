###### Writing SAST Rules for Cross-Site Request Forgery (CSRF) (CWE-352) in Java Using Mariana Trench

To detect Cross-Site Request Forgery (CSRF) vulnerabilities in Java applications via Mariana Trench, we need to define sources (where the CSRF could originate, such as unprotected actions) and sinks (where the CSRF vulnerability is actualized, such as methods that perform sensitive actions without CSRF protection). Additionally, we must handle specific Java frameworks that are commonly used in web applications like Spring MVC and Java Servlets.

#### Mariana Trench Rule Overview
To understand how to write rules, refer to the structure and usage of sources, sinks, and rules discussed in Mariana Trench. A rule is a collection of sources and sinks tied together to detect an end-to-end data flow/vulnerability【8:1†source】  .

### Step-by-Step Guide to Write CSRF SAST Rules

#### 1. Define Sources
Identify methods in web controllers that handle HTTP requests which are susceptible to CSRF if not protected, e.g., methods annotated with `@RequestMapping` or `@PostMapping` in Spring MVC.
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "any_of",
          "inners": [
            {
              "constraint": "has_annotation",
              "pattern": "Lorg/springframework/web/bind/annotation/PostMapping;"
            },
            {
              "constraint": "has_annotation",
              "pattern": "javax/ws/rs/Path"
            },
            {
              "constraint": "has_annotation",
              "pattern": "javax/servlet/http/HttpServlet"
            }
          ]
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "CSRFSource",
            "port": "Argument(0)" // Request parameter typically passed as the first argument
          }
        ]
      }
    }
  ]
}
```

#### 2. Define Sinks
Identify methods where sensitive actions are performed that should be protected from CSRF, e.g., methods doing financial transactions, changing critical settings, etc.
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "processTransaction"
        },
        {
          "constraint": "parent",
          "pattern": "com/corebanking/payment/Gateway"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "CSRFDetected",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```

#### 3. Define Rules
A rule combines sources and sinks to detect unprotected CSRF flows.
```json
{
  "name": "Detect Unprotected CSRF Flows in Java",
  "code": 1001,
  "description": "Cross-Site Request Forgery vulnerability due to missing CSRF protection.",
  "sources": ["CSRFSource"],
  "sinks": ["CSRFDetected"]
}
```

### Verification and Optimization
- **Multiple Sources Handling**: Ensure the rule efficiently tracks different pathways the data might take from the source (HTTP request handler) to the sink (sensitive action method).
- **False Positives/Negatives**: Fine-tune annotations and method names in the `where` constraints to reduce false positives (e.g., actions not meant to be protected) and false negatives (e.g., valid paths missed during rule specification).

### Examples from OWASP WSTG
Common test cases include checking for missing or incorrect CSRF tokens in forms, and ensuring sensitive actions like financial transactions have appropriate CSRF defenses【8:0†source】【8:16†source】.

### Example Models and Rules:

- **Model Generators File**: Define where to find controllers and transaction methods in your project by adding a JSON model generator configuration file.
- **Rule File**: DNSRTA Rules can be specified in a `rules.json` file or any custom rule file that Mariana Trench uses to load and enforce these rules during static analysis.

### Conclusion
By setting up these pieces - Sources, Sinks, and Rules - you can effectively use Mariana Trench to catch potential CSRF vulnerabilities in Java applications. Adjust the patterns and constraints as necessary for the specific configurations and coding patterns in your project to ensure high precision in your SAST tool【8:0†source】 .