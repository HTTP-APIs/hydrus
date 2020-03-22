"""Run PEP8 code format checker on all python files except samples directory."""

import os
import unittest
import pep8
from os.path import dirname, abspath


class Pep8Test(unittest.TestCase):

    def test_pep8(self):
        """Test method to check PEP8 compliance over the entire project."""
        self.file_structure = dirname(dirname(abspath(__file__)))
        print(f"Testing for PEP8 compliance of python files in {self.file_structure}")
        style = pep8.StyleGuide()
        style.options.max_line_length = 100  # Set this to desired maximum line length
        filenames = []
        # Set this to desired folder location
        for root, _, files in os.walk(self.file_structure):
            python_files = [f for f in files if f.endswith(
                '.py') and "examples" not in root]
            for file in python_files:
                if len(root.split('samples')) != 2:     # Ignore samples directory
                    filename = f'{root}/{file}'
                    filenames.append(filename)
        check = style.check_files(filenames)
        self.assertEqual(check.total_errors, 0, f'PEP8 style errors: {check.total_errors:d}')


if __name__ == '__main__':
    print("Starting tests ..")
    unittest.main()
