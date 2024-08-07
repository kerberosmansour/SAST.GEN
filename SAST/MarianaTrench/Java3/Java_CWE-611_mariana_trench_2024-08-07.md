###### Writing SAST Rules for Improper Restriction of XML External Entity Reference (CWE-611) in Java Using Mariana Trench

#### Overview
To write efficient and accurate SAST rules for identifying CWE-611 vulnerabilities (Improper Restriction of XML External Entity Reference) in Java using Mariana Trench, we'll follow the steps outlined for rule creation. These involve defining source and sink methods, creating models, and writing rules that capture the flow between these sources and sinks.

#### Essential Steps for Rule Creation
1. **Identify Sources**: Methods that parse or handle untrusted XML input using certain XML parsing libraries.
2. **Identify Sinks**: Methods or configurations that may result in unsafe XML parsing if improperly configured.
3. **Write the Model Generators**: JSON models specifying sources and sinks.
4. **Define the Rules**: JSON rules that describe the flow from source to sink.

#### Sources and Sinks Identification
**Sources**:
Untrusted or external XML input handled by classes such as:
- `javax.xml.parsers.DocumentBuilder`
- `javax.xml.parsers.SAXParser`
- `javax.xml.parsers.SAXParserFactory`
- `javax.xml.stream.XMLInputFactory`
- `javax.xml.transform.TransformerFactory`
- `org.xml.sax.XMLReader`

**Sinks**:
Configuration methods that can enable unsafe XML processing features such as:
- `setFeature("http://javax.xml.XMLConstants/feature/secure-processing", false)`
- `setFeature("http://apache.org/xml/features/disallow-doctype-decl", false)`
- `setFeature("http://xml.org/sax/features/external-general-entities", true)`
- `setFeature("http://xml.org/sax/features/external-parameter-entities", true)`

#### Model Generators
Create model generator JSON files to detect sources (methods handling XML input) and sinks (methods configuring XML parsing).

**Example Model Generator for Sources**:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "newDocumentBuilder"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "javax.xml.parsers.DocumentBuilderFactory"}}
      ],
      "model": {"sources": [{"kind": "XmlInput", "port": "Return"}]}
    },
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "newSAXParser"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "javax.xml.parsers.SAXParserFactory"}}
      ],
      "model": {"sources": [{"kind": "XmlInput", "port": "Return"}]}
    }
  ]
}
```

**Example Model Generator for Sinks**:
```json
{
  "model_generators": [
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "setFeature"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "javax.xml.parsers.DocumentBuilder"}}
      ],
      "model": {"sinks": [{"kind": "XmlConfig", "port": "Argument(1)"}]}
    },
    {
      "find": "methods",
      "where": [
        {"constraint": "name", "pattern": "setProperty"},
        {"constraint": "parent", "inner": {"constraint": "name", "pattern": "javax.xml.stream.XMLInputFactory"}}
      ],
      "model": {"sinks": [{"kind": "XmlConfig", "port": "Argument(1)"}]}
    }
  ]
}
```

#### Rule Definition
Define the rules to capture the flow from `XmlInput` sources to `XmlConfig` sinks.

**Rule Example**:
```json
{
  "name": "Improper Restriction of XML External Entity Reference (CWE-611)",
  "code": 611,
  "description": "Untrusted XML input flowing into unsafe XML configuration",
  "sources": ["XmlInput"],
  "sinks": ["XmlConfig"]
}
```

#### Summary
1. **Identify Key Methods**: Analyze the methods typically used for XML parsing and configuration in Java.
2. **Create Source and Sink Models**: Use model generators to define sources (methods returning XML parsers) and sinks (methods configuring XML parsers).
3. **Define Rules**: Create a rule matching these sources to sinks to capture potential CWE-611 vulnerabilities.

By carefully identifying sources and sinks and writing precise rules, this approach increases detection accuracy and reduces both false negatives and false positives    .