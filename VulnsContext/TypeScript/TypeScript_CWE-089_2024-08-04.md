# Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') (CWE-089) in TypeScript

###### Explanation: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')

**SQL Injection (SQLi)** is a type of injection attack where an attacker can execute arbitrary SQL code on a database by manipulating the input to an SQL query. This occurs when user input is either concatenated directly into SQL queries, executed without adequate input sanitization, or not using parameterized queries. The predominant consequences of SQL injection are unauthorized viewing of data, data manipulation (insertion, modification, or deletion), and even administrative operations on the database.

Key Points:
1. **Improper Input Handling**: SQL injection arises from improper input handling, where user-provided data is not validated, sanitized, or bound to the query safely. 
2. **Dynamic Queries**: Usage of dynamic SQL queries without parameterization.
3. **ORMs and Frameworks**: Even within Object-Relational Mapping (ORM) tools or frameworks, if queries are not parameterized or if they concatenate raw input, vulnerabilities are introduced.

Common SQL Injection Variations in TypeScript Include:

1. **Inline SQL Queries**:
    ```typescript
    const { id } = req.params;
    const query = `SELECT * FROM users WHERE id = '${id}'`;
    db.query(query, (err, result) => {
        if (err) throw err;
        res.send(result);
    });
    ```

2. **Using Template Literals**:
    ```typescript
    const userId = req.query.id;
    const sqlQuery = `SELECT * FROM users WHERE userId = ${userId}`;
    connection.query(sqlQuery, (error, results) => {
        if (error) throw error;
        res.json(results);
    });
    ```

### SQL Injection in Popular Frameworks

1. **Express with MySQL**:
    - **Vulnerable Example**:
        ```typescript
        const userId = req.body.userId;
        const query = `DELETE FROM users WHERE userId = ${userId}`;
        connection.query(query, (error, results) => {
            if (error) {
                console.error("An error occurred while deleting the user: ", error);
                res.status(500).send('Internal Server Error');
            } else {
                res.send('User deleted successfully');
            }
        });
        ```
    - **Secure Example**:
        ```typescript
        const userId = req.body.userId;
        const query = `DELETE FROM users WHERE userId = ?`;
        connection.query(query, [userId], (error, results) => {
            if (error) {
                console.error("An error occurred while deleting the user: ", error);
                res.status(500).send('Internal Server Error');
            } else {
                res.send('User deleted successfully');
            }
        });
        ```

2. **TypeORM**:
    - **Vulnerable Example**:
        ```typescript
        const userId = req.query.id;
        const user = await getConnection()
            .createQueryBuilder()
            .select("user")
            .from(User, "user")
            .where(`user.id = ${userId}`)
            .getOne();
        ```
    - **Secure Example**:
        ```typescript
        const userId = req.query.id;
        const user = await getConnection()
            .createQueryBuilder()
            .select("user")
            .from(User, "user")
            .where("user.id = :id", { id: userId })
            .getOne();
        ```

3. **Sequelize**:
    - **Vulnerable Example**:
        ```typescript
        const userId = req.body.userId;
        const query = `UPDATE users SET email = '${req.body.newEmail}' WHERE id = ${userId}`;
        db.query(query).then(result => {
            res.status(200).send('Email updated successfully');
        }).catch(error => {
            res.status(500).send('Internal Server Error');
        });
        ```
    - **Secure Example**:
        ```typescript
        const userId = req.body.userId;
        db.query('UPDATE users SET email = :email WHERE id = :id', {
            replacements: { email: req.body.newEmail, id: userId }
        }).then(result => {
            res.status(200).send('Email updated successfully');
        }).catch(error => {
            res.status(500).send('Internal Server Error');
        });
        ```

### Writing SAST Rules for SQL Injection

When crafting static analysis rules to detect SQL injection vulnerabilities in TypeScript, it's essential to identify patterns suggesting unsafe handling of SQL queries. These include:

1. **Direct Concatenation of Inputs to Queries**: 
    - Detect concatenation operators (`+`, `${}`) involving variables and string literals used in SQL statements.
    - Example: Any instances of `const query = "SELECT ... " + userInput;`.

2. **Template Literals with Unsanitized Inputs**:
    - Any usage patterns like `` `SELECT ... WHERE ... = ${userInput}` ``.

3. **Vulnerable ORM or Database Calls**:
    - Identify usage of query methods (e.g., `createQueryBuilder`, `db.query`) with dynamic inputs that are not using binding or parameterized queries.

4. **Detection of Raw queries in ORM wrappers**:
    - ORM-specific raw query methods without parameterization should be flagged, e.g., `repository.query(query)` without proper parameter binding.

By implementing the above rules, it ensures the detection of typical and variant usages of SQL commands where an SQL injection vulnerability may arise, thus improving the SAST tool's accuracy.

### Citations
For more information and examples of SQL Injection vulnerabilities and prevention methods, refer to:
- OWASP guidelines on SQL Injection Prevention【4:0†source】【4:1†source】【4:2†source】【4:3†source】【4:4†source】【4:5†source】【4:6†source】【4:7†source】.
- OWASP Cheat Sheet for Injection Prevention【4:8†source】【4:9†source】【4:10†source】【4:11†source】【4:12†source】【4:13†source】【4:14†source】【4:15†source】【4:16†source】【4:17†source】【4:18†source】.