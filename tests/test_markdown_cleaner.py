# tests/test_markdown_cleaner.py

from markdown_cleaner import MarkdownCleaner

def test_clean_file_fix_spacing():
    """Test that trailing spaces are removed when fix_spacing is enabled."""
    cleaner = MarkdownCleaner(fix_spacing=True, standardize_headers=False, fix_lists=False, remove_multiple_blanks=False, extract_text=False)
    input_content = "This is a line with trailing spaces    \nAnother line  "
    expected_output = "This is a line with trailing spaces\nAnother line\n"
    assert cleaner.clean_file(input_content) == expected_output

def test_clean_file_standardize_headers():
    """Test that headers are standardized with a space after # symbols."""
    cleaner = MarkdownCleaner(fix_spacing=False, standardize_headers=True, fix_lists=False, remove_multiple_blanks=False, extract_text=False)
    input_content = "#Header\n##NoSpace"
    expected_output = "# Header\n\n## NoSpace\n"  # Updated to expect the blank line
    assert cleaner.clean_file(input_content) == expected_output

def test_clean_file_fix_lists():
    """Test that list items have proper spacing after markers."""
    cleaner = MarkdownCleaner(fix_spacing=False, standardize_headers=False, fix_lists=True, remove_multiple_blanks=False, extract_text=False)
    input_content = "-  Item1\n*Item2\n1.Item3"
    expected_output = "- Item1\n* Item2\n1. Item3\n"
    assert cleaner.clean_file(input_content) == expected_output

def test_clean_file_remove_multiple_blanks():
    """Test that multiple blank lines are reduced to one."""
    cleaner = MarkdownCleaner(fix_spacing=False, standardize_headers=False, fix_lists=False, remove_multiple_blanks=True, extract_text=False)
    input_content = "Line 1\n\n\nLine 2"
    expected_output = "Line 1\n\nLine 2\n"
    assert cleaner.clean_file(input_content) == expected_output

def test_clean_file_add_space_before_headers_and_lists():
    """Test that a blank line is added before headers and lists if needed."""
    cleaner = MarkdownCleaner(fix_spacing=False, standardize_headers=True, fix_lists=True, remove_multiple_blanks=False, extract_text=False)
    input_content = "Some text\n# Header\nSome other text\n- Item"
    expected_output = "Some text\n\n# Header\nSome other text\n\n- Item\n"
    assert cleaner.clean_file(input_content) == expected_output

def test_extract_plain_text():
    """Test that plain text extraction removes Markdown formatting."""
    cleaner = MarkdownCleaner(extract_text=True)
    input_content = "# Header\nThis is *bold* and **bolder**.\n- Item 1\n- Item 2\n[Link](url)"
    expected_output = "Header\nThis is bold and bolder.\n• Item 1\n• Item 2\nLink\n"
    assert cleaner.clean_file(input_content) == expected_output