import tkinter as tk
from tkinter import ttk
import re

def transform_items():
    input_text = input_box.get("1.0", tk.END)
    custom_items = re.findall(r'<custom_item>.*?</custom_item>', input_text, re.DOTALL)
    
    if len(custom_items) < 2:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "Error: Please provide at least two custom_items.")
        return

    # Extract description from the first custom_item
    description = re.search(r'description\s*:\s*"(.*?)"', custom_items[0], re.DOTALL)
    description = description.group(1) if description else ""

    # Output skeleton for logic
    output = f"# {description}\n"
    output += "  <if>\n"
    output += '    <condition type:"AND">\n'

    # Split input text into lines
    lines = input_text.split('\n')
    in_custom_item = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            output += line + "\n"
        elif stripped.startswith('<custom_item>'):
            in_custom_item = True
            output += "        " + stripped + "\n"  
        elif stripped.endswith('</custom_item>'):
            in_custom_item = False
            output += "        " + stripped + "\n"  
        elif in_custom_item:
            output += "          " + stripped + "\n"  

    output += "    </condition>\n"
    output += "    <then>\n"
    output += '      <report type:"PASSED">\n'

    # Extract fields from the first custom_item
    fields = ['description', 'info', 'solution', 'reference', 'see_also']
    for field in fields:
        value = re.search(rf'{field}\s*:\s*"(.*?)"', custom_items[0], re.DOTALL)
        if value:
            output += f"        {field:<12}: \"{value.group(1)}\"\n"

    output += "        show_output : YES\n"
    output += "      </report>\n"
    output += "    </then>\n"
    output += "  </if>"

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output)

def clear_boxes():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)

# Create the main window
root = tk.Tk()
root.title("Custom Item Transformer")
root.geometry("1600x900")  # Increased window size

# Create a frame for the input and output boxes
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

#  input text box
input_label = ttk.Label(frame, text="Input Custom Items:")
input_label.grid(row=0, column=0, pady=5)
input_box = tk.Text(frame, height=40, width=100)  # Increased text box size
input_box.grid(row=1, column=0, padx=(0, 10))

#  output text box
output_label = ttk.Label(frame, text="Transformed Output:")
output_label.grid(row=0, column=1, pady=5)
output_box = tk.Text(frame, height=40, width=100)  # Increased text box size
output_box.grid(row=1, column=1, padx=(10, 0))

# frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

#  transform button
transform_button = ttk.Button(button_frame, text="Transform", command=transform_items)
transform_button.pack(side=tk.LEFT, padx=5)

#  clear button
clear_button = ttk.Button(button_frame, text="Clear", command=clear_boxes)
clear_button.pack(side=tk.LEFT, padx=5)

#  expand with window
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(1, weight=1)

# Start the GUI  loop
root.mainloop()
