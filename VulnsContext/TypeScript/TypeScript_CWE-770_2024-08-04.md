# Allocation of Resources Without Limits or Throttling (CWE-770) in TypeScript

###### Explanation of Allocation of Resources Without Limits or Throttling

**Allocation of Resources Without Limits or Throttling** refers to the programming practice where applications fail to impose restrictions or control over the consumption of system resources (CPU, memory, disk I/O, network bandwidth, or threads). This can lead to various Denial of Service (DoS) attacks as attackers may exploit these unbounded allocations to overwhelm the system, thus reducing its availability.

Effective mitigation often involves implementing rate limiting, imposing maximum thresholds on resource allocation, and validating all inputs to ensure they do not result in excessive resource consumption. Here are some critical comments and strategies discussed in the documents:

- **Input Based Resource Allocation**: Ensuring that user inputs do not drive unchecked resource-heavy operations.
- **Rate Limiting**: Implementing control to manage the rate of requests served by the application.
- **Timeouts**: Applying timeouts to long-running operations to prevent them from consuming resources indefinitely.
- **Cost Analysis**: Assessing the 'cost' of operations and rejecting or limiting overly expensive ones【4:0†source】【4:1†source】【4:2†source】【4:3†source】【4:4†source】.

### Examples in TypeScript and Variations Across Popular Frameworks

Below are examples of improper and proper handling of resource allocation in TypeScript, using popular frameworks like Express.js, NestJS, and basic Node.js applications.

#### 1. **Express.js**

**Improper Handling:**
```typescript
import express from 'express';

const app = express();

app.post('/process', (req, res) => {
    // Unchecked processing of user input, potentially consuming huge resources
    for (let i = 0; i < Number(req.body.iterations); i++) {
        // Intensive operation
    }
    res.send('Processing complete');
});

app.listen(3000);
```

**Proper Handling with Throttling and Limits:**
```typescript
import express from 'express';
import rateLimit from 'express-rate-limit';
import multer from 'multer';

const app = express();
const upload = multer({ limits: { fileSize: 1024 * 1024 } }); // Limit file size to 1MB

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

app.post('/process', upload.single('file'), (req, res) => {
    const iterations = Math.min(Number(req.body.iterations), 1000); // Limit iterations
    for (let i = 0; i < iterations; i++) {
        // Intensive operation
    }
    res.send('Processing complete');
});

app.listen(3000);
```

#### 2. **NestJS**

**Improper Handling:**
```typescript
import { Controller, Post, Body } from '@nestjs/common';

@Controller('process')
export class AppController {
  @Post()
  process(@Body() body: { iterations: number }) {
    for (let i = 0; i < body.iterations; i++) {
      // Intensive operation
    }
    return 'Processing complete';
  }
}
```

**Proper Handling with Throttling and Limits:**
```typescript
import { Controller, Post, Body, UseInterceptors } from '@nestjs/common';
import { ThrottlerGuard } from '@nestjs/throttler';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';

@Controller('process')
@UseGuards(ThrottlerGuard)
export class AppController {
  
  @Post()
  @UseInterceptors(FileInterceptor('file', {
    storage: diskStorage({}),
    limits: { fileSize: 1024 * 1024 } // 1MB limit
  }))
  process(@Body() body: { iterations: number }) {
    const iterations = Math.min(body.iterations, 1000); // Limit iterations
    for (let i = 0; i < iterations; i++) {
      // Intensive operation
    }
    return 'Processing complete';
  }
}
```

#### 3. **Node.js (without framework)**

**Improper Handling:**
```typescript
import http from 'http';

http.createServer((req, res) => {
    if (req.url === '/process' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            const { iterations } = JSON.parse(body);
            for (let i = 0; i < iterations; i++) {
                // Intensive operation
            }
            res.end('Processing complete');
        });
    }
}).listen(3000);
```

**Proper Handling with Throttling and Limits:**
```typescript
import http from 'http';
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});

const server = http.createServer((req, res) => {
    if (req.url === '/process' && req.method === 'POST') {
        limiter(req, res, () => {
            let body = '';
            req.on('data', chunk => body += chunk);
            req.on('end', () => {
                const { iterations } = JSON.parse(body);
                const limitedIterations = Math.min(iterations, 1000); // Limit iterations
                for (let i = 0; i < limitedIterations; i++) {
                    // Intensive operation
                }
                res.end('Processing complete');
            });
        });
    }
}).listen(3000);
```

### SAST Rule Criteria for Detection

To effectively detect instances of resource allocation without limits or throttling in TypeScript applications, a SAST rule could be designed to:

1. **Identify Unrestricted Loops or Recursions:**
   - Look for `for`, `while`, and recursion patterns without bounds or maximum thresholds.
   - Example Pattern: `for (let i = 0; i < input; i++) { ... }`, where `input` is user-controlled.

2. **Detect Lack of Rate Limiting/Throttling Middleware:**
   - In frameworks like Express.js, check for the absence of middleware such as `rateLimit`.
   - Example Pattern: Absence of `rateLimit` middleware usage within Express routes.

3. **Monitor File Upload Restrictions:**
   - Ensure file uploads use constraints like file size limits.
   - Example Pattern: Absence of `limits: { fileSize: ... }` in file upload configurations (e.g., `multer`).

4. **Check for Absence of Iteration Limits:**
   - Ensure iteration counts influenced by user input are clamped to a safe maximum.
   - Example Pattern: `const iterations = input.number` without a minimum/maximum value check.

By focusing on these patterns, the SAST tool can minimize false positives and false negatives, ensuring effective detection of potential resource allocation issues【4:4†source】【4:13†source】.