# Uncontrolled Search Path Element (CWE-427) in JavaScript

###### Understanding Uncontrolled Search Path Element

The "Uncontrolled Search Path Element" vulnerability occurs when an application uses external input to construct paths to critical system resources, like executables or libraries, without properly validating or restricting these paths. This can lead to severe security issues such as executing malicious code or accessing unintended files. The vulnerability is categorized under CWE-427 (Uncontrolled Search Path Element) and CWE-426 (Untrusted Search Path)【4:0†source】【4:2†source】.

### Common Occurrence Variations in JavaScript

JavaScript and its popular frameworks are prone to various instances of Uncontrolled Search Path Element. Here are some common patterns and variations where this vulnerability can occur:

#### 1. Node.js Path Manipulation

In Node.js applications, which involve extensive file system interactions, developers may inadvertently introduce vulnerabilities while handling file paths.

**Example:**
```javascript
const fs = require('fs');
const path = require('path');

function readFile(fileName) {
  const filePath = path.join(__dirname, fileName);
  return fs.readFileSync(filePath, 'utf8');
}

const userFile = readFile(request.query.fileName);
```
In this example, `request.query.fileName` is taken from user input, which can lead to an attacker accessing unauthorized files by providing a malicious input like `../../etc/passwd`.

#### 2. Electron.js Native Modules

Electron applications often involve native modules, which can lead to vulnerabilities if paths are not properly managed.

**Example:**
```javascript
const nativeModulePath = path.join(__dirname, request.query.moduleName);
const nativeModule = require(nativeModulePath);
```
Here, `request.query.moduleName` can be manipulated to load unintended or malicious native modules, leading to code execution vulnerabilities.

#### 3. Script or Module Import/Require

JavaScript applications dynamically importing or requiring scripts or modules without validation are susceptible.

**Example:**
```javascript
function loadModule(moduleName) {
  return require(moduleName);
}

const userModule = loadModule(request.body.moduleName);
```
An attacker can supply a path to a malicious module, leading to the execution of untrusted code.

#### 4. MongoDB and NoSQL Injections

Popular frameworks using MongoDB or other NoSQL databases are vulnerable if user input is not properly sanitized when constructing queries.

**Example:**
```javascript
app.get('/search', (req, res) => {
  const searchPath = req.query.searchPath;
  db.collection(searchPath).find({}).toArray((error, results) => {
    res.send(results);
  });
});
```
Here, `req.query.searchPath` can be controlled to access unauthorized collections.

### Detection Strategy for SAST Tools

To detect Uncontrolled Search Path Element, a SAST tool should focus on identifying patterns where external input influences path construction or resource access. Here are some rules:

#### Node.js Specific Patterns:
1. **Path Join Vulnerability**:
    - Identify instances where `path.join` or similar functions concatenate paths with user input.
    - Example detection rule: 
      ```regex
      path\.join\s*\(\s*[^,]+,\s*request\.\w+\.\w+\s*\)
      ```

2. **Require Module Vulnerability**:
    - Locate `require` statements accepting user-controlled variables.
    - Example detection rule:
      ```regex
      require\s*\(\s*request\.\w+\.\w+\s*\)
      ```

3. **File System Access**:
    - Scan for `fs` module methods using user input directly.
    - Example detection rule:
      ```regex
      fs\.\w+\s*\(\s*path\.join\s*\(\s*[^,]+,\s*request\.\w+\.\w+\s*\)
      ```

#### Framework Agnostic Patterns:
1. **Dynamic Import Statements**:
    - Identify dynamic imports using user input.
    - Example detection rule:
      ```regex
      import\(\s*request\.\w+\.\w+\s*\)
      ```

2. **Database Collection Access**:
    - Detect database methods with user-controlled collection or path names.
    - Example detection rule:
      ```regex
      db\.\w+\(\s*request\.\w+\.\w+\s*\)
      ```

3. **Path Manipulation and Construction**:
    - Find instances of path manipulation functions using user input.
    - Example detection rule:
      ```regex
      (path\.\w+|fs\.\w+)\s*\(\s*request\.\w+\.\w+\s*\)
      ```

### Conclusion

By focusing on these specific patterns and leveraging the detection strategies above, it becomes easier for a SAST tool to flag potential Uncontrolled Search Path Element vulnerabilities in JavaScript applications. Properly handling and validating all external inputs used in path constructions is critical to maintaining security【4:14†source】.