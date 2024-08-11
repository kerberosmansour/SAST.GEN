"""
this script creates a basic test C# file for every rule in the dir /Csharp
Once we have done this, we can use the Semgrep test framework to add basic tests to check for the formatting / indentation of the semgrep rules created.
The semgrep test framework works as defined here: https://semgrep.dev/docs/writing-rules/testing-rules

TL;DR: Given a rule named rules/rule-1.yaml, you can create rules/rule-1.<language_of_rule> & then run semgrep --test rules/
The goal is to use the findings here to optimize the rule creation prompt to not make the same mistakes

"""
import os

# Path to the folder containing the YAML files
yaml_folder = "./Csharp"
# Path to the folder where the .cs files will be saved
cs_folder = "./Csharp"

# Contents for the .cs files- some dummy contents 
cs_content = """using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Data;
using System.Data.OleDb;
using System.Data.SqlClient;
using System.Data.Odbc;

namespace MvcMovie.Controllers;

public class HomeCtrl : Controller
{

    private readonly string _connectionString;

    public HomeCtrl(YourDbContext context)
    {
        _connectionString = configuration.GetConnectionString("YourConnectionStringName");
    }

    public IActionResult Test1(string filename)
    {
        if (string.IsNullOrEmpty(filename))
        {
            throw new ArgumentNullException("error");
        }
        string filepath = Path.Combine("/FILESHARE/images", filename);
        return File.ReadAllBytes(filepath);
    }
"""

# Get the list of all YAML files in the folder
yaml_files = [f for f in os.listdir(yaml_folder) if f.endswith('.yaml')]

# Create .cs files with the same names as the YAML files
for yaml_file in yaml_files:
    # Remove the .yaml extension and add .cs extension
    cs_filename = os.path.splitext(yaml_file)[0] + ".cs"
    cs_filepath = os.path.join(cs_folder, cs_filename)

    # Write the content to the .cs file
    with open(cs_filepath, 'w') as cs_file:
        cs_file.write(cs_content)

print(f"Created {len(yaml_files)} .cs files.")
