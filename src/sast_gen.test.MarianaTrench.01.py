import os
from datetime import datetime
from file_summarizer_assistant import FileSummarizerAssistant  # Import the class

def read_vulnerability_info(file_path):
    """Reads the first line of the markdown file to extract vulnerability info."""
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
    return first_line

def generate_mariana_trench_rule(vulnerability_info, context_files):
    """Generates a Mariana Trench SAST rule using the file summarizer assistant."""
    file_summarizer = FileSummarizerAssistant()
    
    try:
        # Construct the prompt
        question = f"""
        **Task: Generate Mariana Trench SAST Rules**

        **Instructions:**

        1. **Context Review:**
           - Review the guidelines and best practices for writing Mariana Trench rules provided in the context file. This file is provided as a knowledge base that can be searched through using the OpenAI Assistant API (indirectly via library).
           - Focus on the structure of `mariana_trench` rules, the use of metadata, and the appropriate constructs that are relevant to the language and framework associated with the provided vulnerability.
           - Refer to the attached Mariana Trench documentation for additional guidance on writing effective Mariana Trench rules.

        2. **Vulnerability Analysis:**
           - Analyze the provided vulnerability information, considering its potential manifestations across different frameworks and coding patterns.
           - Identify common coding practices and patterns that may lead to this vulnerability, considering popular frameworks and libraries used with the relevant language.
           - Consider potential data flow paths, control flow, and the interaction between different functions and methods that may lead to the propagation of this vulnerability.

           - Vulnerability information also provided here delmited by three backticks

          ``` {vulnerability_info} ```

        3. **Mariana Trench Rule Creation:**
           - Generate a set of Mariana Trench rules to detect this vulnerability in various scenarios.
           - Utilize Mariana Trench's capabilities to define rules that accurately identify the vulnerability, including:
               - **Taint flow tracking**: Identify how data tainted with user input or sensitive information flows through the code.
               - **Sink definitions**: Define key points in the code where the vulnerability might manifest, such as unsafe method calls or API interactions.
               - **Propagation rules**: Specify how taint might propagate through method calls, including parameter and return value mappings.
               - **Source definitions**: Define where the taint originates, such as from external inputs or user-generated content.
               - **Shim definitions**: Consider the use of shims to accurately trace data flow through abstracted or overridden methods.
           - Focus on creating rules that have **low false positives** by precisely defining conditions under which the vulnerability occurs.
           - Minimize **false negatives** by considering edge cases and less common coding patterns that could lead to the vulnerability.
           - Leverage advanced features like **taint tracking**, **data flow analysis**, and **control flow analysis** to enhance the accuracy of your rules.
           - Include **attach_to_sources**, **attach_to_sinks**, and **attach_to_propagations** where appropriate to enhance rule flexibility and applicability.

        4. **Testing and Validation:**
           - Include test cases that cover a wide range of scenarios, from typical use cases to edge cases, to validate the effectiveness of the Mariana Trench rules.
           - Suggest ways to test the Mariana Trench rules to ensure they perform effectively across different codebases and frameworks.
           - Provide guidance on how to use the Mariana Trench query console or GitHub Code Scanning to run these rules against large codebases for further validation.
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
    output_path = os.path.join("SAST/MarianaTrench", output_file_name)
    
    with open(output_path, 'w') as file:
        file.write(content)
    print(f"Generated {output_file_name}")

def main():
    base_dir = "VulnsContext/Java"
    context_files = ["KnowledgeBase/Mariana_Trench.md"]
    
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
