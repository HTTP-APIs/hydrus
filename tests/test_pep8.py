"""Run PEP8 code format checker on all python files except samples directory."""

import os
from os.path import abspath, dirname

import pep8


def test_pep8():
    """Test method to check PEP8 compliance over the entire project."""
    file_structure = dirname(dirname(abspath(__file__)))
    print(f"Testing for PEP8 compliance of python files in {file_structure}")
    style = pep8.StyleGuide()
    style.options.max_line_length = 100  # Set this to desired maximum line length
    filenames = []
    # Set this to desired folder location
    for root, _, files in os.walk(file_structure):
        python_files = [f for f in files if f.endswith('.py') and "examples" not in root]
        for file in python_files:
            if len(root.split('samples')) != 2:     # Ignore samples directory
                filename = f'{root}/{file}'
                filenames.append(filename)
    check = style.check_files(filenames)
    assert check.total_errors == 0, f'PEP8 style errors: check.total_errors'
