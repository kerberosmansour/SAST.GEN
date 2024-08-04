# Integer Overflow or Wraparound (CWE-190) in TypeScript

###### Understanding Integer Overflow or Wraparound

#### Overview
Integer Overflow or Wraparound occurs when an arithmetic operation attempts to create a numeric value that is outside of the range that can be represented with a given number of bits. When this happens in an unsigned integer scenario, it wraps around starting again from zero. In signed integers, exceeding the range can switch the sign bit, potentially leading to unexpected and typically incorrect results.

### Integer Overflow or Wraparound in TypeScript

#### Common Variations

1. **Arithmetic Operations**:
    ```typescript
    let a: number = Number.MAX_SAFE_INTEGER;
    a += 1;
    console.log(a); // This may output an incorrect value due to overflow.
    ```

2. **Type Conversion**:
    ```typescript
    let largeNumber: string = "9007199254740992"; // Greater than Number.MAX_SAFE_INTEGER
    let num: number = parseInt(largeNumber); 
    console.log(num); // The parsed number may not be accurate leading to undefined behavior.
    ```

3. **Frameworks Usage**:

    - **Node.js**:
        ```typescript
        const fs = require('fs');
        
        let buffer = new Buffer(4);
        buffer.writeInt32BE(Number.MAX_SAFE_INTEGER+1, 0);  // This will lead to overflow in the buffer.
        console.log(buffer.readInt32BE(0));
        ```

    - **Angular**:
        ```typescript
        import { Component } from '@angular/core';

        @Component({
          selector: 'app-root',
          template: `<div>The Value is: {{ largeValue }}</div>`
        })
        export class AppComponent {
          largeValue: number = Number.MAX_SAFE_INTEGER + 1; // Unsafe integer usage
        }
        ```

    - **React**:
        ```typescript
        import React from 'react';

        function App() {
          let largeValue = Number.MAX_SAFE_INTEGER + 1; // Overflow might occur here
          return (
            <div>
              The Value is: {largeValue}
            </div>
          );
        }

        export default App;
        ```

### For SAST Tool Detection

To write high accuracy rules for detecting Integer Overflow or Wraparound in TypeScript, focus on the following patterns:

1. **Arithmetic Operations Close to Limits**:
    - **Pattern**: Detect arithmetic operations involving `Number.MAX_SAFE_INTEGER` and `Number.MIN_SAFE_INTEGER`.
    - **Rule**: Alert if any arithmetic operation (`+`, `-`, `*`, `/`) involves these constants.

2. **Large Number Literals**:
    - **Pattern**: Look for numeric literals that exceed `Number.MAX_SAFE_INTEGER`.
    - **Rule**: Alert when such numbers are used without proper validation.

3. **Buffer Operations**:
    - **Pattern**: Use of buffers with values that may exceed 32-bit or 64-bit limits.
    - **Rule**: Pay attention to methods like `buffer.writeInt32BE` or `buffer.writeInt32LE` with unvalidated large values.

4. **Potential conversions**:
    - **Pattern**: Look out for `parseInt`, `parseFloat`, `Number` constructors, or similar functions where there's a risk of overflow.
    - **Rule**: Raise potential warnings if the input is not validated against safe integer range.

### Example SAST Rule in Pseudocode

```typescript
rule IntegerOverflowCheck {
    pattern = [
        "let $V = Number.MAX_SAFE_INTEGER $OP $N;",
        "let $V = Number.parseInt($L);",
        "$buffer.writeInt32BE($VAL, $OFFSET);",
    ];

    report match {
        message: "Potential Integer Overflow detected",
        suggest: "Ensure the values and operations are within safe integer limits."
    }
}
```

### Summary
Ensuring security in JavaScript and TypeScript applications involves careful validation of operations involving large numbers, especially near the boundaries of JavaScript's integer limits. By focusing on these crucial elements, SAST tools can be finely tuned to identify real potential overflows while minimizing false positives and false negatives.

For references and deeper dives into various warnings and suppression techniques, the pertinent knowledge was derived from the provided documents 【4:12†source】.