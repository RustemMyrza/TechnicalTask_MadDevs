import unittest
from msg_split import split_message

class TestSplitMessage(unittest.TestCase):

    def test_no_split_needed(self):
        """Проверка, что если строка меньше max_len, она не делится."""
        html = "<p>Hello World</p>"
        max_len = 100
        result = split_message(html, max_len)
        self.assertEqual(result, ["<p>Hello World</p>"])

    def test_empty_string(self):
        """Проверка, что происходит при передаче пустой строки."""
        html = ""
        max_len = 10
        result = split_message(html, max_len)
        self.assertEqual(result, [""])


if __name__ == '__main__':
    unittest.main()
