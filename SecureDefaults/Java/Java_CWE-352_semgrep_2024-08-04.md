ToTo address Cross-Site Request Forgery (CSRF) (CWE-352) in Java, focusing on secure defaults, remediation code, and secure library recommendations, we need to consider the different frameworks and libraries available in the Java ecosystem, such as Spring and Java Enterprise Edition (Java EE).

### Secure Defaults for CSRF Protection in Java

#### 1. **Spring Framework**

Spring Framework provides built-in CSRF protection. Ensure the following default configurations are enabled:

- **Enable CSRF Protection:** By default, Spring Security enables CSRF protection. You need to ensure it’s configured correctly.

```java
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .csrf().disable() // This should be removed in prod
            .authorizeRequests()
            .antMatchers("/", "/home").permitAll()
            .anyRequest().authenticated();
    }
}
```

**Recommendation:** Do not disable CSRF protection unless absolutely necessary (e.g., for stateless REST APIs).

- **Using CSRF Tokens in Forms:**

Ensure that every form on your website includes a CSRF token:
```html
<form action="/submit" method="post">
    <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>
    <!-- other form fields -->
    <button type="submit">Submit</button>
</form>
```

- **AJAX Requests:**

Include the CSRF token in your JavaScript AJAX request headers:

```javascript
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrfToken = getCookie('XSRF-TOKEN');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader('X-XSRF-TOKEN', csrfToken);
    }
});
```

#### 2. **Java EE (Jakarta EE)**

Java EE typically does not provide built-in CSRF protection in older versions. You may need to implement it manually.

- **Filter-Based CSRF Protection:**

Create a CSRF filter that checks for tokens:

```java
@WebFilter("/*")
public class CSRFFilter implements Filter {

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        if ("POST".equalsIgnoreCase(req.getMethod())) {
            String csrfToken = req.getParameter("csrfToken");
            HttpSession session = req.getSession(false);
            if (session == null || !csrfToken.equals(session.getAttribute("csrfToken"))) {
                res.sendError(HttpServletResponse.SC_FORBIDDEN, "CSRF protection");
                return;
            }
        }
        chain.doFilter(request, response);
    }
}
```

- **Generate CSRF Tokens:**

Add a CSRF token to the session and forms:

```java
public class CSRFTokenUtil {
    public static String generateToken() {
        return UUID.randomUUID().toString();
    }

    public static String getTokenForSession(HttpSession session) {
        String token = (String) session.getAttribute("csrfToken");
        if (token == null) {
            token = generateToken();
            session.setAttribute("csrfToken", token);
        }
        return token;
    }
}
```

### Secure Libraries to Use

1. **OWASP Java CSRFGuard:** It's a popular library that provides substantial CSRF protections.

   - **Usage:**
   
   ```xml
   <!-- In pom.xml -->
   <dependency>
       <groupId>org.owasp.esapi</groupId>
       <artifactId>esapi</artifactId>
       <version>2.2.3.1</version>
   </dependency>
   ```

   - **Configuration:**

   ```xml
   <filter>
       <filter-name>CSRFGuard</filter-name>
       <filter-class>org.owasp.csrfguard.CsrfGuardServletContextListener</filter-class>
   </filter>
   <filter-mapping>
       <filter-name>CSRFGuard</filter-name>
       <url-pattern>/*</url-pattern>
   </filter-mapping>
   ```

2. **Spring Security:**

   - **Spring Security already includes built-in CSRF protection and should be utilized directly.

### Conclusion

By leveraging these secure defaults, remediation codes, and secure libraries, developers can significantly mitigate the risk of CSRF attacks in Java applications. Each approach should be tailored to integrate seamlessly with the development workflow, ensuring a high development experience with minimal false negatives and false positives. Custom rules for detecting missing CSRF protection can also be enforced using static analysis tools like Semgrep to ensure continuous security validation【4:0†source】  .