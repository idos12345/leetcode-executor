import unittest
import base64
from unittest.mock import patch, MagicMock, mock_open
from string import Template
from leetcode_execution_api.bl.image_factory.image_generator import ImageGenerator


class TestImageGenerator(unittest.TestCase):

    def setUp(self):
        self.mock_template = Template("Solution: $solution\nTests: $tests")
        self.mock_dockerfile = "FROM python:3.12\nCMD [\"python\", \"TestSolution.py\"]"
        self.image_generator = ImageGenerator(self.mock_template, self.mock_dockerfile, "py", "\n")

    def test_indent_string(self):
        text = "line1\nline2"
        indented_text = self.image_generator.indent_string(text, spaces=2)
        self.assertEqual(indented_text, "  line1\n  line2")

    def test_inject_code_to_test_script(self):
        solution_code = "def add(a, b):\n    return a + b"
        tests_code_list = ["assert add(2, 3) == 5", "assert add(5, 5) == 10"]
        injected_script = self.image_generator.inject_code_to_test_script(solution_code, tests_code_list)

        self.assertIn("Solution:", injected_script)
        self.assertIn("Tests:", injected_script)
        self.assertIn("assert add(2, 3) == 5", injected_script)



if __name__ == "__main__":
    unittest.main()