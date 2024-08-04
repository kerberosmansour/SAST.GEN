import os
import re

# Function to extract YAML blocks from a markdown file
def extract_yaml_blocks(markdown_text):
    yaml_blocks = re.findall(r'```yaml(.*?)```', markdown_text, re.DOTALL)
    return yaml_blocks

# Function to save YAML blocks to separate files
def save_yaml_blocks(yaml_blocks, markdown_filename, output_dir, subfolder_path=""):
    base_name = os.path.splitext(markdown_filename)[0]
    subfolder_output_dir = os.path.join(output_dir, subfolder_path)
    
    # Create the subfolder in the output directory if it doesn't exist
    os.makedirs(subfolder_output_dir, exist_ok=True)
    
    for i, block in enumerate(yaml_blocks, start=1):
        yaml_filename = f"{base_name}_yaml_{i}.yaml"
        yaml_filepath = os.path.join(subfolder_output_dir, yaml_filename)
        with open(yaml_filepath, 'w') as yaml_file:
            yaml_file.write(block.strip())
        print(f"Saved {yaml_filepath}")

# Function to process each markdown file in the directory tree
def process_markdown_files(root_dir, output_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Determine the relative path of the current directory to the root directory
        subfolder_path = os.path.relpath(dirpath, root_dir)
        
        for filename in filenames:
            if filename.endswith(".md"):
                markdown_filepath = os.path.join(dirpath, filename)
                with open(markdown_filepath, 'r') as md_file:
                    markdown_text = md_file.read()
                    yaml_blocks = extract_yaml_blocks(markdown_text)
                    if yaml_blocks:
                        save_yaml_blocks(yaml_blocks, filename, output_dir, subfolder_path)

# Main function
if __name__ == "__main__":
    # Define the root directory containing markdown files
    root_directory = "SAST"
    
    # Define the output directory to save extracted YAML files
    output_directory = "SemgrepYAML"
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)
    
    # Process markdown files and extract YAML blocks
    process_markdown_files(root_directory, output_directory)
