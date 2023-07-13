#MB
import argparse

def process_line(line, in_custom_item, description_id):
    if line.strip() == "<custom_item>":
        in_custom_item = True
        return f"    {line.strip()}\n", in_custom_item, description_id
    elif line.strip() == "</custom_item>":
        in_custom_item = False
        return f"    {line.strip()}\n", in_custom_item, description_id
    elif in_custom_item:
        if ":" in line and " " in line.split(":")[0]:  # Section header
            if "description" in line:
                # Extract identifier for next comment
                description_id = line.split('"')[1].strip()
            return f"      {line.strip()}\n", in_custom_item, description_id
        elif "for example:" not in line:
            return f"        {line.strip()}\n", in_custom_item, description_id
    return line, in_custom_item, description_id

def format_file(input_filepath):
    # Define the output file path
    output_filepath = input_filepath.replace(".audit", "_formatted.audit")

    # First, read all lines into a list
    with open(input_filepath, "r") as infile:
        lines = infile.readlines()

    # Then, process the lines
    with open(output_filepath, "w") as outfile:
        in_custom_item = False
        description_id = ""
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip() == "<custom_item>":
                # Look ahead to find the description line
                j = i + 1
                while j < len(lines) and lines[j].strip() != "</custom_item>":
                    if "description" in lines[j]:
                        description_id = lines[j].split('"')[1].strip()
                        break
                    j += 1
                # Write comment for <custom_item> tag
                outfile.write(f"# {description_id}\n")
            processed_line, in_custom_item, _ = process_line(line, in_custom_item, description_id)
            outfile.write(processed_line)
            i += 1

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Format a file.")

    # Add an argument for the file path
    parser.add_argument("filepath", help="The path to the file to be formatted.")

    # Parse the arguments
    args = parser.parse_args()

    # Apply the format_file function to the provided file
    format_file(args.filepath)

# Entry point
if __name__ == "__main__":
    main()

