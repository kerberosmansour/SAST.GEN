from file_summarizer_assistant import FileSummarizerAssistant  # Import the class
from datetime import datetime

def generate_cwe_question(cwe_name, language):
    return f"""
**Task: Provide Examples and Guidance for Writing SAST Rules to Detect {cwe_name} in {language}**

**Instructions:**

1. **Review and Understand {cwe_name}:**
   - Read the attached content to fully understand {cwe_name}, focusing on how it manifests in applications written in {language}.

2. **Identify and Explain Variations:**
   - Consider different ways {cwe_name} can appear in {language}, especially within popular frameworks.
   - Provide detailed examples of {cwe_name} in {language}, showcasing variations in different contexts, such as different frameworks, coding patterns, or application layers.

3. **Guide SAST Rule Creation:**
   - Explain {cwe_name} in a way that would help an author of SAST tool detection rules understand the vulnerability and how it can be exploited.
   - Include as many code examples as possible in {language}, highlighting different ways the vulnerability can occur.

4. **Focus on Accurate Detection:**
   - Emphasize the importance of creating SAST rules that effectively minimize false negatives (undetected vulnerabilities) while also reducing false positives (incorrectly flagged code).
   - Discuss common pitfalls and edge cases to consider when writing detection rules for {cwe_name}.

**Objective:** The goal is to equip the SAST tool author with comprehensive examples and insights to write precise and effective detection rules for {cwe_name} in {language}.
"""

def main():
    file_summarizer = FileSummarizerAssistant()
    
    languages = ["PHP"]
    cwes = {
        "CWE-917": "Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')",
        "CWE-502": "Deserialization of Untrusted Data",
        "CWE-089": "Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')",
        "CWE-078": "Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')",
        "CWE-094": "Improper Control of Generation of Code ('Code Injection')",
        "CWE-843": "Access of Resource Using Incompatible Type ('Type Confusion')",
        "CWE-434": "Unrestricted Upload of File with Dangerous Type",
        "CWE-077": "Improper Neutralization of Special Elements used in a Command ('Command Injection')",
        "CWE-427": "Uncontrolled Search Path Element",
        "CWE-611": "Improper Restriction of XML External Entity Reference",
        "CWE-352": "Cross-Site Request Forgery (CSRF)",
        "CWE-190": "Integer Overflow or Wraparound",
        "CWE-022": "Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')",
        "CWE-918": "Server-Side Request Forgery (SSRF)",
        "CWE-059": "Improper Link Resolution Before File Access ('Link Following')",
        "CWE-295": "Improper Certificate Validation",
        "CWE-400": "Uncontrolled Resource Consumption",
        "CWE-319": "Cleartext Transmission of Sensitive Information",
        "CWE-770": "Allocation of Resources Without Limits or Throttling",
        "CWE-079": "Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')",
    }

    try:
        for language in languages:
            for cwe_id, cwe_name in cwes.items():
                question = generate_cwe_question(cwe_name, language)
                
                # Static file paths
                file_paths = [
                    "KnowledgeBase/combined_top10_markdown.md",
                    "KnowledgeBase/combined_vuln_markdown.md"
                ]
                
                # Get the summary
                summary = file_summarizer.summarize_files(file_paths, question)
                
                # Define the output markdown file name
                date_str = datetime.now().strftime("%Y-%m-%d")
                output_file = f"{language}_{cwe_id}_{date_str}.md"
                
                # Write the summary to a markdown file
                with open(output_file, 'w') as f:
                    f.write(f"# {cwe_name} ({cwe_id}) in {language}\n\n")
                    f.write(summary)
                    
                print(f"Generated {output_file}")
                
    finally:
        # Clean up resources
        file_summarizer.cleanup()

if __name__ == "__main__":
    main()
