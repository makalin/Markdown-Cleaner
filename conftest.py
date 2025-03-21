import pytest
from collections import NamedTuple

from src.markdown_cleaner import MarkdownCleaner

class Config(NamedTuple):
        fix_spacing=False,
        standardize_headers=False
        fix_lists=False
        remove_multiple_blanks=False
        extract_text=False




@pytest.fixture
def mc_fix_spacing():
    return MarkdownCleaner(fix_spacing=True)

@pytest.fixture
def mc_standardize_headers():
    return MarkdownCleaner(standardize_headers=True)

@pytest.fixture
def mc_fix_lists():
    return MarkdownCleaner(fix_lists=True)

@pytest.fixture
def mc_remove_multiple_blanks():
    return MarkdownCleaner(remove_multiple_blanks=True)

@pytest.fixture
def mc_standardize_headers_fix_lists():
    return MarkdownCleaner(standardize_headers=True,fix_lists=True)

 
