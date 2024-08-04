BasedBased on your context, here is a Semgrep SAST rule for detecting deserialization of untrusted data (CWE-502) in JavaScript. This rule will cover popular JavaScript frameworks like Node.js, Express, and general JavaScript code that uses JSON or other serialization frameworks.

```yaml
rules:
  - id: deserialization-of-untrusted-data
    patterns:
      - pattern: |
          var $VAR = JSON.parse($DATA);
      - pattern: |
          const $VAR = JSON.parse($DATA);
      - pattern: |
          let $VAR = JSON.parse($DATA);
      - pattern: |
          var $VAR = eval($DATA);
      - pattern: |
          const $VAR = eval($DATA);
      - pattern: |
          let $VAR = eval($DATA);
      - pattern: |
          var $VAR = deserialize($DATA);
      - pattern: |
          const $VAR = deserialize($DATA);
      - pattern: |
          let $VAR = deserialize($DATA);
    message: Avoid deserialization of untrusted data to prevent RCE (CWE-502)
    languages: [javascript]
    severity: ERROR
    metadata:
      cwe: "CWE-502"
      confidence: High
      likelihood: High
      impact: High
      subcategory: vuln

```

To understand the construction and parameters of this rule, you can refer to the references on writing effective Semgrep rules, combining patterns, and setting metadata【4:0†source】  . These guides provide detailed insights to ensure your rules are accurate and provide useful feedback for identified vulnerabilities in your code.

If you need further customization or additional patterns to match other serialization libraries or methods specific to different frameworks or contexts, let me know and I can help you revise the rule accordingly!