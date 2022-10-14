"""
Test suite for the Daedalus lexer
"""
import os
import unittest

from gothic_lexer import DaedalusLexer
from pygments import lexers

import general_tokens
import misc_tokens

TESTS_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
GENERAL_D_PATH = os.path.join(TESTS_DIR_PATH, "general.d")
MISC_D_PATH = os.path.join(TESTS_DIR_PATH, "misc.d")


class DaedalusTest(unittest.TestCase):
    """
    Daedalus TestCase Class
    """

    def test_get_lexer_by_name(self) -> None:
        """
        Test that both `dae` and `pbd` alias names get the correct lexer
        """
        self.assertTrue(isinstance(lexers.get_lexer_by_name("dae"), DaedalusLexer))
        self.assertTrue(isinstance(lexers.get_lexer_by_name("pbd"), DaedalusLexer))

    def test_general_tokens(self) -> None:
        """
        Test that the lexer tokenizes the `general.d` file correctly
        """
        with open(GENERAL_D_PATH, encoding="utf8") as file:
            source: str = file.read()

        tokens = DaedalusLexer().get_tokens(source)
        correct = iter(general_tokens.CORRECT_TOKENS)

        for token in tokens:
            self.assertEqual(token, next(correct))

    def test_misc_tokens(self) -> None:
        """
        Test that the lexer tokenizes the `misc.d` file correctly
        The whitespace tokens are ignored
        """
        with open(MISC_D_PATH, encoding="utf8") as file:
            source: str = file.read()

        tokens = DaedalusLexer().get_tokens(source)
        correct = iter(misc_tokens.CORRECT_TOKENS_NO_WHITESPACE)

        for token in tokens:
            if "Whitespace" not in str(token):
                self.assertEqual(token, next(correct))


if __name__ == "__main__":
    unittest.main()
