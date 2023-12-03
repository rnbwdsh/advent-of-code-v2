import os
import re
import subprocess

directory_path = '.'  # Replace with the path to your directory

# Regex pattern to capture the required part of the filename
pattern = re.compile(r"(day\d+).ipynb")

for filename in os.listdir(directory_path):
    match = pattern.match(filename)
    if match:
        print(match)
        new_filename = match.group(1) + '.py'
        full_path_to_file = os.path.join(directory_path, filename)
        full_path_to_new_file = os.path.join(directory_path, new_filename)

        # Convert the notebook to a Python file
        subprocess.run(["jupyter", "nbconvert", "--to", "script", full_path_to_file])
