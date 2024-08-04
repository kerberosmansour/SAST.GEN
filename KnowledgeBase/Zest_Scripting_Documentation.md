
# Zest Scripting Documentation

This documentation covers the fundamentals of Zest scripting within OWASP ZAP (Zed Attack Proxy). Zest is a specialized scripting language developed by Mozilla for automating web security tasks. This guide outlines how to create, edit, and run Zest scripts, and describes the key components of the language.

---

## 1. **Introduction to Zest**

Zest is a scripting language that allows security testers to automate tasks such as vulnerability scanning, fuzzing, and data extraction. Zest scripts are created and edited within the ZAP GUI, and they can also be run from the command line. Zest is designed to be user-friendly and can be used even by those with limited scripting experience.

### Key Features:
- **Graphical Script Creation:** Scripts are created and modified within ZAP using a graphical interface.
- **Reusable and Shareable Scripts:** Scripts can be exported, imported, and shared among users.
- **Automation:** Ideal for automating repetitive security tasks and for testing web applications for common vulnerabilities.

---

## 2. **Zest Script Components**

A Zest script is composed of multiple elements, each serving a specific purpose within the script. These elements include actions, conditionals, requests, and assertions.

### 2.1. **Actions**
Actions are operations that cause something to happen in the script. Common actions include:
- **Fail Action:** Indicates a script failure, often used after a conditional statement to signal a triggered vulnerability.
- **Scan Action:** Triggers a security scan on the last accessed URL.
- **Set Token Action:** Extracts and sets tokens from the response data for later use in the script.

Example of a Fail Action in JSON:
```json
{
  "message": "There is an XSS vulnerability in the 'search' parameter",
  "index": 1,
  "elementType": "ZestActionFail"
}
```

### 2.2. **Conditionals**
Conditionals are statements that control the flow of the script based on specific conditions. These include:
- **Regex Conditional:** Checks if a specified regular expression is present in a given location (e.g., response body).
- **Response Time Conditional:** Tests whether the response time is greater or less than a specified value.
- **Status Code Conditional:** Verifies if the HTTP status code matches a given value.

Example of a Regex Conditional in JSON:
```json
{
  "regex": "alert(1);",
  "location": "BODY",
  "ifStatements": [],
  "elseStatements": [],
  "index": 2,
  "elementType": "ZestConditionRegex"
}
```

### 2.3. **Requests**
Requests are instructions to interact with a web application. They specify the URL, HTTP method, data, and headers required for the interaction.

Example of a Request in JSON:
```json
{
  "url": "http://www.example.com/test?aaa=bbb&ccc=ddd",
  "method": "GET",
  "headers": "",
  "index": 1,
  "elementType": "ZestRequest"
}
```

### 2.4. **Assertions**
Assertions are checks applied to responses to ensure they meet expected conditions. Common assertions include:
- **Body Regex Assertion:** Verifies that the response body matches a regular expression.
- **Header Regex Assertion:** Ensures specific headers match a regex pattern.
- **Response Length Assertion:** Checks if the response length is within an expected range.
- **Status Code Assertion:** Validates that the HTTP status code matches an expected value.

Example of a Status Code Assertion in JSON:
```json
{
  "rootExpression": {
    "code": 200,
    "not": false,
    "elementType": "ZestExpressionStatusCode"
  },
  "elementType": "ZestAssertion"
}
```

---

## 3. **Creating and Editing Zest Scripts**

Zest scripts are typically created and edited using the ZAP graphical interface:

1. **Create a New Script:**
   - Right-click within the ZAP interface and select "New Script."
   - Choose "Zest Script" as the type.

2. **Adding Components:**
   - Add requests, actions, conditionals, and assertions by right-clicking and selecting the appropriate options.

3. **Using Variables:**
   - Zest supports variables, which can be assigned values and reused throughout the script.

4. **Recording Scripts:**
   - ZAP allows recording of actions in a web browser, which are automatically converted into Zest script actions.

---

## 4. **Running Zest Scripts**

