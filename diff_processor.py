import difflib

# At the top of diff_processor.py
known_placeholders = {
    "// Other functions remain the same",
    "/* Rest of the code remains the same */",
    # Add more placeholders as needed.
}

def generate_diff(original_text, modified_text):
    """
    Generates a unified diff between two texts.
    """
    diff = difflib.unified_diff(
        original_text.splitlines(keepends=True),
        modified_text.splitlines(keepends=True),
        fromfile='original',
        tofile='modified',
    )
    return list(diff)

def bundle_changes_old(diff):
    """
    Processes the diff to identify and bundle changes, handling special placeholders
    that indicate unchanged code. The function categorizes each line in the diff as an
    addition, deletion, or unchanged and bundles consecutive changes.
    """
    changes = []  # List to hold all structured changes
    buffer = []  # Temporary buffer to hold consecutive changes of the same type
    
    def flush_buffer(change_type):
        """Helper function to flush the buffer into the changes list."""
        if buffer:
            changes.append({'type': change_type, 'content': buffer.copy()})
            buffer.clear()

    for line in diff:
        if line.startswith('---') or line.startswith('+++'):
            continue  # Skip diff metadata lines
        
        content = line[1:].rstrip('\n')  # Extract the content without the diff symbol and newline
        if line.startswith('+'):
            if content in known_placeholders:
                # If current addition is a known placeholder, discard previous deletions
                if buffer and changes[-1]['type'] == 'deletion':
                    changes.pop()  # Remove the last change if it was a deletion
                    flush_buffer('unchanged')  # Flush as unchanged if buffer has content
                continue  # Skip further processing for this line
            flush_buffer('deletion')  # Flush any accumulated deletions
            buffer.append(content)
            flush_buffer('addition')  # Directly flush additions as they're not batched
        elif line.startswith('-'):
            flush_buffer('addition')  # Flush any accumulated additions
            buffer.append(content)  # Accumulate deletions for potential batching
        else:
            # Handle unchanged lines by flushing the buffer as the previous type if not empty
            flush_buffer('deletion' if buffer else 'unchanged')
            changes.append({'type': 'unchanged', 'content': [content]})

    # Flush any remaining changes in the buffer after processing all lines
    flush_buffer('deletion' if buffer else 'unchanged')
    
    return changes


def process_code_diff(original_code, modified_code):
    """
    Processes the difference between original and modified code,
    and returns a structured representation of changes.
    """
    diff = generate_diff(original_code, modified_code)
    changes = bundle_changes(diff)
    return changes

def parse_hunk_header(header_line):
    """
    Parses a hunk header line to extract line number information.
    Example input: '@ -5,8 +5,7 @@'
    """
    parts = header_line.split()
    original_range = parts[1].lstrip('-')
    modified_range = parts[2].lstrip('+')
    return {
        'original_range': original_range,
        'modified_range': modified_range,
        'changes': []  # Placeholder for the changes within this hunk
    }

def bundle_changes(diff):
    """
    Processes the diff to identify changes, including parsing hunk headers
    to structure results according to hunk sections.
    """
    hunks = []
    current_hunk = None

    for line in diff:
        if line.startswith('---') or line.startswith('+++'):
            continue  # Skip diff metadata lines

        if line.startswith('@'):
            # Start a new hunk
            if current_hunk is not None:
                # Save the previous hunk if it exists
                hunks.append(current_hunk)
            current_hunk = parse_hunk_header(line)
            continue

        # Ensure there is a current hunk to process changes
        if current_hunk is None:
            continue  # Skip lines until the first hunk header is found

        # Process changes within the current hunk
        line_content = line[1:].rstrip('\n')  # Extract content without diff symbol
        line_type = 'unchanged'
        if line.startswith('+'):
            line_type = 'addition'
        elif line.startswith('-'):
            line_type = 'deletion'
        
        # Append the change to the current hunk
        current_hunk['changes'].append({
            'type': line_type,
            'content': line_content
        })

    # Append the last hunk if any
    if current_hunk is not None:
        hunks.append(current_hunk)

    return hunks
