###### Generating Mariana Trench SAST Rules for Deserialization of Untrusted Data (CWE-502) in Java

#### 1. **Context Review:**
The Mariana Trench documentation specifies how to define sources, sinks, and taint propagation rules using JSON. This includes creating rules that track the flow of data from sources (e.g., user input) to sinks (e.g., deserialization methods).

##### Key Components:
- **Rule Definition**: In Mariana Trench, a rule defines the flow from sources to sinks, which needs to be tracked.
- **Source Definition**: This defines where the tainted data originates.
- **Sink Definition**: This points to vulnerable methods that lead to potential security risks.
- **Propagation Rules**: These describe how taint propagates through the code.

Example of a rule in JSON:
```json
{
  "name": "Deserialization from untrusted data",
  "code": 1001,
  "description": "User-controlled data is deserialized",
  "sources": [
    "UserInput"
  ],
  "sinks": [
    "Deserialization"
  ]
}
```

Here are the steps for writing the rule:

1. **Defining Sources and Sinks**:
    - **Sources**: Typically, user input or data from external sources.
    - **Sinks**: Methods like `ObjectInputStream.readObject`, `XMLDecoder.readObject`, etc.

2. **Example JSON for Source Definition**:
   ```json
   {
     "model_generators": [
       {
         "find": "methods",
         "where": [
           {
             "constraint": "name",
             "pattern": "getParameter|getHeader"
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

2. **Example JSON for Sink Definition**:
   ```json
   {
     "model_generators": [
       {
         "find": "methods",
         "where": [
           {
             "constraint": "name",
             "pattern": "readObject|readUnshared"
           },
           {
             "constraint": "parent",
             "pattern": "java.io.ObjectInputStream"
           }
         ],
         "model": {
           "sinks": [
             {
               "kind": "Deserialization",
               "port": "Argument(0)"
             }
           ]
         }
       }
     ]
   }
   ```

### 2. **Vulnerability Analysis:**
Deserialization of untrusted data (CWE-502) is a high-severity risk where user-supplied data is directly deserialized, potentially executing untrusted code within the application. Methods to monitor include `readObject` from `ObjectInputStream`, `XMLDecoder.readObject` and similar methods.

### 3. **Mariana Trench Rule Creation:**

Defining low false positives and false negatives conditions is critical. This means carefully defining sources of untrusted input and sinks where deserialization can occur.

Here are the rules and models for identifying deserialization vulnerabilities:

#### **Source Definitions:**
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "constraint": "name",
          "pattern": "(getParameter|getHeader|getCookie|getQueryString|fromFile|fromStream)"
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
#### **Sink Definitions:**
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {
          "signature_match": "$class; Object readObject();"
        },
        {
          "constraint": "parent",
          "pattern": "java.io.ObjectInputStream"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "Deserialization",
            "port": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        {
          "signature_match": "$class; Object readObject(InputStream);"
        },
        {
          "constraint": "parent",
          "pattern": "java.beans.XMLDecoder"
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "Deserialization",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

### 4. **Testing and Validation:**

#### **Test Cases:**
1. **Standard Use Cases**:
    - Test standard deserialization flows where user input is passed directly to `ObjectInputStream.readObject`.
2. **Edge Cases**:
    - Test indirect deserialization scenarios where data flows through multiple methods before being deserialized.
3. **Frameworks and Libraries**:
    - Ensure compatibility with common Java frameworks such as Spring and Hibernate.

#### **Testing Strategies**:
1. **Unit Tests**:
    - Write unit tests to ensure rules catch deserialization from typical sources.
2. **Integration Tests**:
    - Use GitHub Code Scanning to run these rules against large codebases.
3. **Mariana Trench Query Console**:
    - Use the Mariana Trench query console for ad-hoc queries and validations.

These comprehensive rules and thorough testing will help ensure that deserialization vulnerabilities are accurately identified with minimal false positives and negatives.

### References:
- Mariana Trench Documentation on Generating Models【4:0†source】【4:1†source】【4:3†source】【4:6†source】【4:7†source】【4:8†source】【4:10†source】【4:11†source】【4:17†source】
- Guidelines on Customizing Sources and Sinks【4:14†source】【4:15†source】【4:16†source】【4:18†source】【4:19†source】

By following these guidelines, you can create effective Mariana Trench SAST rules tailored to detecting the deserialization of untrusted data vulnerabilities in Java applications.