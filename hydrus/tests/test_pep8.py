"""Run PEP8 code format checker on all python files."""

import unittest
import pep8
from subprocess import Popen, PIPE


class TestCodeFormat(unittest.TestCase):
    """Test class for Code Format"""

    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""

        print("Testing PEP8 conformance... ")
        pep8style = pep8.StyleGuide(quiet=True)
        with Popen("find . -type f -name '*.py'", shell=True, stdout=PIPE) as pipe:
            py_files = [line.strip().decode('utf-8') for line in pipe.stdout]
            pipe.stdout.close()
        result = pep8style.check_files(py_files)
        err_msg = "\n\tFound {} code style errors (and warnings)."
        self.assertEqual(result.total_errors, 0,
                         err_msg.format(result.total_errors))
