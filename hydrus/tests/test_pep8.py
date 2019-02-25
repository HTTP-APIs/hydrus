"""Run PEP8 code format checker on all python files except samples directory."""

import os
import unittest
import pep8
from os.path import dirname, abspath


class Pep8Test(unittest.TestCase):

    def test_pep8(self):
        """Test method to check PEP8 compliance over the entire project."""
        print(dirname(dirname(abspath(__file__))))
        style = pep8.StyleGuide()
        style.options.max_line_length = 100  # Set this to desired maximum line length
        filenames = []
        # Set this to desired folder location
        for root, _, files in os.walk(dirname(dirname(abspath(__file__)))):
            python_files = [f for f in files if f.endswith('.py')]
            for file in python_files:
                if len(root.split('samples')) != 2:     # Ignore samples directory
                    filename = '{0}/{1}'.format(root, file)
                    filenames.append(filename)
        check = style.check_files(filenames)
        self.assertEqual(check.total_errors, 0, 'PEP8 style errors: %d' %
                         check.total_errors)

if __name__ == '__main__':
    print("Starting tests ..")
    unittest.main()
