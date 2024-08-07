ToTo write Mariana Trench SAST rules for the vulnerability "Unrestricted Upload of File with Dangerous Type (CWE-434)" in Java, we need to define custom sources, sinks, and rules in JSON format. These rules should cover variations of the vulnerability that could occur in popular Java frameworks like Spring, Apache Struts, and others. This process aims to create rules with high accuracy, minimizing false positives and false negatives.

### Step-by-Step Guide

1. **Identifying Sources and Sinks:**
    - **Sources:** Methods where the file upload originates, e.g., from HTTP requests.
    - **Sinks:** Methods where the file is processed, e.g., saved to disk or executed.

2. **Creating Model Generators:**
    - Define the sources and sinks using JSON model generators.
    - Use constraints to specify the relevant methods and parameters.

3. **Writing Rules:**
    - Define rules specifying the data flow from sources to sinks.

### Example JSON Configuration

#### Sources

Let's define HTTP request file upload methods as sources. We assume our sensitive user inputs come from `javax.servlet.http.HttpServletRequest` or similar classes in popular frameworks.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "getInputStream|getFile|getFiles"},
        {
          "constraint": "parent",
          "inner": {
            "constraint": "name",
            "pattern": "javax.servlet.http.HttpServletRequest|org.springframework.web.multipart.MultipartFile"
          }
        }
      ],
      "model": {
        "sources": [
          {
            "kind": "FileUploadSource",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

#### Sinks

Define sinks where potentially dangerous files might be saved or executed. These can include methods from java.io.File, java.nio.file.Files, etc.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "createNewFile|saveFile|transferTo"},
        {
          "constraint": "parent",
          "inner": {
            "constraint": "name",
            "pattern": "java.io.File|java.nio.file.Files|org.springframework.web.multipart.MultipartFile"
          }
        }
      ],
      "model": {
        "sinks": [
          {
            "kind": "FileSaveSink",
            "port": "Argument(1)"
          }
        ]
      }
    }
  ]
}
```

#### Taint Propagation

If your application should also track the propagation of data (e.g., from an input stream to a file output stream), introduce appropriate propagation rules.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "write|transferTo"},
        {
          "constraint": "parent",
          "inner": {
            "constraint": "name",
            "pattern": "java.io.OutputStream|java.nio.file.Files"
          }
        }
      ],
      "model": {
        "propagation": [
          {
            "input": "Argument(0)",
            "output": "Argument(1)"
          }
        ]
      }
    }
  ]
}
```

### Defining the Rule

Finally, define a rule linking the sources and sinks via potential taint propagations.

```json
{
  "rules": [
    {
      "name": "File upload with dangerous type",
      "code": 434,
      "description": "Detect unrestricted upload of files with dangerous types",
      "sources": [
        "FileUploadSource"
      ],
      "sinks": [
        "FileSaveSink"
      ],
      "propagations": [
        "FileSavePropagation"
      ]
    }
  ]
}
```

### Summary

1. **Sources:** Identify sources where files are uploaded.
2. **Sinks:** Identify sinks where files are saved or processed.
3. **Propagation:** Capture how files might move from sources to sinks through various methods.
4. **Rule:** Link sources to sinks with propagation to detect potential CWE-434 vulnerabilities.

Following these steps and custom JSON configurations should provide a robust Mariana Trench setup to detect CWE-434 in Java applications with high accuracy【8:0†source】【8:13†source】【8:14†source】【8:16†source】【8:18†source】.