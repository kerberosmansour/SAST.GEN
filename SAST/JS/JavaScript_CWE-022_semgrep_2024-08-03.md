ToTo create Semgrep SAST rules for detecting Improper Limitation of a Pathname to a Restricted Directory (Path Traversal, CWE-022) in JavaScript, you can follow guidelines and examples drawn from various parts of the document. Here's a custom rule to detect unsafe usage patterns that might lead to directory traversal vulnerabilities in JavaScript, specifically for popular frameworks like Express.js or Node.js:

### Rule for Generic JavaScript Path Traversal
```yaml
rules:
  - id: path-traversal-javascript
    pattern: |
      $res.sendFile($PATH, {
        root: $ROOT
      })
    message: "Potential Path Traversal vulnerability: Using raw paths in sendFile"
    severity: WARNING
    languages:
      - javascript
    metadata:
      cwe: "CWE-22"
```

### Rule Focusing on Node.js Specific Usage
```yaml
rules:
  - id: path-traversal-node
    pattern: |
      require("fs").readFile(..., $PATH, ...)
    message: "fs.readFile with user-controlled paths can lead to Path Traversal"
    severity: ERROR
    languages:
      - javascript
    metadata:
      cwe: "CWE-22"
  - id: path-traversal-node-fs
    pattern: |
      require("fs").readFileSync(..., $PATH, ...)
    message: "fs.readFileSync with user-controlled paths can lead to Path Traversal"
    severity: ERROR
    languages:
      - javascript
    metadata:
      cwe: "CWE-22"
  - id: path-traversal-node-open
    pattern: |
      require("fs").open(..., $PATH, ...)
    message: "fs.open with user-controlled paths can lead to Path Traversal"
    severity: ERROR
    languages:
      - javascript
    metadata:
      cwe: "CWE-22"
```

### Rule for Express.js Specific Usage
```yaml
rules:
  - id: path-traversal-express
    patterns:
      - pattern: |
          app.get($ROUTE, (req, res) => {
            res.sendFile(req.params.file);
          })
      - pattern-inside: |
          function $FUNC(req, res) {...}
    message: "Express.js sendFile with user-controlled paths can lead to Path Traversal"
    severity: ERROR
    languages:
      - javascript
    metadata:
      cwe: "CWE-22"
```

### Rule for Usage in HTTP Requests
```yaml
rules:
  - id: path-traversal-http
    patterns:
      - pattern: |
          http.get(req.params[$PARAM], ($, res) => {
            $FS_METHOD($, req.params[$PARAM], function(err, data) {...})
          })
      - metavariable-pattern:
          metavariable: $FS_METHOD
          patterns:
            - pattern: |
                fs.readFile
            - pattern: |
                fs.readFileSync
            - pattern: |
                fs.open
    message: "HTTPRequest handlers with user-controlled paths can lead to Path Traversal"
    severity: ERROR
    languages:
      - javascript
    metadata:
      cwe: "CWE-22"
```

These rules capture multiple scenarios where user input might be used in file path operations, leading to potential path traversal vulnerabilities. Variants cover the use of core Node.js modules and specific cases using Express.js, a popular JavaScript framework for building web applications     .