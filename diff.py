import difflib
import re

def extract_modified_code(response_content):
    try:
        code_pattern = re.compile(r'```(.*?)\n(.*?)```', re.DOTALL)
        match = code_pattern.search(response_content)
        if match:
            language = match.group(1)
            code = match.group(2)
            return code
        else:
            print("Modified code block not found.")
            return None
    except Exception as e:
        print("Error extracting modified code:", e)
        return None

def compare_files(original, modified):
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)
    return difflib.unified_diff(original_lines, modified_lines, fromfile="Original", tofile="Modified")

def display_diff(diff):
    for line in diff:
        if line.startswith('+'):
            print(f"\033[92m{line}\033[0m", end="")
        elif line.startswith('-'):
            print(f"\033[91m{line}\033[0m", end="")
        else:
            print(line, end="")
