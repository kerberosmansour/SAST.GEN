ToTo create Mariana Trench SAST rules for detecting Cross-Site Request Forgery (CSRF) vulnerabilities (CWE-352) in Java, you need to define sources and sinks, and then create rules to detect the flows between these sources and sinks. CSRF attacks typically exploit the trust that a web application has in the browser of a user.

### Step-by-Step Guide to Creating SAST Rules for CSRF Detection in Java Using Mariana Trench

#### Step 1: Define CSRF Sources

CSRF sources are typically methods that handle incoming HTTP requests. In Java frameworks such as Spring and Struts, methods in controllers that are mapped to HTTP endpoints are potential CSRF sources.

Example Model Generator for CSRF Sources:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": ".*Controller.*"
        },
        {
          "constraint": "annotation",
          "type": "org.springframework.web.bind.annotation.RequestMapping"
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "HttpRequest",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```
Explanation:
- `find`: Specifies to look for methods.
- `where`: Filters methods to those in classes whose names contain "Controller" and are annotated with `@RequestMapping`.
- `model`: Defines these methods' incoming HTTP request parameters as `HttpRequest` sources.

#### Step 2: Define CSRF Sinks

CSRF sinks are actions such as modifying user data without proper CSRF token verification. Methods that perform operations like `POST`, `PUT`, or `DELETE` HTTP methods in controllers and services are potential CSRF sinks.

Example Model Generator for CSRF Sinks:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "annotation",
          "type": "org.springframework.web.bind.annotation.PostMapping"
        },
        {
          "constraint": "annotation",
          "type": "org.springframework.web.bind.annotation.PutMapping"
        },
        {
          "constraint": "annotation",
          "type": "org.springframework.web.bind.annotation.DeleteMapping"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "HttpDataModification",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```
Explanation:
- `find`: Specifies to look for methods.
- `where`: Filters methods annotated with `@PostMapping`, `@PutMapping`, or `@DeleteMapping`.
- `model`: Defines these methods' incoming arguments as `HttpDataModification` sinks.

#### Step 3: Define the Rule

Create a rule that specifies the data flow from identified CSRF sources to sinks without proper verification.

Example Rule for CSRF:
```json
{
  "name": "CSRF Vulnerability Rule",
  "code": 1001,
  "description": "CSRF vulnerability detected: HTTP request handling method leading to data modification without CSRF token verification.",
  "sources": [
    "HttpRequest"
  ],
  "sinks": [
    "HttpDataModification"
  ]
}
```

Explanation:
- `name`, `code`, and `description`: Metadata for the rule.
- `sources`: Identifies HTTP request handling methods as sources.
- `sinks`: Identifies data modification methods as sinks.

### Implementation Considerations for Popular Frameworks

Java frameworks like Spring, Struts, and Play have different annotations and methods for handling HTTP requests and performing data modifications. Ensure the model generators consider these specific annotations and methods.

#### For Spring Framework:
- Sources: Methods annotated with `@RequestMapping`, `@GetMapping`.
- Sinks: Methods annotated with `@PostMapping`, `@PutMapping`, `@DeleteMapping`.

#### For Struts Framework:
- Sources: `execute` methods in Action classes.
- Sinks: Methods that perform data modifications in Action classes.

#### For Play Framework:
- Sources: Controller methods that handle HTTP requests.
- Sinks: Methods that perform actions modifying user state.

### Example for Struts Framework:
CSRF Source Model Generator:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "execute"
        },
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {
              "constraint": "name",
              "pattern": "Action"
            }
          }
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "HttpRequest",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```

CSRF Sink Model Generator:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "parent",
          "inner": {
            "constraint": "extends",
            "inner": {
              "constraint": "name",
              "pattern": "Action"
            }
          }
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "HttpDataModification",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```

### Final Notes
Always thoroughly test the rule set to minimize false positives and false negatives. Since CSRF vulnerabilities can be framework-specific, tailor your model generators and rules to the specific framework used in your project.

Reference: The provided data about Mariana Trench model generators and rule definitions can be found in the [Mariana Trench documentation sections on rules and models]       .