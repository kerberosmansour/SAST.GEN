import os
from datetime import datetime
from file_summarizer_assistant import FileSummarizerAssistant  # Import the class

def read_vulnerability_info(file_path):
    """Reads the first line of the markdown file to extract vulnerability info."""
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
    return first_line

def generate_mariana_trench_rule(vulnerability_info, context_files, web_testing_guide):
    """Generates a Mariana Trench SAST rule using the file summarizer assistant."""
    file_summarizer = FileSummarizerAssistant()
    
    try:
        # Use the extracted vulnerability info and context file to create a question
        question = f"Read how to write Mariana Trench SAST rules from the following context delimited by three backticks  ``` '{context_files}' ``` , generate a set of Mariana Trench SAST rules for the following vulnerability and its variations in the this information delimited by three backticks: ```{vulnerability_info}``` . Ensure that the rule covers variations to which this vulnerability could occur in popular frameworks for the mentioned language. The aim here is to write SAST rules with high false negative and low false postive rates. In order to also consider other variations, and the the type of inputs attackers use to exploit a vulnerability, as well as what input validation routines between sources and sinks should check for and limit false positives & false negatives review the examples of the vulnerability in the following testing guide delimited by three backticks ```{web_testing_guide}```"
        # Get the summary using the context files and the question
        summary = file_summarizer.summarize_files(context_files, question)
        return summary

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def save_output(language, cwe, content):
    """Saves the generated content to a markdown file."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file_name = f"{language}_{cwe}_mariana_trench_{date_str}.md"
    output_path = os.path.join("SAST/MarianaTrench/Java3", output_file_name)
    
    with open(output_path, 'w') as file:
        file.write(content)
    print(f"Generated {output_file_name}")

def main():
    base_dir = "VulnsContext/Java"
    context_files = ["KnowledgeBase/Mariana_Trench.md"]
    web_testing_guide = ["KnowledgeBase/WSTG.md"]
    
    # Iterate over all markdown files in the directory
    for filename in os.listdir(base_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(base_dir, filename)
            
            # Step 1: Read the first line to get vulnerability info
            vulnerability_info = read_vulnerability_info(file_path)
            
            # Extract language and CWE from the filename
            language = filename.split('_')[0]
            cwe = filename.split('_')[1]
            
            # Step 2: Generate Mariana Trench SAST rule using the file summarizer assistant
            mariana_trench = generate_mariana_trench_rule(vulnerability_info, context_files, web_testing_guide)
            
            # Step 3: Save the generated Mariana Trench rule to a new markdown file
            if mariana_trench:
                save_output(language, cwe, mariana_trench)

if __name__ == "__main__":
    main()
