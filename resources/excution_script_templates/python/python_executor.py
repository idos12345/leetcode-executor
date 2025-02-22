from string import Template

python_template = Template("""
import unittest

class Solution:
    $solution

class DynamicTest(unittest.TestCase):
    $tests

if __name__ == "__main__":
    unittest.main()

""")

