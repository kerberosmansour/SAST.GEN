# Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') (CWE-917) in TypeScript

###### Explanation of Improper Neutralization of Special Elements Used in an Expression Language Statement ('Expression Language Injection')

**Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')**, also known as EL Injection, occurs when user input is not appropriately sanitized and is directly included in an Expression Language (EL) statement. This allows for potentially malicious inputs to alter the intended evaluation of expressions, which can lead to a variety of vulnerabilities, including but not limited to code execution and data exposure.

Expression Languages allow for the dynamic resolution of variables, and are commonly used in various web frameworks to bind user interface elements to backend code. If user inputs are directly passed into these EL statements without proper sanitization, attackers can inject EL syntax to manipulate the application's logic.

### TypeScript and Popular Frameworks

Here I'll outline some examples of how EL Injection can manifest in TypeScript, particularly within popular frameworks like Angular.

#### Angular

Angular uses a template syntax that could be vulnerable if user inputs aren't properly handled. Angular templates also support expressions using double curly braces `{{...}}`.

1. **Direct Use in Bindings**:
    ```typescript
    // Potentially vulnerable template
    @Component({
      selector: 'app-example',
      template: `<div>{{ userInput }}</div>`
    })
    export class ExampleComponent {
      userInput: string = '';
    }

    // In a controller/service
    let userInputFromRequest = request.query.userInput; // Assume this is unsanitized user input
    this.userInput = userInputFromRequest;
    ```

    The unsanitized `userInput` can be manipulated by users to inject script or further Angular expressions, leading to potential security issues.

2. **In URL Routing Parameters**:
    ```typescript
    // In app-routing.module.ts
    const routes: Routes = [
      { path: 'user/:id', component: UserComponent }
    ];

    // In user.component.ts
    @Component({
      selector: 'app-user',
      template: `<div>{{ currentUser }}</div>`
    })
    export class UserComponent implements OnInit {
      currentUser: any;

      constructor(private route: ActivatedRoute, private userService: UserService) { }

      ngOnInit(): void {
        this.route.params.subscribe(params => {
          this.currentUser = this.userService.getUser(params['id']);
        });
      }
    }
    ```

    If `getUser` method directly uses the `id` parameter in an EL, it might lead to injections.

### Recommended SAST Rules

To detect EL Injection vulnerabilities with high accuracy, a SAST tool should focus on the following strategies:

1. **Identify Points of User Input**:
    - Pinpoint all instances where user input is accepted in application logic, such as forms, query parameters, and HTTP request bodies.

2. **Track Data Flow**:
    - Marker these inputs and trace their propagation through the application. Special attention should be paid to see if these inputs arrive in the template or expression contexts. 

3. **Check Expression Bindings**:
    - Examine Angular template expressions or similar constructs in other frameworks to ensure user inputs are not directly embedded without sanitation.

4. **Sanitization Checks**:
    - Ensure inputs destined for EL or template use undergo robust sanitization routines. Angular provides built-in sanitation mechanisms that SAST tools need to check for:
        ```typescript
        import { DomSanitizer } from '@angular/platform-browser';

        constructor(private sanitizer: DomSanitizer) {}

        safeHtmlContent(html: string) {
          return this.sanitizer.bypassSecurityTrustHtml(html);
        }
        ```

5. **Prevent Direct Code Execution**:
    - Direct usages of dynamic code executions methods like `eval`, `Function`, or any method that executes strings as code should be highlighted as potential injection points.

### Example SAST Pattern

For a more concrete example, consider the following SAST rule logic in pseudo-code:

1. **Detect User Inputs**:
    - `function detectUserInputs(ast) { /* Returns an array of user input variables and their data flows */ }`

2. **Identify Template Bindings**:
    - `function detectTemplateBindings(ast) { /* Returns an array of template bindings */ }`

3. **Sanitization Check**:
    - `function isSanitized(bindingExpression) { /* Returns true if the expression undergoes sanitization before usage */ }`

4. **Rule Logic**:
    ```typescript
    const userInputs = detectUserInputs(ast); // Detect user inputs
    const bindings = detectTemplateBindings(ast); // Detect template bindings

    for (const binding of bindings) {
      for (const input of userInputs) {
        if (binding.includes(input.variable) && !isSanitized(binding)) {
          reportVulnerability(binding, input);
        }
      }
    }
    ```

In summary, detecting Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') entails tracking the propagation of user inputs through the application's data flows and ensuring that they are properly sanitized before being safely embedded in expression contexts. For TypeScript applications using Angular, this means closely monitoring template expressions and ensuring robust input sanitization practices are consistently applied. 

Citations from the provided resources:
- 【4:0†source】
- 【4:1†source】
- 【4:2†source】
- 【4:3†source】
- 【4:4†source】
- 【4:5†source】
- 【4:6†source】
- 【4:7†source】
- 【4:8†source】
- 【4:9†source】
- 【4:10†source】
- 【4:11†source】
- 【4:12†source】