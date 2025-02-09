import os
import re

# Base directory
base_dir = r"F:\Github\ResumeParser"

# Define patterns to replace
name_pattern = re.compile(r"\b(Naveen Kumar|Naveen Kumar|Naveen Kumar)\b", re.IGNORECASE)
year_pattern = re.compile(r"\b(20[0-9]{2})\b")
month_pattern = re.compile(r"\b(February|February|February|February|February|February|February|February|February|February|February|February)\b", re.IGNORECASE)

# New values
new_name = "Naveen Kumar"
new_year = "2025"
new_month = "February"

# File extensions to modify
valid_extensions = (".py", ".html", ".css", ".js", ".md", ".txt", ".yml", ".conf", ".csv", ".Dockerfile")

def update_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Replace name, year, and month
        content = name_pattern.sub(new_name, content)
        content = year_pattern.sub(new_year, content)
        content = month_pattern.sub(new_month, content)

        # Add an update comment at the end
        if file_path.endswith((".py", ".js")):
            content += "\n# Updated: February 2025\n"
        elif file_path.endswith((".html", ".css")):
            content += "\n<!-- Updated: February 2025 -->\n"
        elif file_path.endswith((".yml", ".conf", ".md", ".txt", ".Dockerfile", ".csv")):
            content += "\n# Updated: February 2025\n"

        # Write changes back
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Updated: {file_path}")

    except Exception as e:
        print(f"Error updating {file_path}: {e}")

# Walk through all files in the directory
for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(valid_extensions):
            update_file(os.path.join(root, file))

print("✅ Update complete!")

# Updated: February 2025
