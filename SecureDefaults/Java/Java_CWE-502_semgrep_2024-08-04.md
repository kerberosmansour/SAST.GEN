## Deserialization of Untrusted Data (CWE-502) in Java

Deserialization of untrusted data is a critical vulnerability where an application processes untrusted data without proper validation. This can lead to arbitrary code execution, denial-of-service, and other malicious activities. Common frameworks where this vulnerability occurs include Java's native serialization, Apache Commons-Collections, and other serialization libraries.

## Secure Defaults and Remediation Code

### Preventing Serialization Attacks

Java's native serialization mechanism can be replaced with safer alternatives like JSON or XML processing libraries (e.g., Jackson, Gson) which provide better control over data deserialization.

#### JSON Example with Jackson

A secure default implementation using Jackson would involve:
1. Disabling polymorphic deserialization.
2. Enforcing strict typing.

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.jsontype.BasicPolymorphicTypeValidator;
import com.fasterxml.jackson.databind.jsontype.PolymorphicTypeValidator;

public class SecureSerialization {

    public static ObjectMapper createSecureObjectMapper() {
        PolymorphicTypeValidator ptv = BasicPolymorphicTypeValidator.builder()
            .allowIfSubType("com.yourcompany.")
            .build();
        ObjectMapper mapper = new ObjectMapper();
        mapper.activateDefaultTyping(ptv, ObjectMapper.DefaultTyping.NON_FINAL);
        return mapper;
    }

    public static void main(String[] args) {
        ObjectMapper secureMapper = createSecureObjectMapper();
        // Use secureMapper for serialization and deserialization
    }

}
```

#### XML Example with Jackson

```java
import com.fasterxml.jackson.dataformat.xml.XmlMapper;
import com.fasterxml.jackson.databind.DeserializationFeature;

public class SecureXmlSerialization {

    public static XmlMapper createSecureXmlMapper() {
        XmlMapper xmlMapper = new XmlMapper();
        xmlMapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
        return xmlMapper;
    }

    public static void main(String[] args) {
        XmlMapper secureXmlMapper = createSecureXmlMapper();
        // Use secureXmlMapper for XML (de)serialization
    }
}
```

### Using Whitelisting Techniques

Enforcing a whitelist of classes allowed for deserialization helps mitigate risks:

#### Java Serialization Filtering

Available from Java 9 onwards:

```java
import java.io.*;

public class SecureObjectInputStream extends ObjectInputStream {
    public SecureObjectInputStream(InputStream in) throws IOException {
        super(in);
        this.setObjectInputFilter(info -> {
            Class<?> serialClass = info.serialClass();
            if (serialClass != null && serialClass.getName().startsWith("com.yourcompany.")) {
                return ObjectInputFilter.Status.ALLOWED;
            }
            return ObjectInputFilter.Status.REJECTED;
        });
    }
}
```

## Secure Library Recommendations

1. **Jackson**:
   - JSON processing with extensive support for security features.
   - Configurable to disable dangerous features and enforce strict deserialization policies.

2. **Google Gson**:
   - Lightweight JSON parser with strict type handling.
   - Can be configured to permit only safe types.

3. **Hjson**:
   - Human-readable JSON alternative that also emphasizes secure deserialization.

4. **XStream**:
   - XML serialization library with secure processing features.
   - Supports explicit type whitelisting and can be secured against arbitrary code execution.

### Best Practices using Semgrep

Semgrep can automate the detection of insecure use patterns and enforce secure coding practices. Examples include detecting insecure deserialization of data or ensuring proper authorization checks in Java Spring Controllers.

#### Example Semgrep Rule to Detect Dangerous Deserialization in Java

```yaml
rules:
  - id: detect-unsafe-deserialization
    patterns:
      - pattern: |
          new ObjectInputStream($STREAM$);
      - pattern-not-inside: |
          public class SecureObjectInputStream
    message: "Detected use of ObjectInputStream. Ensure this is securely handled and only used for safe deserialization."
    languages: [java]
    severity: WARNING
```

### Applying Security Best Practices in Spring Framework

Custom Semgrep rule example for ensuring authorization annotations are in place for sensitive actions:

```yaml
rules:
  - id: spring-unauthenticated-route
    patterns:
      - pattern-inside: |
          @RestController
          class $CONTROLLER{ 
            ...
          }          
      - pattern-inside: |
          @$MAPPING($ROUTE)
          $RET $METHOD(...) {...}          
      - metavariable-regex:
          metavariable: $MAPPING
          regex: (GetMapping|PostMapping|DeleteMapping|PutMapping|PatchMapping)    
      - pattern-not: |
          @PreAuthorize(...)
          $METHOD(...){...}          
      - focus-metavariable:
          - $ROUTE
    message: >
      The route $ROUTE is exposed to unauthenticated users. Please verify
      this is expected behaviour, otherwise add the proper authentication/authorization checks.      
    languages:
      - java
    severity: WARNING
```

## Conclusion

By adopting secure defaults, using safe libraries, and employing tools like Semgrep for detecting insecure patterns, developers can significantly enhance the security posture of applications against deserialization vulnerabilities in Java. Leveraging whitelisting, secure serialization libraries, and enforcing best practices are essential components of a comprehensive security strategy against deserialization of untrusted data.

For more detailed Semgrep examples and configuration, refer to the provided documentation and examples on Semgrep's official resources【4:0†source】【4:1†source】【4:5†source】【4:7†source】【4:9†source】.