Zest scripts can be executed directly from the ZAP interface or from the command line using the Zest Java Reference library. The command-line usage is as follows:

```bash
./bin/zest -script <file> [-summary | -list] [-prefix <http://prefix>] [-token <name>=<value>] ...
```

Parameters:
- **-script:** Specifies the Zest script to use.
- **-summary:** Displays a summary of the script without running it.
- **-list:** Lists the script components without running it.
- **-prefix:** Replaces the URL prefix in the script.
- **-token:** Sets token values when the script is run.

---

## 5. **Use Cases**

Zest scripts are versatile and can be used for various tasks including:
- **Reproducing Security Vulnerabilities:** Automate the process of reproducing vulnerabilities found during security assessments.
- **Automating Common Tasks:** Automate repetitive tasks like account registration and web application fuzzing.
- **Security Assessments:** Perform automated security assessments by sending customized requests and analyzing responses.

---

## 6. **Advanced Features**

- **Environmental Variables:** Zest scripts can interact with environmental variables to share data between different scripts or tools.
- **Active and Passive Scanning:** Create custom scan rules to identify vulnerabilities during active and passive scanning.

---

## 7. **Zest Script Structure Example**

Below is an example of a complete Zest script in JSON format:

```json
{
  "about": "This is a Zest script. For more details about Zest visit https://github.com/zaproxy/zest/",
  "zestVersion": "0.8",
  "title": "BodgeIt Register XSS",
  "description": "This Zest script demonstrates the XSS issue in the BodgeIt Register page.",
  "prefix": "http://localhost:8080/bodgeit",
  "statements": [
    {
      "url": "http://localhost:8080/bodgeit/home.jsp",
      "method": "GET",
      "response": { "statusCode": 200 },
      "assertions": [
        { "rootExpression": { "code": 200, "elementType": "ZestExpressionStatusCode" } }
      ],
      "elementType": "ZestRequest"
    },
    // More statements
  ],
  "elementType": "ZestScript"
}
```

This script demonstrates various Zest components and how they can be structured to automate a security test.

---

## 8. **Contributing and Feedback**

The Zest scripting framework is open-source, and contributions are welcomed. Teams and individuals who develop security tools are encouraged to participate in the development of Zest. Feedback is also appreciated to help improve the language and its documentation.

