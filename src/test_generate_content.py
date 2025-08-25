import unittest
from generate_content import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        actual_title = extract_title("# This is a title")
        self.assertEqual(actual_title, "This is a title")

    def test_eq_multiple_titles(self):
        actual_title = extract_title(
            """
# This is a title

# This is another title that should be ignored
"""
        )
        self.assertEqual(actual_title, "This is a title")

    def test_eq_other_types(self):
        actual_title = extract_title(
            """
# Title

Text.

- unordered
- list
"""
        )
        self.assertEqual(actual_title, "Title")

    def test_no_title(self):
        try:
            extract_title(
                """
No title here.
"""
            )
            self.fail("An exception should have been raised!")
        except Exception as e:
            pass

if __name__ == "__main__":
    unittest.main()