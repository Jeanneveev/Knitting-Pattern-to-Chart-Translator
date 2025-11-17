import unittest
from src.domain.model.model import Part, Row, Repeat, Stitch
from src.adapters.parser_adapter import ParserAdapter
from src.domain.parser.parser import ParserError

class TestParserAdapter(unittest.TestCase):
    def test_can_parse_model_from_rowless_pattern(self):
        pattern = "k2, p2, k2"

        expected = Part(6, [
            Row(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")])
        ])
        actual = ParserAdapter().parse(pattern)

        self.assertEqual(expected, actual)

    def test_raises_error_on_invalid_pattern_input(self):
        pattern = "invalid input"

        with self.assertRaises(ParserError) as err:
            ParserAdapter().parse(pattern)
        self.assertEqual('PARSER ERROR DETECTED:\nFound the token: "invalid"\nBut was expecting one of: "row"', str(err.exception))

if __name__ == "__main__":
    unittest.main()