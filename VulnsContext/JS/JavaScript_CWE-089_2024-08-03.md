# Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') (CWE-089) in JavaScript

###### Explanation of SQL Injection

**Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')**, known as SQL injection, is a vulnerability that occurs when an attacker is able to manipulate the SQL queries that an application sends to a database. This type of attack can lead to unauthorized data disclosure, modification, and other destructive actions against the database.

---

### How SQL Injection Occurs

Here's a basic example of vulnerable code:
```java
String query = "SELECT * FROM users WHERE username = '" + inputUsername + "' AND password = '" + inputPassword + "'";
```
In this example, if an attacker enters `admin' OR '1'='1` as the password, it would modify the SQL query to:
```sql
SELECT * FROM users WHERE username = 'admin' AND password = 'admin' OR '1'='1'
```
This is always true and would allow the attacker to bypass authentication.

---

### Improper Neutralization in JavaScript

In JavaScript, SQL Injection can occur in multiple ways, especially when using various frameworks and libraries for server-side applications. Below are examples from popular frameworks:

#### **1. Node.js with MySQL**

```javascript
const express = require('express');
const mysql = require('mysql');
const app = express();

app.get('/user', (req, res) => {
  const { username } = req.query;
  const query = `SELECT * FROM users WHERE username = '${username}'`;
  connection.query(query, function (error, results) {
    if (error) throw error;
    res.send(results);
  });
});
```
An attacker can pass `' OR '1'='1` as the username to manipulate the query.

#### **2. Sequelize (ORM for Node.js)**

```javascript
const Sequelize = require('sequelize');
const sequelize = new Sequelize('database', 'username', 'password');

app.get('/user', (req, res) => {
  const { username } = req.query;
  sequelize.query(`SELECT * FROM users WHERE username = '${username}'`)
    .spread((results, metadata) => {
      res.send(results);
    });
});
```
Again, passing malicious input as `username` will modify the SQL query.

#### **3. MongoDB with Mongoose (NoSQL Injection)**

```javascript
const mongoose = require('mongoose');
const User = mongoose.model('User');

app.get('/user', async (req, res) => {
  const { username } = req.query;
  const user = await User.findOne({ username: username });
  res.send(user);
});
```
Although MongoDB doesn't use SQL, a similar risk exists with queries constructed from unsanitized user input.

#### **4. REST APIs in Express**

```javascript
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
  db.query(query, (err, results) => {
    if (err) throw err;
    res.send(results);
  });
});
```
The input fields `username` and `password` are prone to injection if not sanitized.

---

### Examples for Detecting SQL Injection in SAST Tool

When creating SAST detection rules, look for the following patterns:

1. **String Concatenations in SQL Queries**:
    ```javascript
    const query = `SELECT * FROM users WHERE username = '${userInput}'`;
    ```
    Detect usage of variables directly within SQL strings.

2. **Use of Non-Parameterized ORM Queries**:
    ```javascript
    sequelize.query(`SELECT * FROM users WHERE username = '${userInput}'`);
    ```    
    ORM frameworks should use parameterized methods instead.

3. **Construction of MongoDB Queries with User Input**:
    ```javascript
    const user = await User.findOne({ username: userInput });
    ```
    Detect when user input is directly used in constructing queries without sanitation.

4. **Dynamic Queries in REST APIs**:
    ```javascript
    const query = `SELECT * FROM accounts WHERE user_id = '${req.params.id}'`;
    ```
    Look for patterns where HTTP request parameters are injected into queries.

### Proper Mitigations

To prevent SQL injections:

1. **Parameterized Queries**: Use placeholders for user input.
    ```javascript
    connection.query('SELECT * FROM users WHERE username = ?', [userInput]);
    ```

2. **ORM Input Sanitization**: 
    ```javascript
    User.findOne({ username: req.query.username }).exec();
    ```

3. **Validation and Sanitization**: Validate user input against expected patterns and sanitize appropriately to remove any harmful characters.

### References
- [Combined Top 10 Markdown](file-kpPPhxNd0ZV6Pibr5J2grG97)【4:10†source】
- [Combined Top 10 Markdown](file-YspBcHWW9s0N0MS934wsHOd1)【4:0†source】

---

Implementing the above patterns and mitigations in your detection logic for the Static Application Security Testing (SAST) tool will help in identifying vulnerabilities like SQL injection effectively.