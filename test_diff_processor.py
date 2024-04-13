import difflib
from diff_processor import process_code_diff

def color_addition(text):
    """Returns the text colored in green for additions."""
    return f"\033[92m+{text}\033[0m"

def color_deletion(text):
    """Returns the text colored in red for deletions."""
    return f"\033[91m-{text}\033[0m"

def color_unchanged(text):
    """Returns the text prefixed with a space for unchanged lines."""
    return f" {text}"

def load_file_content(filepath):
    """
    Reads the content of a file and returns it as a string.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def color_line(line):
    """Returns the line colored based on its type."""
    if line.startswith('+'):
        return f"\033[92m{line}\033[0m"  # Green for additions
    elif line.startswith('-'):
        return f"\033[91m{line}\033[0m"  # Red for deletions
    elif line.startswith('@'):
        return f"\033[94m{line}\033[0m"  # Blue for hunk headers
    else:
        return line  # Default color for unchanged/context lines

def generate_and_color_diff(original_content, modified_content):
    """Generates a diff, colors each line according to its type, and includes line numbers."""
    diff = difflib.unified_diff(
        original_content.splitlines(keepends=True),
        modified_content.splitlines(keepends=True),
        fromfile='original',
        tofile='modified',
    )
    
    # Initialize line counters
    orig_line_num = 0
    mod_line_num = 0

    for line in diff:
        # Process hunk headers to reset the line counters appropriately
        if line.startswith('@@'):
            # Extract line numbers from the hunk header
            _, orig_range, mod_range, _ = line.split(' ', 3)
            orig_line_num = int(orig_range.split(',')[0][1:])  # Skip the leading '-'
            mod_line_num = int(mod_range.split(',')[0][1:])  # Skip the leading '+'
            # Print the hunk header with color but without line numbers
            print(color_line(line), end='')
            continue

        # Adjust line numbers and print lines with color and line numbers
        line_num_display = f"{orig_line_num if line.startswith(('-', ' ')) else ' '}:{mod_line_num if line.startswith(('+', ' ')) else ' '}"
        
        if line.startswith('+'):
            mod_line_num += 1
        elif line.startswith('-'):
            orig_line_num += 1
        elif line.startswith(' '):
            orig_line_num += 1
            mod_line_num += 1
        
        print(f"{color_line(line_num_display + ' ' + line)}", end='')

def main():
    # Hardcode the paths to the original and modified text files
    original_file_path = 'test/original.txt'
    modified_file_path = 'test/modified.txt'

    # Load the content of the original and modified files
    original_content = load_file_content(original_file_path)
    modified_content = load_file_content(modified_file_path)

    generate_and_color_diff(original_content, modified_content)

if __name__ == "__main__":
    main()