For more details about Zest, visit the [Zest GitHub repository](https://github.com/zaproxy/zest/).


## 9. **Detailed Action Descriptions**

### 9.1. **Fail Action**
The Fail action is used to indicate that the script has not been successful. It is typically a child of a conditional statement and used to indicate that a vulnerability has been triggered.

#### Attributes:
- **message (String):** The failure message to display to the user.
- **index (Integer):** The index of the statement in the script.
- **elementType (String):** Always "ZestActionFail".

#### JSON Example:
```json
{
  "message": "There is an XSS vulnerability in the 'search' parameter",
  "index": 1,
  "elementType": "ZestActionFail"
}
```

### 9.2. **Scan Action**
The Scan action causes the URL last accessed to be scanned for security vulnerabilities. This action is not supported by the default Zest runtime - it is expected to be supported by security tools that include Zest.

#### Attributes:
- **targetParameter (String):** The parameter to attack - note that tools may ignore this and attack all parameters.
- **index (Integer):** The index of the statement in the script.
- **elementType (String):** Always "ZestActionScan".

If a vulnerability is found, the script should fail.

#### JSON Example:
```json
{
  "targetParameter": "search",
  "index": 1,
  "elementType": "ZestActionScan"
}
```

### 9.3. **Set Token Action**
This action allows the script to set tokens from data returned in the last response which can be used later in the script.

#### Attributes:
- **tokenName (String):** The name of the token.
- **prefix (String):** The string in the response which immediately precedes the token value.
- **postfix (String):** The string in the response which is immediately after the token value.
- **index (Integer):** The index of the statement in the script.
- **elementType (String):** Always "ZestActionSetToken".

When a Zest Token Action is encountered, the Zest runtime will set the token value to the string between the first occurrences of the prefix and postfix. If either the prefix or postfix are not found in the response, the runtime should report an error.

#### JSON Example:
```json
{
  "tokenName": "userid",
  "prefix": "your user id is: ",
  "postfix": "\n",
  "index": 2,
  "elementType": "ZestActionSetToken"
}
```

## 10. **Assertions**

### 10.1. **Zest Assertions**
Zest Assertions are 'sanity checks' associated with requests and applied to responses. A failing assertion typically indicates that the test is not working as expected - either the script is incorrect or the script has not been configured correctly for the target application.

#### Types of Assertions:
- **Assert Body Regex:** Verifies that the response body matches a regular expression.
- **Assert Header Regex:** Ensures specific headers match a regex pattern.
- **Assert Response Length:** Checks if the response length is within an expected range.
- **Assert Response Status Code:** Validates that the HTTP status code matches an expected value.

### 10.2. **Conditionals**
Zest Conditionals are statements that provide IF / THEN / ELSE functionality. All conditional statements test for a particular condition and provide two alternate paths. Each path may contain zero or more statements, and these can include conditionals to any depth.

#### Types of Conditionals:
- **Regex Conditional:** Tests whether the specified regex is present.
- **Response Time Conditional:** Tests the time taken for the last response.
- **Status Code Conditional:** Tests the status code of the last response.

#### Example of Regex Conditional in JSON:
```json
{
  "regex": "alert(1);",
  "location": "BODY",
  "ifStatements": [],
  "elseStatements": [],
  "index": 2,
  "elementType": "ZestConditionRegex"
}
```

### 10.3. **Command Line Usage**
The Zest Java Reference library can run scripts from the command line. After building and unpacking the standalone command-line application (e.g., zest-0.16.0.zip), you can run it with the following options:

#### Usage:
```bash
./bin/zest -script <file> [-summary | -list] [-prefix <http://prefix>] [-token <name>=<value>] ...
```

#### Supported Parameters:
- **-script:** Allows you to specify the Zest script to use.
- **-summary:** Displays a summary of the Zest script without running it.
- **-list:** Lists the Zest script without running it.
- **-prefix:** Replaces the prefix with the one specified when the script is run.
- **-token:** Sets the specified token values when the script is run.
- **-http-auth-site:** Replaces the HTTP authentication site with the one specified when the script is run.
- **-http-auth-realm:** Replaces the HTTP authentication realm with the one specified when the script is run.
- **-http-auth-user:** Replaces the HTTP authentication user with the one specified when the script is run.
- **-http-auth-password:** Replaces the HTTP authentication password with the one specified when the script is run.

---

For more details about Zest, visit the [Zest GitHub repository](https://github.com/zaproxy/zest/).


## Zest Script Structure: BodgeIt Register XSS

This section provides details about a Zest script designed to demonstrate an XSS issue in the BodgeIt Register page.

### Zest Script Metadata

```json
{
  "about": "This is a Zest script. For more details about Zest visit https://github.com/zaproxy/zest/",
  "zestVersion": "0.8",
  "generatedBy": "ZAP Dev Build",
  "title": "BodgeIt Register XSS",
  "description": "This Zest script demonstrates the XSS issue in the BodgeIt Register page. It uses a 'random integer replacement' transformation to ensure a new user is registered each time the script is run.",
  "prefix": "http://localhost:8080/bodgeit",
  "parameters": {
    "tokenStart": "{{",
    "tokenEnd": "}}",
    "tokens": {},
    "elementType": "ZestVariables"
  }
}
```

- **about**: A brief description of the script and where to find more information about Zest.
- **zestVersion**: Specifies the version of Zest the script is compatible with.
- **generatedBy**: Indicates the tool or build that generated the script.
- **title**: A short title describing the script’s purpose.
- **description**: A detailed explanation of what the script does. In this case, it highlights the XSS issue in the BodgeIt Register page and mentions the use of a random integer replacement transformation.
- **prefix**: The URL prefix common to all requests in the script.
- **parameters**: Defines the structure of tokens used within the script.

### Requests and Responses

The script contains multiple requests and responses to demonstrate the vulnerability. Below are the details:

1. **Home Page Request**

   ```json
   {
     "url": "http://localhost:8080/bodgeit/home.jsp",
     "data": "",
     "method": "GET",
     "headers": "",
     "response": {
       "headers": "HTTP/1.1 200 OK\r\nServer: Apache-Coyote/1.1\r\nContent-Type: text/html;charset=ISO-8859-1\r\nContent-Length: 3233\r\nDate: Fri, 05 Apr 2013 10:02:00 GMT\r\n\r\n",
       "body": "",
       "statusCode": 200,
       "responseTimeInMs": 21,
       "elementType": "ZestResponse"
     },
     "assertions": [
       {
         "rootExpression": {
           "code": 200,
           "not": false,
           "elementType": "ZestExpressionStatusCode"
         },
         "elementType": "ZestAssertion"
       },
       {
         "rootExpression": {
           "length": 3233,
           "approx": 2,
           "variableName": "response.body",
           "not": false,
           "elementType": "ZestExpressionLength"
         },
         "elementType": "ZestAssertion"
       }
     ],
     "followRedirects": true,
     "cookies": [],
     "index": 1,
     "enabled": true,
     "elementType": "ZestRequest"
   }
   ```

   - **url**: The URL of the home page.
   - **method**: HTTP method used (GET).
   - **response**: The expected response, including headers, body, status code, and response time.
   - **assertions**: Checks applied to the response, ensuring the status code is 200 and the response length matches expectations.


### Request Details (Login Page)

- **URL**: `http://localhost:8080/bodgeit/login.jsp`
- **Method**: GET
- **Response Details**:
  - **Headers**: 
    ```
    HTTP/1.1 200 OK
    Server: Apache-Coyote/1.1
    Content-Type: text/html;charset=ISO-8859-1
    Content-Length: 2470
    Date: Fri, 05 Apr 2013 10:02:02 GMT
    ```
  - **Body**:
    ```html
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
    <html>
    <head>
    <title>The BodgeIt Store</title>
    <link href="style.css" rel="stylesheet" type="text/css" />
    <script type="text/javascript" src="./js/util.js"></script>
    </head>
    <body>
    <center>
    <table width="80%" class="border">
    <tr BGCOLOR="#C3D9FF">
    <td align="center" colspan="6">
    <H1>The BodgeIt Store</H1>
    <table width="100%" class="noborder">
    <tr BGCOLOR="#C3D9FF">
    <td align="center" width="30%">&nbsp;</td>
    <td align="center" width="40%">We bodge it, so you dont have to!</td>
    <td align="center" width="30%" style="text-align: right" >Guest user</td>
    </tr>
    </table>
    </td>
    </tr>
    <tr>
    <td align="center" width="16%" BGCOLOR="#EEEEEE"><a href="home.jsp">Home</a></td>
    <td align="center" width="16%" BGCOLOR="#EEEEEE"><a href="about.jsp">About Us</a></td>
    <td align="center" width="16%" BGCOLOR="#EEEEEE"><a href="contact.jsp">Contact Us</a></td>
    <td align="center" width="16%" BGCOLOR="#EEEEEE"><a href="login.jsp">Login</a></td>
    <td align="center" width="16%" BGCOLOR="#EEEEEE"><a href="basket.jsp">Your Basket</a></td>
    <td align="center" width="16%" BGCOLOR="#EEEEEE"><a href="search.jsp">Search</a></td>
    </tr>
    </table>
    </center>
    </body>
    </html>
    ```
  - **Status Code**: 200
  - **Response Time**: 5 ms

- **Assertions**:
  - Status Code Assertion: The status code should be 200.
  - Response Length Assertion: The length of the response body should be approximately 2470 bytes.
  - Both assertions ensure that the login page is functioning correctly before proceeding with further actions in the script.
  
- **Request Index**: 2
- **Follow Redirects**: `true`
- **Cookies**: No cookies used in this request
- **Enabled**: `true`
