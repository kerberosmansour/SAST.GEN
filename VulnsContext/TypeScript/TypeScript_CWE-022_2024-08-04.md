# Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (CWE-022) in TypeScript

###### Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')

Improper Limitation of a Pathname to a Restricted Directory, commonly known as 'Path Traversal', occurs when the software uses external input to construct a pathname that is intended to identify a file or directory but does not properly validate this input. This can allow unauthorized users to access files and directories outside the typical filesystem hierarchy. According to CWE-22, this issue can be represented by the following threat: 

> "The software uses external input to construct a pathname that is intended to identify a file or directory that is located underneath a restricted parent directory but does not properly neutralize special elements within the pathname that can cause the pathname to resolve to a location that is outside of the restricted directory"【4:0†source】.

### Path Traversal in TypeScript

To address creating SAST rules to detect 'Path Traversal' vulnerabilities in TypeScript, it's essential to understand the potential variations of this vulnerability. Below are different scenarios and variations on how Path Traversal can occur in TypeScript, especially within popular frameworks like Express.js, NestJS, and others.

#### Example 1: Express.js

##### Scenario 1: Direct File Access using Untrusted Input

```typescript
import * as express from 'express';
import * as path from 'path';

const app = express();

app.get('/file', (req, res) => {
  const fileName = req.query.fileName;
  const filePath = path.join(__dirname, 'public', fileName);
  
  res.sendFile(filePath);
});
```

Here, the `fileName` is taken directly from the user input (`req.query.fileName`) without validation. An attacker can manipulate this input to traverse the filesystem.

##### Scenario 2: Using `path.normalize`

```typescript
import * as express from 'express';
import * as path from 'path';

const app = express();

app.get('/file', (req, res) => {
  const fileName = req.query.fileName;
  let filePath = path.normalize(path.join(__dirname, 'public', fileName));
  
  // Ensure the file path starts with the expected directory
  if (!filePath.startsWith(path.join(__dirname, 'public'))) {
    return res.status(400).send('Invalid file path');
  }

  res.sendFile(filePath);
});
```

Although using `path.normalize` helps, improperly sanitized input may still allow traversal.

#### Example 2: NestJS

##### Scenario 1: Poor Input Sanitization

```typescript
import { Controller, Get, Query, Res } from '@nestjs/common';
import { Response } from 'express';
import { join } from 'path';

@Controller('files')
export class FilesController {
  @Get()
  getFile(@Query('fileName') fileName: string, @Res() res: Response) {
    const filePath = join(__dirname, 'public', fileName);
    res.sendFile(filePath);
  }
}
```

Again, `fileName` from the query string can be exploited for directory traversal without proper sanitization.

#### Example 3: File Systems in Node.js

##### Scenario 1: Reading Files

```typescript
import * as http from 'http';
import * as fs from 'fs';
import * as path from 'path';

http.createServer((req, res) => {
  const fileName = new URL(req.url, 'http://example.com').searchParams.get('fileName');
  const filePath = path.join(__dirname, 'files', fileName);
  
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(400);
      res.end('Error reading file');
    } else {
      res.writeHead(200);
      res.end(data);
    }
  });
}).listen(3000);
```

Same issue arises with Node.js filesystem methods where user input is directly used to construct file paths.

### Ensuring High Detection Accuracy 

For a SAST tool, the following strategies can reduce false positives and negatives:

1. **Path Joins with User Input**: Flag any instance where path joins concatenate a user-controlled input directly.

2. **Normalize and Checks**: Ensure that the path is normalized (`path.normalize`) and checked thoroughly against the expected directory using robust measures like `startsWith`, ensuring it matches precisely.

3. **Library-Specific Translations**: Extend the rules to identify Path Traversal issues in common frameworks such as detecting `res.sendFile(...)`, `fs.readFile(...)`, and equivalents in NestJS, Express, or other framework-specific methods where pathnames are manipulated.

4. **Parameter Usage Analysis**: Trace the path parameters flow from input retrieval (e.g., `req.query`, `req.params`, `req.body`) to filesystem utilities, identifying potential misuse.

By leveraging these techniques and the examples provided, your SAST tool can better detect 'Path Traversal' vulnerabilities in TypeScript with greater precision, minimizing false positives and negatives【4:0†source】【4:1†source】【4:2†source】.