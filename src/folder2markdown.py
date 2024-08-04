import os

# Path to the root directory containing all your folders
root_dir = "/Users/sherif/Documents/GitHub/wstg/document"

# The output file where all markdown files will be appended
output_file = "WSTG.md"

# List to store the paths of markdown files in ascending order
md_files = []

# Walk through the directory in a sorted order
for dirpath, dirnames, filenames in sorted(os.walk(root_dir)):
    # Sort the directories to ensure they are processed in ascending order
    dirnames.sort()
    # Find all markdown files in the current directory
    for filename in sorted(filenames):
        if filename.endswith(".md"):
            md_files.append(os.path.join(dirpath, filename))

# Write the contents of each markdown file to the output file
with open(output_file, "w", encoding="utf-8") as outfile:
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as infile:
            outfile.write(infile.read())
            outfile.write("\n\n")  # Add some space between each file's content

print(f"All markdown files have been combined into {output_file}")
