BasedBased on the provided context about writing Semgrep SAST rules and understanding various patterns, here's a set of Semgrep SAST rules to detect the vulnerability "Deserialization of Untrusted Data (CWE-502)" in Swift. This rule covers various frameworks like Foundation and other custom deserialization methods.

### Rule: Deserialization of Untrusted Data in Swift

```yaml
rules:
  - id: swift-deserialization-of-untrusted-data
    languages: [swift]
    message: "Potential deserialization of untrusted data"
    severity: ERROR
    patterns:
      # Match the use of JSONSerialization with potentially unsafe data
      - pattern: |
          let $OBJ = try JSONSerialization.jsonObject(with: Data($UNSAFE), options: .mutableContainers)
      - pattern: |
          let $OBJ = try JSONSerialization.jsonObject(with: $UNSAFE, options: .mutableContainers)
      # Match the use of PropertyListSerialization with potentially unsafe data
      - pattern: |
          let $OBJ = try PropertyListSerialization.propertyList(from: Data($UNSAFE), format: nil)
      - pattern: |
          let $OBJ = try PropertyListSerialization.propertyList(from: $UNSAFE, format: nil)
      # Match the use of NSKeyedUnarchiver with potentially unsafe data
      - pattern: |
          let $OBJ = try NSKeyedUnarchiver.unarchivedObject(ofClass: $CLASS, from: $UNSAFE)
      - pattern: |
          let $OBJ = try NSKeyedUnarchiver.unarchivedObject(ofClasses: $CLASSES, from: $UNSAFE)
      # Custom deserialization via NSCoder
      - pattern: |
          let $DECODER = $CLASS(forReadingWith: Data($UNSAFE))
      - pattern: |
          let $DECODER = $CLASS(forReadingWith: $UNSAFE)

    metadata:
      cwe: 502
      documentation: "https://cwe.mitre.org/data/definitions/502.html"
      examples:
        - |
          import Foundation

          struct User: Codable {
              var name: String
              var email: String
          }

          let jsonData = Data()
          let user = try JSONSerialization.jsonObject(with: jsonData, options: .mutableContainers) # ruleid: swift-deserialization-of-untrusted-data
        - |
          import Foundation

          struct User: Codable {
              var name: String
              var email: String
          }

          let plistData = Data()
          let user = try PropertyListSerialization.propertyList(from: plistData, format: nil) # ruleid: swift-deserialization-of-untrusted-data
        - |
          import Foundation

          let keyedUnarchiver = try NSKeyedUnarchiver.unarchivedObject(ofClass: MyClass.self, from: Data()) # ruleid: swift-deserialization-of-untrusted-data
```

### Explanation

1. **Targeted Functions:**
   - `JSONSerialization.jsonObject(with: Data(_), options: .mutableContainers)`
   - `PropertyListSerialization.propertyList(from: Data(_), format: nil)`
   - `NSKeyedUnarchiver.unarchivedObject(ofClass: _, from: Data())`
   - Custom deserialization using `NSCoder`.

2. **Patterns:**
   - `$UNSAFE` represents the untrusted data which is being deserialized.
   - Patterns are used to match key functions and methods that are used in deserialization.

3. **Frameworks:**
   - Foundation framework handling for JSON, property lists, and keyed archivers.
   - This should also accommodate custom deserialization patterns commonly used in Swift.

4. **False Positives and Negatives:**
   - The goal is to minimize false negatives by covering common deserialization patterns.
   - False positives are controlled by specifically focusing on deserialization functions.

Applying these rules will help in identifying potential issues related to deserialization of untrusted data in Swift projects.

All the information utilized to generate these rules is extracted and
interpreted from the given context on writing Semgrep rules and the
provided document content    .