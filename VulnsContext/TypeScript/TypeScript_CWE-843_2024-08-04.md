# Access of Resource Using Incompatible Type ('Type Confusion') (CWE-843) in TypeScript

###### Access of Resource Using Incompatible Type ('Type Confusion')

**Definition:**
Access of resource using incompatible type, also known as 'Type Confusion', refers to vulnerabilities that occur when a variable or object is treated as a different type than it was originally intended or created as. This can lead to unauthorized data access, data corruption, or arbitrary code execution within the context of the running application.

### Type Confusion in TypeScript

Type Confusion in TypeScript can lead to various types of vulnerabilities, especially in applications using popular frameworks such as React, Angular, and Node.js. Here are some variations of how type confusion can occur:

#### 1. **Direct Type Misinterpretation**
   **Example:** A function may expect a specific type, but it receives and processes an incompatible type.
   ```typescript
   // This function expects a number array but might receive a mixed-type array.
   function calculateSum(numbers: number[]) {
       return numbers.reduce((sum, num) => sum + num);
   }

   const mixedArray: any = [1, '2', 3];
   console.log(calculateSum(mixedArray)); // TypeScript does not catch this at runtime
   ```

#### 2. **Improper Casting**
   **Example:** Using `any` type to cast objects can introduce type confusion by bypassing TypeScript's type-checking capabilities.
   ```typescript
   let data: any = {name: "John", id: 12345};
   let employee = data as Employee; // Incorrectly casts the object to Employee
   console.log(employee.name.toUpperCase()); // Works fine
   console.log(employee.id * 2); // Type conflict if id is not a number, but no error at runtime
   ```

### Type Confusion in Frameworks

#### **React**
1. **Props Misinterpretation**
   **Example:** A component expects props of a certain type but receives another.
   ```typescript
   type UserProps = { name: string; age: number };
   const UserInfo: React.FC<UserProps> = ({ name, age }) => {
       return <div>{name} is {age} years old.</div>;
   };

   const incorrectProps = { name: "Alice", age: "twenty-five" as any };
   // This will not cause an error in runtime but breaks type safety
   <UserInfo {...incorrectProps} />;
   ```

#### **Angular**
1. **Service Injection**
   **Example:** A service is injected expecting a specific type of dependency but receives an incompatible type.
   ```typescript
   import { Injectable } from '@angular/core';

   @Injectable({
       providedIn: 'root',
   })
   export class DataService {
       constructor(private httpClient: any) {} // Ideally should be HttpClient
      
       fetchData() {
           this.httpClient.get('api/data').subscribe(data => console.log(data));
       }
   }

   // In some old test files or main.ts, a mock object might be passed through manual instantiation
   const dataService = new DataService({}); // Instead of real HttpClient
   dataService.fetchData(); // This will lead to runtime errors
   ```

#### **Node.js**
1. **Parameter and Data Validation**
   **Example:** Accepting user input without proper validation can lead to processing unexpected types.
   ```typescript
   function processInput(input: string) {
       input = input.trim();
       // perform some operations
   }

   // A route handler might inadvertently pass non-string input
   app.post('/api/data', (req, res) => {
       processInput(req.body.data); // If data is not string, trim function might break
       res.send('Processed successfully');
   });
   ```

### Writing SAST Rules

#### Rule 1: **Detect Direct Type Misinterpretation**
A SAST rule should check if a function's parameter types are consistently maintained throughout the function body.

#### Rule 2: **Detect Improper Casting**
This rule should identify instances where `any` or `unknown` types are being cast into specific types without type checks.

#### Rule 3: **Detect Misinterpreted Props in React**
The rule should inspect React components to ensure that the types of props match the expected types defined in the component's prop-types or interface.

#### Rule 4: **Service Injection in Angular**
This rule should verify if the services or classes injected via Angular's DI match the expected types, especially in constructor injections.

#### Rule 5: **Parameter and Data Validation in Node.js**
Ensure user inputs are validated and sanitized before processing them in functions to avoid runtime type confusion.

By focusing on these rules, the SAST tool can significantly reduce the occurrence of type confusion vulnerabilities, ensuring that the applications remain robust and secure against unexpected type-based errors.

### Citations
- The information above is derived and adapted from general knowledge of type confusion and specific examples from common vulnerabilities in TypeScript and framework usage as detailed in the documented files .