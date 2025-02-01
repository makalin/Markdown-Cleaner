# Markdown Cleaner

A Python utility for cleaning and standardizing Markdown files. This tool helps maintain consistent formatting across your Markdown documents by fixing common formatting issues and standardizing the layout.

## Features

- Standardizes header formatting (ensures proper spacing after # symbols)
- Fixes list item indentation and spacing (both bullet points and numbered lists)
- Removes multiple consecutive blank lines
- Maintains consistent spacing around headers and list items
- Extracts plain text from Markdown files (optional)
- Supports batch processing of multiple files
- Can modify files in-place or output to stdout

## Installation

Clone this repository and ensure you have Python 3.x installed:

```bash
git clone https://github.com/makalin/Markdown-Cleaner.git
cd Markdown-Cleaner
chmod +x Markdown-Cleaner.py
```

## Usage

Basic usage:

```bash
./markdown-cleaner.py file1.md file2.md
```

Process multiple files and modify them in-place:

```bash
./markdown-cleaner.py -i *.md
```

Extract plain text, removing all Markdown formatting:

```bash
./markdown-cleaner.py --extract-text document.md
```

### Command Line Options

- `--in-place`, `-i`: Modify files in place instead of outputting to stdout
- `--no-spacing`: Disable fixing of spacing issues
- `--no-headers`: Disable header standardization
- `--no-lists`: Disable list formatting fixes
- `--keep-blanks`: Keep multiple consecutive blank lines
- `--extract-text`, `-e`: Extract plain text, removing all Markdown formatting

## Examples

### Before Cleaning

```markdown
#Header with no space
* Inconsistent list marker
-Another list item with no space
  ##Nested header with no space

Multiple

blank lines
```

### After Cleaning

```markdown
# Header with proper space
* Consistent list marker
- Another list item with proper space
  ## Nested header with proper space

Single blank lines between sections
```

## Features in Detail

### Header Standardization
- Ensures exactly one space after # symbols
- Adds blank lines before headers
- Maintains header levels (# through ######)

### List Formatting
- Standardizes list markers (- or *)
- Fixes spacing after list markers
- Maintains proper indentation for nested lists
- Handles both bullet points and numbered lists

### Plain Text Extraction
When using `--extract-text`, the tool:
- Removes all Markdown formatting symbols
- Strips code blocks
- Converts links to plain text
- Removes HTML tags
- Maintains readable text structure

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
