import unittest
from src.domain.parser.lexer import Lexer, LexerError, Token, TokenType

WORD = TokenType.WORD
NUMBER = TokenType.NUMBER
COMMA = TokenType.COMMA
PERIOD = TokenType.PERIOD
SEMICOLON = TokenType.SEMICOLON
COLON = TokenType.COLON
ASTERISK = TokenType.ASTERISK
OPEN_GROUP = TokenType.OPEN_GROUP
CLOSE_GROUP = TokenType.CLOSE_GROUP
NEWLINE = TokenType.NEWLINE
STITCH = TokenType.STITCH
EOI_TOKEN = Token(TokenType.EOI, None)

class TestPrimitiveLexing(unittest.TestCase):
    def test_can_identify_primitive_letters(self):
        lexer = Lexer("k p tog ssk")
        
        expected = [
            Token(WORD, "k"), Token(WORD, "p"), Token(WORD, "tog"), Token(WORD, "ssk"),
            EOI_TOKEN
        ]
        actual = lexer.scan()

        self.assertEqual(expected, actual)

    def test_can_identify_primitive_numbers(self):
        lexer = Lexer("1 22 513")

        expected = [
            Token(NUMBER, "1"), Token(NUMBER, "22"), Token(NUMBER, "513"),
            EOI_TOKEN
        ]
        actual = lexer.scan()

        self.assertEqual(expected, actual)

    def test_can_identify_primitive_relevant_punctuation(self):
        lexer = Lexer("*k2, p2*; repeat 3 times. (k3, p3) x 2: []")

        expected = [
            Token(ASTERISK, "*"), Token(WORD, "k"), Token(NUMBER, "2"), Token(COMMA, ","),
            Token(WORD, "p"), Token(NUMBER, "2"), Token(ASTERISK, "*"), Token(SEMICOLON, ";"),
            Token(WORD, "repeat"), Token(NUMBER, "3"), Token(WORD, "times"), Token(PERIOD, "."),
            Token(OPEN_GROUP, "("), Token(WORD, "k"), Token(NUMBER, "3"), Token(COMMA, ","),
            Token(WORD, "p"), Token(NUMBER, "3"), Token(CLOSE_GROUP, ")"),
            Token(WORD, "x"), Token(NUMBER, "2"),
            Token(COLON, ":"), Token(OPEN_GROUP, "["), Token(CLOSE_GROUP, "]"),
            EOI_TOKEN
        ]
        actual = lexer.scan()

        self.assertEqual(expected, actual)

    def test_cannot_identify_irrelevant_primitive_punctuation(self):
        lexer = Lexer("k! *k2, p2*")

        with self.assertRaises(LexerError) as err:
            lexer.scan()
        self.assertEqual(str(err.exception), "LEXING ERROR DETECTED:\nFound unknown token \"!\"")

    def test_can_identify_newline(self):
        lexer = Lexer("cast on 12 sts\n" "*k2, p2*")

        expected = [
            Token(WORD, "cast"), Token(WORD, "on"), Token(NUMBER, "12"), Token(WORD, "sts"),
            Token(NEWLINE, "\n"),
            Token(ASTERISK, "*"), Token(WORD, "k"), Token(NUMBER, "2"), Token(COMMA, ","),
            Token(WORD, "p"), Token(NUMBER, "2"), Token(ASTERISK, "*"),
            EOI_TOKEN
        ]
        actual = lexer.scan()

        self.assertEqual(expected, actual)

class TestComplexLexing(unittest.TestCase):
    def test_can_combine_single_letter_stitch(self):
        lexer = Lexer("p")
        tokens = [Token(WORD, "p")]
        expected = [Token(STITCH, "p")]
        actual = lexer.combine(tokens)

        self.assertEqual(expected, actual)

    def test_can_combine_stitches_from_only_words(self):
        lexer = Lexer("k, p, ssk")
        tokens = [
            Token(WORD, "k"), Token(COMMA, ","), Token(WORD, "p"), Token(COMMA, ","), Token(WORD, "ssk"),
            EOI_TOKEN
        ]

        expected = [
            Token(STITCH, "k"), Token(COMMA, ","), Token(STITCH, "p"), Token(COMMA, ","), Token(STITCH, "ssk"),
            EOI_TOKEN
        ]
        actual = lexer.combine(tokens)

        self.assertEqual(expected, actual)

    def test_can_combine_stitches_from_prefix_number_suffix_pattern(self):
        lexer = Lexer("N/A")
        tokens = [Token(WORD, "k"), Token(NUMBER, "2"), Token(WORD, "tog")]
        
        expected = [Token(STITCH, "k2tog")]
        actual = lexer.combine(tokens)
        
        self.assertEqual(expected, actual)

    def test_can_not_combine_non_stitch_words(self):
        lexer = Lexer("N/A")
        tokens = [Token(WORD, "caston"), Token(WORD, "times")]

        expected = [Token(WORD, "caston"), Token(WORD, "times")]
        actual = lexer.combine(tokens)

        self.assertEqual(expected, actual)

    def test_can_combine_stitches_in_series_of_stitches_and_non_stitches(self):
        self.maxDiff = None

        lexer = Lexer("N/A")
        tokens = [
            Token(WORD, "caston"), Token(NUMBER, "10"), Token(WORD, "sts"), Token(NEWLINE, "\n"),
            Token(WORD, "row"), Token(NUMBER, "1"), Token(COLON, ":"),
            Token(WORD, "k"), Token(NUMBER, "2"), Token(COMMA, ","),
            Token(WORD, "c"), Token(NUMBER, "6"), Token(WORD, "f"), Token(COMMA, ","),
            Token(WORD, "k"), Token(NUMBER, "2"),
            EOI_TOKEN
        ]

        expected = [
            Token(WORD, "caston"), Token(NUMBER, "10"), Token(WORD, "sts"), Token(NEWLINE, "\n"),
            Token(WORD, "row"), Token(NUMBER, "1"), Token(COLON, ":"),
            Token(STITCH, "k"), Token(NUMBER, "2"), Token(COMMA, ","),
            Token(STITCH, "c6f"), Token(COMMA, ","),
            Token(STITCH, "k"), Token(NUMBER, "2"),
            EOI_TOKEN
        ]
        actual = lexer.combine(tokens)

        self.assertEqual(expected, actual)

class TestCompleteLexing(unittest.TestCase):
    def test_can_completely_tokenize_pattern(self):
        lexer = Lexer("caston 4 sts\n"
                    "row 1: p, k2tog, p\n"
                    "row 2: k, ssk")

        expected = [
            Token(WORD, "caston"), Token(NUMBER, "4"), Token(WORD, "sts"), Token(NEWLINE, "\n"),
            Token(WORD, "row"), Token(NUMBER, "1"), Token(COLON, ":"),
            Token(STITCH, "p"), Token(COMMA, ","), Token(STITCH, "k2tog"), Token(COMMA, ","), Token(STITCH, "p"), Token(NEWLINE, "\n"),
            Token(WORD, "row"), Token(NUMBER, "2"), Token(COLON, ":"),
            Token(STITCH, "k"), Token(COMMA, ","), Token(STITCH, "ssk"),
            EOI_TOKEN
        ]
        actual = lexer.tokenize()

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()