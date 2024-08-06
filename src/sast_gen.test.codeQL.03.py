import os
from datetime import datetime
from file_summarizer_assistant import FileSummarizerAssistant  # Import the class

def read_vulnerability_info(file_path):
    """Reads the first line of the markdown file to extract vulnerability info."""
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
    return first_line

def generate_codeql_rule(vulnerability_info, context_files):
    """Generates a CodeQL SAST rule using the file summarizer assistant."""
    file_summarizer = FileSummarizerAssistant()
    
    try:
        # Construct the prompt
        question = f"""
        **Task: Generate CodeQL SAST Rules for {vulnerability_info}**

        **Instructions:**

        1. **Context Review:**
           - Review the guidelines and best practices for writing CodeQL rules provided in the context file. This file is provided as a knowledge base that can be searched through using the OpenAI Assistant API (indirectly via library).
           - Focus on the structure of `.ql` files, the use of metadata, and the appropriate QL constructs that are relevant to the {vulnerability_info} language.
           - Refer to the attached CodeQL documentation for additional guidance on writing effective CodeQL rules.

        2. **Vulnerability Analysis:**
           - Analyze the following vulnerability description and its potential manifestations across different frameworks and coding patterns in {vulnerability_info}:
           \"""
           {vulnerability_info}
           \"""
           - Identify common coding practices and patterns that may lead to this vulnerability in {vulnerability_info}, taking into account popular frameworks and libraries used with this language.

        3. **CodeQL Rule Creation:**
           - Generate a set of CodeQL rules using the QL language to detect {vulnerability_info} in various scenarios.
           - Utilize CodeQL's capabilities to define queries that accurately identify the vulnerability.
           - Focus on creating rules that have **low false positives** by precisely defining conditions under which the vulnerability occurs. 
           - Minimize **false negatives** by considering edge cases and less common coding patterns that could lead to the vulnerability.
           - Use CodeQL's advanced features, such as **data flow analysis**, **control flow analysis**, and **taint tracking**, to enhance the accuracy of your rules.
           - Leverage **predicate functions** and **configuration options** to make the rules more flexible and adaptable to different codebases.

        4. **Testing and Validation:**
           - Include test cases that cover a wide range of scenarios, from typical use cases to edge cases, to validate the effectiveness of the CodeQL rules.
           - Suggest ways to test the CodeQL rules to ensure they perform effectively across different codebases and frameworks.
           - Provide guidance on how to use the CodeQL query console or GitHub Code Scanning to run these rules against large codebases for further validation.
        """
        # Get the summary using the context files and the question
        summary = file_summarizer.summarize_files(context_files, question)
        return summary

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_output(language, cwe, content):
    """Saves the generated content to a markdown file."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file_name = f"{language}_{cwe}_codeql_{date_str}.md"
    output_path = os.path.join("SAST/CodeQL/Csharp", output_file_name)
    
    with open(output_path, 'w') as file:
        file.write(content)
    print(f"Generated {output_file_name}")

def main():
    base_dir = "VulnsContext/Csharp"
    context_files = ["KnowledgeBase/CodeQL.md"]
    
    # Iterate over all markdown files in the directory
    for filename in os.listdir(base_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(base_dir, filename)
            
            # Step 1: Read the first line to get vulnerability info
            vulnerability_info = read_vulnerability_info(file_path)
            
            # Extract language and CWE from the filename
            language = filename.split('_')[0]
            cwe = filename.split('_')[1]
            
            # Step 2: Generate CodeQL SAST rule using the file summarizer assistant
            codeql_rule = generate_codeql_rule(vulnerability_info, context_files)
            
            # Step 3: Save the generated CodeQL rule to a new markdown file
            if codeql_rule:
                save_output(language, cwe, codeql_rule)

if __name__ == "__main__":
    main()
