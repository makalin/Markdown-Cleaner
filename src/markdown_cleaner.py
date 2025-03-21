#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional


class MarkdownCleaner:
    def __init__(
        self,
        fix_spacing: bool = True,
        standardize_headers: bool = True,
        fix_lists: bool = True,
        remove_multiple_blanks: bool = True,
        extract_text: bool = False,
    ):
        self.fix_spacing = fix_spacing
        self.standardize_headers = standardize_headers
        self.fix_lists = fix_lists
        self.remove_multiple_blanks = remove_multiple_blanks
        self.extract_text = extract_text

    def clean_file(self, content: str) -> str:
        """Clean and format markdown content."""
        if self.extract_text:
            return self._extract_plain_text(content)

        lines = content.split("\n")
        cleaned_lines = []
        prev_line = ""
        in_list = False  # Track if we're in a list

        i = 0
        while i < len(lines):
            line = lines[i]

            # Handle basic cleaning
            if self.fix_spacing:
                line = line.rstrip()

            # Standardize headers
            if self.standardize_headers and line.lstrip().startswith("#"):
                line = self._fix_header(line)

            # Fix lists
            is_list_item = False
            if self.fix_lists and (
                line.lstrip().startswith(("- ", "* ", "-", "*"))
                or re.match(r"^\s*\d+\.", line)
            ):
                line = self._fix_list_item(line)
                is_list_item = True

            # Handle blank lines
            if self.remove_multiple_blanks:
                if line.strip() == "" and prev_line.strip() == "":
                    i += 1
                    continue

            # Add space before headers and lists if needed, but not between consecutive list items
            if (
                i > 0
                and line.lstrip().startswith(("#", "-", "*"))
                or re.match(r"^\s*\d+\.", line)
            ):
                if cleaned_lines and cleaned_lines[-1].strip() != "":
                    # Don't add a blank line if we're in a list and the current line is a list item
                    if not (in_list and is_list_item):
                        cleaned_lines.append("")

            cleaned_lines.append(line)
            prev_line = line
            in_list = is_list_item  # Update list state
            i += 1

        # Ensure single newline at end of file
        while cleaned_lines and cleaned_lines[-1].strip() == "":
            cleaned_lines.pop()
        cleaned_lines.append("")

        return "\n".join(cleaned_lines)

    def _extract_plain_text(self, content: str) -> str:
        """Extract plain text from markdown content."""
        # Normalize newlines
        content = content.replace("\r\n", "\n").replace("\r", "\n")

        # Remove code blocks
        content = re.sub(r"```[^`]*```", "", content, flags=re.DOTALL)
        content = re.sub(r"`[^`]*`", "", content)

        # Remove images
        content = re.sub(r"!\[(.*?)\]\(.*?\)", r"\1", content)

        # Remove headers
        content = re.sub(r"^#+\s*", "", content, flags=re.MULTILINE)

        # Remove emphasis markers
        content = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", content)

        # Remove HTML tags
        content = re.sub(r"<[^>]+>", "", content)

        # Convert list markers to plain text
        content = re.sub(r"^\s*[-*+]\s+", "• ", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*\d+\.\s+", "", content, flags=re.MULTILINE)

        # Handle blockquotes
        content = re.sub(r"^\s*>\s*", "", content, flags=re.MULTILINE)

        # Collapse multiple newlines
        content = re.sub(r"\n\s*\n", "\n\n", content)

        # Remove horizontal rules
        content = re.sub(r"^\s*[-*_]{3,}\s*$", "", content, flags=re.MULTILINE)

        # Remove links but keep link text
        content = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", content)

        return content.strip() + "\n"

    def _fix_header(self, line: str) -> str:
        """Ensure headers have a space after # symbols."""
        match = re.match(r"^(#+)(.*)$", line.lstrip())
        if match:
            hashes, content = match.groups()
            return f"{hashes} {content.lstrip()}"
        return line

    def _fix_list_item(self, line: str) -> str:
        """Fix spacing in list items."""
        indent = len(line) - len(line.lstrip())
        content = line.lstrip()

        # Handle numbered lists
        if re.match(r"^\d+\.", content):
            number_part = re.match(r"^\d+\.", content).group()
            content = content[len(number_part) :].lstrip()
            return " " * indent + number_part + " " + content

        # Handle bullet lists (with or without space after marker)
        if content.startswith(("-", "*")):
            marker = content[0]
            content = content[1:].lstrip()  # Remove marker and strip leading space
            return " " * indent + marker + " " + content

        return line


def process_file(
    file_path: Path, cleaner: MarkdownCleaner, in_place: bool
) -> Optional[str]:
    """Process a single markdown file."""
    try:
        content = file_path.read_text()
        cleaned = cleaner.clean_file(content)

        if in_place:
            file_path.write_text(cleaned)
            return None
        return cleaned
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Clean and format Markdown files")
    parser.add_argument("files", nargs="+", type=Path, help="Markdown files to process")
    parser.add_argument(
        "--in-place", "-i", action="store_true", help="Modify files in place"
    )
    parser.add_argument(
        "--no-spacing",
        action="store_false",
        dest="fix_spacing",
        help="Disable fixing spacing",
    )
    parser.add_argument(
        "--no-headers",
        action="store_false",
        dest="standardize_headers",
        help="Disable header standardization",
    )
    parser.add_argument(
        "--no-lists", action="store_false", dest="fix_lists", help="Disable list fixing"
    )
    parser.add_argument(
        "--keep-blanks",
        action="store_false",
        dest="remove_multiple_blanks",
        help="Keep multiple blank lines",
    )
    parser.add_argument(
        "--extract-text",
        "-e",
        action="store_true",
        help="Extract plain text, removing all markdown formatting",
    )

    args = parser.parse_args()

    cleaner = MarkdownCleaner(
        fix_spacing=args.fix_spacing,
        standardize_headers=args.standardize_headers,
        fix_lists=args.fix_lists,
        remove_multiple_blanks=args.remove_multiple_blanks,
        extract_text=args.extract_text,
    )

    for file_path in args.files:
        if not file_path.exists():
            print(f"File not found: {file_path}", file=sys.stderr)
            continue

        result = process_file(file_path, cleaner, args.in_place)
        if result is not None:
            print(result)


if __name__ == "__main__":
    main()
