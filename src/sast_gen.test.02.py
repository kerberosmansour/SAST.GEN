import os
from datetime import datetime
from file_summarizer_assistant import FileSummarizerAssistant  # Import the class

def read_vulnerability_info(file_path):
    """Reads the first line of the markdown file to extract vulnerability info."""
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
    return first_line

def generate_semgrep_rule(vulnerability_info, context_file):
    """Generates a Semgrep SAST rule using the file summarizer assistant."""
    file_summarizer = FileSummarizerAssistant()
    
    try:
        # Construct the prompt
        question = f"""
        **Task: Generate Semgrep SAST Rules for {vulnerability_info['name']}**

        **Instructions:**

        1. **Context Review:**
           - Review the guidelines and best practices for writing Semgrep rules provided in the context file below:
           ```
           {context_file}
           ```
           - Pay particular attention to the pattern constructs, metavariable usage, and how to incorporate language- and framework-specific contexts in your rules.

        2. **Vulnerability Analysis:**
           - Analyze the following vulnerability description and its possible variations across different frameworks and coding patterns in {vulnerability_info['language']}:
           ```
           {vulnerability_info['description']}
           ```
           - Identify common coding practices and patterns that may lead to this vulnerability in {vulnerability_info['language']}, considering popular frameworks and libraries used with this language.

        3. **Semgrep Rule Creation:**
           - Generate a set of Semgrep rules using YAML format to detect {vulnerability_info['name']} across different variations.
           - Utilize Semgrep's pattern matching capabilities, including `pattern`, `pattern-either`, `pattern-inside`, and `pattern-not`, to accurately identify the vulnerability.
           - Leverage Semgrep's `metavariable-pattern` and `metavariable-regex` to handle dynamic code patterns and variations that may indicate the presence of the vulnerability.
           - Consider writing multiple rules or combining patterns with `pattern-either` to account for different variations and prevent edge cases.

        4. **Optimization for Accuracy:**
           - Ensure that the rules are designed to minimize false negatives (missed vulnerabilities) while keeping false positives (incorrectly flagged code) low.
           - Test the rules against both vulnerable and non-vulnerable code snippets to refine detection accuracy.
           - Document any known limitations or potential edge cases where the rules may not perform optimally.

        **Objective:** The goal is to create robust and precise Semgrep SAST rules that effectively detect {vulnerability_info['name']} in {vulnerability_info['language']} across different coding patterns and frameworks.
        """

        # Define the file paths
        file_paths = [context_file]
        
        # Get the generated Semgrep rule
        semgrep_rule = file_summarizer.summarize_files(file_paths, question)
        return semgrep_rule
    finally:
        # Clean up resources
        file_summarizer.cleanup()

def save_output(language, cwe, content):
    """Saves the generated content to a markdown file."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file_name = f"{language}_{cwe}_semgrep_{date_str}.md"
    output_path = os.path.join("SAST/Semgrep/Swift", output_file_name)
    
    with open(output_path, 'w') as file:
        file.write(content)
    print(f"Generated {output_file_name}")

def main():
    base_dir = "Swift"
    context_file = "KnowledgeBase/Semgrep.output.md"
    
    # Iterate over all markdown files in the directory
    for filename in os.listdir(base_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(base_dir, filename)
            
            # Step 1: Read the first line to get vulnerability info
            vulnerability_info = read_vulnerability_info(file_path)
            
            # Extract language and CWE from the filename
            language = filename.split('_')[0]
            cwe = filename.split('_')[1]
            
            # Step 2: Generate Semgrep SAST rule using the file summarizer assistant
            semgrep_rule = generate_semgrep_rule(vulnerability_info, context_file)
            
            # Step 3: Save the generated Semgrep rule to a new markdown file
            save_output(language, cwe, semgrep_rule)

if __name__ == "__main__":
    main()
