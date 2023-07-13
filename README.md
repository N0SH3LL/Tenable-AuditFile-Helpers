# Formatter

The Formatter script is a Python tool designed to make working with Tenable .audit files easier and more convenient. It allows you to format these files, making them more readable and facilitating the isolation of specific sections for editing purposes. The script takes a command line input specifying the filename, and it outputs the formatted version with the "_formatted" suffix appended to the original filename.

## Features

- Formats Tenable .audit files for improved readability
- Supports folding entire sections in Visual Studio Code
- Preserves the original file by creating a formatted copy
- Works with command line inputs for easy execution

## Requirements

- Python 3.x

## Installation

1. Clone the repository or download the `formatter.py` file directly.
2. Ensure you have Python 3.x installed on your system.

## Usage

To format a Tenable .audit file, follow these steps:

1. Open a command prompt or terminal.
2. Navigate to the directory where the `formatter.py` script is located.
3. Run the script using the following command:

   ```shell
   python formatter.py <filename>
   ```

   Replace `<filename>` with the name of the .audit file you want to format.

4. The formatted version of the file will be created with the suffix "_formatted" appended to the original filename.


## Folding Sections in Visual Studio Code

The Formatter script specifically aims to make it easier to fold entire sections in Visual Studio Code. Once you have the formatted .audit file opened in Visual Studio Code, you can use the folding feature to isolate specific parts for better focus.

To fold a section, use one of the following methods:

- Place the cursor at the beginning of a section and press `Ctrl + Shift + [` (`Cmd + Shift + [` on macOS).
- Right-click on a section and select "Fold" from the context menu.
- Click on the small triangle icon on the left side of a section.
- 
This will collapse the section, allowing you to work with other parts of the file without distraction.

Or, alternatively, press `Ctrl + K, Ctrl + 0`. This should fold all sections, and allow you to unfold the controls you wish to work on. 



## Contributing

Contributions to the Formatter script are welcome. If you encounter any issues, have suggestions for improvements, or would like to add new features, please open an issue or submit a pull request on the GitHub repository.

