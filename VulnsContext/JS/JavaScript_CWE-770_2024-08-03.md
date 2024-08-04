# Allocation of Resources Without Limits or Throttling (CWE-770) in JavaScript

###### Allocation of Resources Without Limits or Throttling: Explanation

**Allocation of Resources Without Limits or Throttling** refers to scenarios in software where resources like CPU, memory, or network bandwidth are allocated without any restrictions, potentially leading to Resource Exhaustion or Denial of Service (DoS) attacks. Without proper controls, malicious users can exploit these vulnerabilities to overwhelm system resources, causing performance degradation or outages.

Examples of such conditions include:
1. Unlimited data processing on user input.
2. Infinite loops or uncontrolled recursions.
3. Unrestricted file uploads leading to disk space exhaustion.
4. Processing-intensive operations without timeout limits.

### Examples in JavaScript and Popular Frameworks

#### 1. Unrestricted Data Processing
**Example**: Processing user-uploaded files/videos without size restriction.

```javascript
app.post('/upload', function(req, res) {
    req.pipe(fs.createWriteStream('/tmp/' + req.headers['filename']));
    res.send('Upload Completed');
});
```

**SAST Rule Detection**:
- Identify routes handling file uploads.
- Check for lack of file size limit implementation.

#### 2. Infinite Loops or Uncontrolled Recursions
**Example**: Recursive function without base case or exit condition.

```javascript
function fetchData(id) {
    // Potential infinite recursion
    fetchData(id + 1);
}
```

**SAST Rule Detection**:
- Look for recursive function calls.
- Ensure base cases are defined to terminate recursion.

#### 3. Unrestricted File Uploads
**Example**: Allowing any size or type of file upload.

```javascript
app.post('/upload', function(req, res) {
    // No size or type validation
    req.pipe(fs.createWriteStream('/uploads/' + req.files[0].name));
    res.send('File uploaded successfully');
});
```

**SAST Rule Detection**:
- Detect file upload handlers.
- Check if there are limits set on file size or type.

#### 4. Unbounded Array and Object Growth
**Example**: Growing an array based on user input without checks.

```javascript
app.post('/add-item', function(req, res) {
    let items = [];
    for (let i = 0; i < req.body.itemsCount; i++) {
        items.push(req.body.item);
    }
    res.json(items);
});
```

**SAST Rule Detection**:
- Look for patterns where arrays or objects grow based on user input.
- Validate that size checks or limits are in place.

#### 5. Intensive Operations Without Timeouts
**Example**: Long-running operations (e.g., complex calculations) without a timeout.

```javascript
app.get('/compute-intensive', function(req, res) {
    while (true) {
        // Endless computation
    }
    res.send('Done');
});
```

**SAST Rule Detection**:
- Identify operations within loops or repeated tasks lacking break conditions.
- Ensure timeout logic is included.

### Detailed Examples from JavaScript Frameworks

#### Express.js
**Example**: Lack of rate limiting and request body size limitation.

```javascript
const express = require('express');
const app = express();
app.use(express.json());

app.post('/data', (req, res) => {
    // No rate limiting
    processData(req.body);
    res.send('Data processed');
});

function processData(data) {
    // Intensive processing
}
```

**SAST Rule Detection**:
- Verify routes for middleware enforcing rate limits (e.g., `express-rate-limit`).
- Ensure `express.json()` or other body-parsing middleware have a `limit` option set.

#### Next.js
**Example**: Unthrottled API routes.

```javascript
// pages/api/data.js
export default function handler(req, res) {
    // No throttle or rate limit
    intensiveOperation(req.query.param);
    res.status(200).json({ status: 'completed' });
}
```

**SAST Rule Detection**:
- Scan for API routes in the `pages/api` directory.
- Check for presence of rate-limiting middleware or logic.

Improperly managed resource allocation can introduce significant vulnerabilities that can be exploited by attackers. By understanding these patterns and implementing SAST rules to detect such issues, tools can help enforce secure coding practices and protect applications from potential abuse and DoS attacks.

**References**:
- Allocation of Resources Without Limits or Throttling concepts【4:0†source】.