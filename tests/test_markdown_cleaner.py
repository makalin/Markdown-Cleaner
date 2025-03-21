# tests/test_markdown_cleaner.py


def test_clean_file_fix_spacing(mc_fix_spacing):
    """Test that trailing spaces are removed when fix_spacing is enabled."""
    cleaner = mc_fix_spacing
    input_content = "This is a line with trailing spaces    \nAnother line  "
    expected_output = "This is a line with trailing spaces\nAnother line\n"
    assert cleaner.clean_file(input_content) == expected_output

def test_clean_file_standardize_headers(mc_standardize_headers):
    """Test that headers are standardized with a space after # symbols."""
    cleaner = mc_standardize_headers
    input_content = "#Header\n##NoSpace"
    expected_output = "# Header\n\n## NoSpace\n"  # Updated to expect the blank line
    assert cleaner.clean_file(input_content) == expected_output

def test_clean_file_fix_lists(mc_fix_lists):
    """Test that list items have proper spacing after markers."""
    cleaner = mc_fix_lists
    input_content = "-  Item1\n*Item2\n1.Item3"
    expected_output = "- Item1\n* Item2\n1. Item3\n"
    assert cleaner.clean_file(input_content) == expected_output

def test_clean_file_remove_multiple_blanks(mc_remove_multiple_blanks):
    """Test that multiple blank lines are reduced to one."""
    cleaner = mc_remove_multiple_blanks)
    input_content = "Line 1\n\n\nLine 2"
    expected_output = "Line 1\n\nLine 2\n"
    assert cleaner.clean_file(input_content) == expected_output

def test_clean_file_add_space_before_headers_and_lists(mc_standardize_headers_fix_lists):
    """Test that a blank line is added before headers and lists if needed."""
    cleaner = mc_standardize_headers_fix_lists
    input_content = "Some text\n# Header\nSome other text\n- Item"
    expected_output = "Some text\n\n# Header\nSome other text\n\n- Item\n"
    assert cleaner.clean_file(input_content) == expected_output

def test_extract_plain_text(mc_fix_spacing):
    """Test that plain text extraction removes Markdown formatting."""
    cleaner = mc_fix_spacing
    input_content = "# Header\nThis is *bold* and **bolder**.\n- Item 1\n- Item 2\n[Link](url)"
    expected_output = "Header\nThis is bold and bolder.\n• Item 1\n• Item 2\nLink\n"
    assert cleaner.clean_file(input_content) == expected_output