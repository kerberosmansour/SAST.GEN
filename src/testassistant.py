# Save this code in another Python file, e.g., use_file_summarizer.py

from file_summarizer_assistant import FileSummarizerAssistant  # Import the class

def main():
    file_summarizer = FileSummarizerAssistant()

    try:
        # Define the file paths and the question
        file_paths = ["/Users/sherif/Documents/OWASPDocs/Vulns/OS_Command_Injection_Defense_Cheat_Sheet.md" , "/Users/sherif/Documents/OWASPDocs/Top10/A03_2021-Injection.md"]
        question = "Read about the OWASP Injection Cheat cheat then specifically about command injection. Once you are done, think about the different varations a command injection can occurr in Java, expecially in different (popular frameworks). Explain to an author of SAST tool detection rules what an os command injection is, give many examples in Java as possible for that person to write a SAST rule to detect them"

        # Get the summary
        summary = file_summarizer.summarize_files(file_paths, question)
        print("\nSummary:\n", summary)
    finally:
        # Clean up resources
        file_summarizer.cleanup()

if __name__ == "__main__":
    main()
