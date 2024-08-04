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
        # Use the extracted vulnerability info and context file to create a question
        question = f"Read about application security risks and issues as well as proactive security controls security developers can build three backticks  ``` '{context_file}' ``` , generate a set secure defaults and remediation code as well as secure library recommendations for the following vulnerability and its variations in the this information delimited by three backticks: ```{vulnerability_info}``` . Ensure that the detailed technical recomendations covers variations to which this vulnerability could occur in popular frameworks for the mentioned language. The aim here is to write secure defaults, that have a great developer experience and a high false negative and low false postive rates."
        
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
    output_path = os.path.join("SecureDefaults/Java", output_file_name)
    
    with open(output_path, 'w') as file:
        file.write(content)
    print(f"Generated {output_file_name}")

def main():
    base_dir = "VulnsContext/Java"
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
            
            # Step 2: Generate Secure Defaults using the file summarizer assistant
            semgrep_rule = generate_semgrep_rule(vulnerability_info, context_file)
            
            # Step 3: Save the Secure Defaults to a new markdown file
            save_output(language, cwe, semgrep_rule)

if __name__ == "__main__":
    main()
