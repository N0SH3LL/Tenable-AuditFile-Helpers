import re
import sys
import os

def format_audit_file(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Split into lines
    lines = content.split('\n')

    formatted_lines = []
    indent_level = 0
    max_key_length = 0
    multi_line_field = None
    current_item = []
    current_description = ""
    processing_started = False

    # First pass: determine the max length
    for line in lines:
        if not processing_started:
            if line.strip().startswith('<check_type:'):
                processing_started = True
        if processing_started:
            match = re.match(r'^\s*(\w+)\s*:', line)
            if match:
                max_key_length = max(max_key_length, len(match.group(1)))

    # Reset processing_started for second pass
    processing_started = False

    # Second pass: format the lines
    for line in lines:
        if not processing_started:
            formatted_lines.append(line)  # Keep original comment lines before <check_type:>
            if line.strip().startswith('<check_type:'):
                processing_started = True
            continue

        stripped = line.strip()

        # Handle multi-line fields
        if multi_line_field:
            if current_item:
                current_item[-1] += ' ' + stripped
            else:
                formatted_lines[-1] += ' ' + stripped
            if stripped.endswith('"'):
                multi_line_field = None
            continue

        # Check for opening tags of custom_item or report
        if stripped.startswith('<custom_item>') or stripped.startswith('<report'):
            if current_item:
                if current_description:
                    formatted_lines.append(f"{'  ' * indent_level}# {current_description}")
                formatted_lines.extend(current_item)
            current_item = ['  ' * indent_level + '  ' + stripped]
            indent_level += 1
            current_description = ""
        # Check for closing tags of custom_item or report
        elif stripped in ['</custom_item>', '</report>']:
            indent_level -= 1
            current_item.append('  ' * indent_level + '  ' + stripped)
            if current_description:
                formatted_lines.append(f"{'  ' * indent_level}# {current_description}")
            formatted_lines.extend(current_item)
            current_item = []
            current_description = ""
        # Check for other opening tags
        elif stripped.startswith('<') and not stripped.startswith('</') and not stripped.endswith('/>'):
            formatted_lines.append('  ' * indent_level + stripped)
            indent_level += 1
        # Check for other closing tags
        elif stripped.startswith('</'):
            indent_level -= 1
            formatted_lines.append('  ' * indent_level + stripped)
        # Check for self-closing tags
        elif stripped.startswith('<') and stripped.endswith('/>'):
            formatted_lines.append('  ' * indent_level + stripped)
        # Format key-value pairs
        elif ':' in stripped:
            key, value = stripped.split(':', 1)
            key = key.strip()
            value = value.strip()
            if key == 'description':
                current_description = value.strip('"')
            if current_item:
                field_indent = '  ' * (indent_level + 1)
            else:
                field_indent = '  ' * indent_level + '  '
            formatted_line = f"{field_indent}{key.ljust(max_key_length)} : {value}"
            if current_item:
                current_item.append(formatted_line)
            else:
                formatted_lines.append(formatted_line)
            if (key in ['info', 'solution']) and value.startswith('"') and not value.endswith('"'):
                multi_line_field = key
        # Other lines
        else:
            if current_item:
                current_item.append('  ' * (indent_level + 1) + stripped)
            else:
                formatted_lines.append('  ' * indent_level + stripped)

    # Write the formatted content to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(formatted_lines))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + "_formatted.audit"

    format_audit_file(input_file, output_file)
    print(f"Formatted file saved as {output_file}")
