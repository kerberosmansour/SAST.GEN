HereHere is a set of Semgrep SAST rules for detecting `Improper Restriction of XML External Entity Reference (CWE-611)` in JavaScript. These rules will cover various uses of popular frameworks such as `xml2js`, `xmldom`, and `libxmljs`.

### Rule 1 - Detecting usage of `xml2js` library without disabling external entity resolution
```yaml
rules:
  - id: xml2js-external-entity-disabled
    languages: [javascript]
    message: Use `xml2js` without disabling external entity resolution can lead to XXE vulnerability.
    severity: ERROR
    patterns:
      - pattern: |
            new xml2js.Parser(...)
      - pattern-inside: |
            new xml2js.Parser({ ... })
      - metavariable-comparison:
          metavariable: $CONFIG
          comparison: $CONFIG['explicitRoot'] == false
  - id: xml2js-external-entity-not-set
    languages: [javascript]
    message: Ensure `xml2js` external entity resolution is disabled to prevent XXE vulnerability.
    severity: WARNING
    pattern: |
        new xml2js.Parser({...})
    pattern-not-inside: |
        'explicitRoot': false
```

### Rule 2 - Detecting XML parsing with `xmldom` without disabling external entity resolution
```yaml
rules:
  - id: xmldom-external-entity
    languages: [javascript]
    message: Ensure `xmldom` parser does not resolve external entities to prevent XXE vulnerability.
    severity: ERROR
    pattern: |
        new xmldom.DOMParser().parseFromString(...)
    pattern-not-inside: |
        'disableExternalEntities': true
```

### Rule 3 - Detecting usage of `libxmljs` without disabling external entity resolution
```yaml
rules:
  - id: libxmljs-external-entity
    languages: [javascript]
    message: Ensure external entity loading is disabled when using `libxmljs` to prevent XXE vulnerability.
    severity: ERROR
    pattern: |
        libxmljs.parseXml(...).setDtdLoad(false).setDtdAttr(false)
```

Each of these rules can be saved in a YAML file and run using the `semgrep` tool as follows:

```sh
semgrep --config your_rules.yaml path_to_your_js_project/
```

For more details on writing custom Semgrep rules, you can refer to the guidelines provided in the `Semgrep.output.md` file, such as configuration, syntax, and using the semgrep playground   .