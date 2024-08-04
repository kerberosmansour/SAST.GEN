# Integer Overflow or Wraparound (CWE-190) in JavaScript

###### Understanding Integer Overflow or Wraparound

**Integer Overflow** and **Wraparound** refer to conditions that occur when an arithmetic operation attempts to create a numeric value that is outside the range that can be represented with a given number of bits. 

In the context of programming, especially in languages like JavaScript, this can lead to unexpected behavior and is considered a vulnerability.

Here's an example in a lower-level language, C, to understand the basic concept:

```c
#include <limits.h>
#include <stdio.h>

int main() {
    unsigned int max = UINT_MAX;
    printf("Max unsigned int: %u\n", max);
    max = max + 1;
    printf("After overflow: %u\n", max);
    return 0;
}
```

In this example, `UINT_MAX` represents the maximum value of an `unsigned int`. Incrementing it by 1 causes an overflow, which results in wrapping around to 0, illustrating the Wraparound concept【4:0†source】.

### Variations and Examples in JavaScript

JavaScript, being a high-level language, also suffers from integer overflow and wraparound, especially due to its handling of numbers. JavaScript numbers are represented in double-precision 64-bit binary format (IEEE 754). However, operations may still overflow and result in incorrect values, especially when dealing with integer-specific logic.

#### Example 1: Basic Arithmetic Overflow

```javascript
let maxInt = Number.MAX_SAFE_INTEGER; // 2^53 - 1
console.log(maxInt); // 9007199254740991

let overflow = maxInt + 1;
console.log(overflow); // 9007199254740992

overflow = maxInt + 2;
console.log(overflow); // 9007199254740992 -- Incorrect!
```

In this example, adding 2 to `Number.MAX_SAFE_INTEGER` should result in `9007199254740993` but due to overflow, JavaScript lacks precision and incorrectly repeats `9007199254740992`【4:1†source】.

#### Example 2: Multiplication Overflow

```javascript
let a = 1e308;
let b = 2;

let overflow = a * b;
console.log(overflow); // Infinity
```

Here, multiplying two large numbers results in `Infinity`, demonstrating overflow.

#### Example 3: Framework Example (React.js)

In React or any framework that involves state management, accidental overflow can lead to significant issues.

```javascript
class Counter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      count: Number.MAX_SAFE_INTEGER
    };
  }

  increment = () => {
    this.setState(prevState => ({
      count: prevState.count + 1
    }));
  }

  render() {
    return (
      <div>
        <button onClick={this.increment}>Increment</button>
        <p>{this.state.count}</p>
      </div>
    );
  }
}
```

In this example, clicking the increment button enough times will cause the `count` state to exceed `Number.MAX_SAFE_INTEGER`, leading to incorrect state representation【4:1†source】.

### SAST Rule Detection for Integer Overflow/Wraparound

To detect and prevent integer overflow or wraparound in SAST (Static Application Security Testing) tools, writing rules requires:

1. **Identifying Maximum Safe Limits:** Detect usage of `Number.MAX_SAFE_INTEGER` and verify subsequent operations.
2. **Checking Arithmetic Operations:** Monitor arithmetic operations involving large integers, especially addition, subtraction, multiplication, and division.
3. **Watch for Infinity and NaN:** Ensure that results are checked for `Infinity` or `NaN` immediately following arithmetic operations.
4. **Framework-Specific Patterns:** In frameworks like React, Vue, or Angular, monitor state and props setters for potential overflow risks.

#### Example of SAST Rule (Pseudo-code)

```pseudo
rule JavaScript_Integer_Overflow {
  pattern = [
    "[var|let|const] <identifier> = Number.MAX_SAFE_INTEGER;",
    "<identifier> [operator] [number|<identifier>]"
  ]
  message = "Possible Integer Overflow. Ensure the operation does not exceed the safe integer range."
}

rule JavaScript_Infinity_Check {
  pattern = [
    "<identifier> = <expression>;",
    "if (<identifier> === Infinity) {...}"
  ]
  message = "Infinity check required after large number computation."
}
```

In summary, Integer Overflow and Wraparound can cause significant issues in JavaScript, especially within large-scale applications using popular frameworks. Writing SAST rules to catch such vulnerabilities involves monitoring large number operations and ensuring their results remain within safe limits【4:1†source】【4:10†source】.