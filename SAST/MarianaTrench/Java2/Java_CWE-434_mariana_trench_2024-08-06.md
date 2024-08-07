ToTo create Mariana Trench SAST rules for detecting the vulnerability "Unrestricted Upload of File with Dangerous Type (CWE-434)" in Java, we need to define sources, sinks, and the rules that connect them. Specifically, we should target various popular Java frameworks that handle file uploads, such as Spring and Apache Commons FileUpload.

Let's define this step-by-step based on the provided instructions for writing Mariana Trench SAST rules【4:0†source】  .

### Step 1: Define Sources
A source for this vulnerability is typically a method that accepts file data from an untrusted source, such as a web request.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        { "constraint": "parent", "inner": { "constraint": "name", "pattern": "MultipartFile" } }, 
        { "constraint": "name", "pattern": "getBytes|getInputStream|getOriginalFilename|getName|getSize|getContentType" }
      ],
      "model": {
        "sources": [
          {
            "kind": "UntrustedFile",
            "port": "Return"
          }
        ]
      }
    },
    {
      "find": "methods",
      "where": [
        { "constraint": "parent", "inner": { "constraint": "extends", "inner": { "constraint": "name", "pattern": "HttpServletRequest" } } },
        { "constraint": "name", "pattern": "getPart|getParts" }
      ],
      "model": {
        "sources": [
          {
            "kind": "UntrustedFile",
            "port": "Return"
          }
        ]
      }
    }
  ]
}
```

### Step 2: Define Sinks
A sink for this vulnerability is any method that processes or writes the file without proper validation or sanitization.

```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        { "constraint": "name", "pattern": "write|writeTo|save|store" },
        { "constraint": "parent", "inner": { "constraint": "name", "pattern": "File|FileOutputStream|Files" } }
      ],
      "model": {
        "sinks": [
          {
            "kind": "FileWrite",
            "port": "Argument(0)"
          }
        ]
      }
    }
  ]
}
```

### Step 3: Define Rules
Finally, we define the rules that will track the data flow from our defined sources to our defined sinks.

```json
{
  "rules": [
    {
      "name": "Unrestricted upload of untrusted file",
      "code": 10001,
      "description": "Untrusted file data flows into file write method without validation",
      "sources": ["UntrustedFile"],
      "sinks": ["FileWrite"]
    }
  ]
}
```

### Explanation:
1. **Sources**:
   - **MultipartFile** is a common class in Spring applications used to handle file uploads. We define methods such as `getBytes()`, `getInputStream()`, `getOriginalFilename()`, `getName()`, `getSize()`, and `getContentType()` as returning untrusted data.
   - **HttpServletRequest** methods like `getPart()` and `getParts()` also need to be monitored for untrusted file data.

2. **Sinks**:
   - Methods such as `write()`, `writeTo()`, `save()`, and `store()` present in classes like `File`, `FileOutputStream`, and `Files` can be critical points where the untrusted data might be written to the system without proper validation.

3. **Rules**:
   - We create a rule that looks for data flows from `UntrustedFile` sources to `FileWrite` sinks, which represents a potential CWE-434 vulnerability pattern【4:0†source】  .

By defining these models and rules, Mariana Trench can be instructed to look for problematic data flows regarding CWE-434 vulnerabilities in Java applications using popular frameworks.

### References
Ensure that you have the necessary model generators and rules set up correctly in your configuration paths as specified in Mariana Trench usage instructions   .