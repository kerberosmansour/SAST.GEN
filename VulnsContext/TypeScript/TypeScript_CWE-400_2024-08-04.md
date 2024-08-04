# Uncontrolled Resource Consumption (CWE-400) in TypeScript

###### Understanding Uncontrolled Resource Consumption

**Uncontrolled Resource Consumption** (also known as resource exhaustion) is a situation where an application or service is unable to limit the number of resources it uses, leading to degradation or complete denial of service. This commonly happens when multiple users send large numbers of requests or perform resource-intensive operations, which the system isn't equipped to handle. It is crucial to ensure proper resource management to prevent attackers from exploiting this vulnerability to launch Denial of Service (DoS) attacks.

Preventive measures can be broadly categorized into different defensive tactics such as **Rate Limiting**, **Input Validation**, **Session Management**, **Network Design Concepts**, and **Access Control**             .

### Examples of Uncontrolled Resource Consumption in TypeScript

In TypeScript, particularly within the context of popular frameworks like **Node.js**, **Angular**, and **React**, uncontrolled resource consumption issues can occur in different forms. Here are some specific examples along with potential code snippets that demonstrate how these vulnerabilities can be introduced and exploited.

#### 1. **Unrestricted Loops and Recursions**

##### Node.js
```typescript
function processData(input: any) {
    while (true) {
        // do some processing
        // no break condition provided
    }
}

// This loop will consume CPU indefinitely
processData("some input");
```

##### Angular
```typescript
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  ngOnInit() {
    this.unendingLoop();
  }

  unendingLoop() {
    while (true) {
      // Infinite loop causing CPU exhaustion
    }
  }
}
```

#### 2. **Unrestricted Resource Allocation**
Creating large objects in memory without proper checks can exhaust memory resources.

##### Node.js
```typescript
function allocateMemory(size: number) {
    let largeArray = new Array(size);  // Large allocation based on size
}

allocateMemory(10**8);  // Allocating a huge array which can exhaust memory
```

##### Angular
```typescript
export class ResourceIntensiveComponent {
  largeData: number[] = [];

  consumeResources(size: number) {
    this.largeData = new Array(size).fill(0);  // Fills memory with zeros
  }
}
```

#### 3. **Unrestricted File Upload**
Allowing users to upload files without size restrictions can lead to disk space exhaustion.

##### Node.js with Express
```typescript
const express = require('express');
const multer = require('multer');
const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('file'), (req, res) => {
  res.send('File uploaded successfully.');
});

app.listen(3000);
```
*No size limits, which can exhaust server disk space.*

#### 4. **Uncontrolled Concurrent Tasks**
Running too many concurrent tasks can overwhelm the CPU and memory.

##### Node.js
```typescript
const tasks = [];
for (let i = 0; i < 1000000; i++) {
    tasks.push(new Promise((resolve, reject) => {
        setTimeout(resolve, 1000);
    }));
}

Promise.all(tasks).then(() => {
    console.log('All tasks done');
});
```

##### Angular
```typescript
export class AppComponent {
  tasks: Promise<any>[] = [];

  ngOnInit() {
    for (let i = 0; i < 1000000; i++) {
      this.tasks.push(new Promise((resolve, reject) => {
        setTimeout(resolve, 1000);
      }));
    }

    Promise.all(this.tasks).then(() => {
      console.log('All tasks done');
    });
  }
}
```

### Writing SAST Rules for Detection

To write effective SAST rules for detecting uncontrolled resource consumption in TypeScript applications, consider focusing on:
1. **Detecting Infinite Loops and Recursions**: Look for constructs such as `while (true)`, `for (;;)` which indicate potential infinite loops.
2. **Resource Allocation Without Limits**: Identify instances where large objects or arrays are created based on user input or without clear bounds.
3. **File Uploads Without Limits**: Ensure uploads are checked for size restrictions using `multer` or equivalent middleware in Node.js.
4. **Uncontrolled Concurrency**: Detect large numbers of concurrent tasks being created in loops.

**Key Points for Detection Rules**:
- **Pattern Matching**: Use pattern matching to identify potential infinite loops or unbounded allocations.
- **Context Awareness**: Ensure the rule understands the context of the detected pattern to avoid false positives, such as loops that clearly have break conditions.
- **API-specific Checks**: Recognize specific API calls like `multer`, `Promise.all`, and their potential misuse.

Here is an example detection rule for **uncontrolled resource allocation**:
```xml
<rule id="typescript_uncontrolled_allocation" severity="high">
    <pattern>new Array($size$)</pattern>
    <message>Potential uncontrolled resource allocation detected. Ensure that $size$ is validated and limited to prevent resource exhaustion.</message>
    <confidence>high</confidence>
</rule>
```

In summary, uncontrolled resource consumption can severely impact the availability and performance of applications. Detecting these issues in TypeScript requires a thorough understanding of common patterns and framework-specific APIs. Writing precise SAST rules targeting these patterns can help minimize false negatives while maintaining a low false positive rate, ensuring applications are robust against resource exhaustion attacks.