import unittest
from src.domain import Stitch, Repeat, Row, Part
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

    def test_can_parse_model_from_rowed_pattern(self):
        pattern = (
            "cast on 3 sts\n"
            "row 1: k, p, k\n"
            "row 2: k2, p"
        )

        expected = Part(3, [
            Row(1, [Stitch("k"), Stitch("p"), Stitch("k")]),
            Row(2, [Stitch("k"), Stitch("k"), Stitch("p")])
        ])
        actual = ParserAdapter().parse(pattern)

        self.assertEqual(expected, actual)

    def test_can_parse_from_pattern_with_explicit_repeats(self):
        pattern = (
            "cast on 6 sts\n"
            "row 1: *k, p*; repeat from * to * 3 times"
        )

        expected = Part (6, [
            Row(1, [Repeat([Stitch("k"), Stitch("p")], num_times=3)])
        ])
        actual = ParserAdapter().parse(pattern)

        self.assertEqual(expected, actual)

    def test_can_parse_from_pattern_with_impicit_repeats(self):
        pattern = (
            "cast on 6 sts\n"
            "row 1: *k, p*\n"
            "row 2: k2, p2, k2"
        )

        expected = Part (6, [
            Row(1, [Repeat([Stitch("k"), Stitch("p")], num_times=None)]),
            Row(2, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")])
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