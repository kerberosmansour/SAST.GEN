#### Secure Defaults for Unrestricted File Upload (CWE-434) in Java

### Secure Defaults

1. **Filename Validation**:
   - Ensure the uploaded files have safe filenames.
   - Allowlisting specific characters and removing dangerous ones.

2. **File Type Validation**:
   - Strict validation of file types using both file extension and inspecting file headers.
   - Maintain a list of allowed MIME types.

3. **File Upload Location**:
   - Save uploaded files in a directory outside the webroot to prevent direct access.

4. **File Size Limits**:
   - Impose a maximum file size limit to avoid potential denial of service attacks.

### Remediation Code

#### Filename Validation
```java
import java.nio.file.Paths;
import java.nio.file.InvalidPathException;

public boolean isValidFilename(String filename) {
    try {
        Paths.get(filename);
        return filename.matches("[a-zA-Z0-9._-]+");
    } catch (InvalidPathException e) {
        return false;
    }
}
```

#### File Type Validation
Using Apache Tika for MIME type detection:
```java
import org.apache.tika.Tika;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public boolean isAllowedMimeType(String filePath) {
    Tika tika = new Tika();
    try {
        String mimeType = tika.detect(new File(filePath));
        List<String> allowedMimeTypes = Arrays.asList("image/jpeg", "image/png", "application/pdf");
        return allowedMimeTypes.contains(mimeType);
    } catch (IOException e) {
        return false;
    }
}
```

#### File Upload Location and Size Check in Spring Boot
```java
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.List;

@RestController
public class FileUploadController {

    private static final List<String> allowedMimeTypes = Arrays.asList("image/jpeg", "image/png", "application/pdf");
    private static final long MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
    private static final String UPLOAD_DIR = "/safe/upload/directory/";

    @PostMapping("/upload")
    public String uploadFile(@RequestParam("file") MultipartFile file) throws IOException {
        String filename = file.getOriginalFilename();

        // Validate the filename
        if (!isValidFilename(filename)) {
            return "Invalid filename";
        }

        // Check file size
        if (file.getSize() > MAX_FILE_SIZE) {
            return "File too large";
        }

        // Validate MIME type
        Tika tika = new Tika();
        String mimeType = tika.detect(file.getInputStream());
        if (!allowedMimeTypes.contains(mimeType)) {
            return "Invalid file type";
        }

        // Save the file
        Path destinationPath = Paths.get(UPLOAD_DIR, filename).normalize();
        Files.copy(file.getInputStream(), destinationPath, StandardCopyOption.REPLACE_EXISTING);

        return "File uploaded successfully";
    }

    private boolean isValidFilename(String filename) {
        try {
            Paths.get(filename);
            return filename.matches("[a-zA-Z0-9._-]+");
        } catch (InvalidPathException e) {
            return false;
        }
    }
    
}
```

### Secure Library Recommendations

1. **Apache Tika**:
   - Use Apache Tika to detect MIME types of files.
   - Provides robust and reliable file type detection using file content inspection.
   - [Apache Tika](https://tika.apache.org/)

2. **Commons IO**:
   - Use Commons IO libraries for handling and validating file uploads.
   - Provides utilities for file interactions that are secure and efficient.
   - [Apache Commons IO](https://commons.apache.org/proper/commons-io/)

3. **Spring Security**:
   - Ensure proper authentication and authorization checks before uploading files.
   - [Spring Security](https://spring.io/projects/spring-security)

### Variations in Popular Frameworks

#### Spring Framework

- **Spring Boot File Upload**:
  - Use MultipartFile for handling file uploads securely.
  - Validate file before processing as shown in the remediation code above.

- **JSP/Servlets**:
  - Use Servlet 3.0's `@MultipartConfig` for file upload handling.
  - Implement similar validation for files in servlets.

By applying the secure defaults and using recommended libraries, we can build robust upload functionalities in Java applications that limit both false positives and negatives.

For completeness and additional implementation insights, leverage content from resources like Semgrep as they demonstrate pattern matching and taint tracking which can further secure application code【4:0†source】    .