import re
import unittest
from src.backend.parser.parser import Parser, ParserError
from src.backend.domain.model import Stitch, Repeat, Row, Part

class TestParserCreation(unittest.TestCase):
    def test_can_create_parser(self):
        parser = Parser("k")
        assert parser is not None

    def test_parser_must_initialize_with_input(self):
        with self.assertRaises(TypeError) as err:
            parser = Parser()
        self.assertEqual(str(err.exception), "Parser.__init__() missing 1 required positional argument: 'input'")

    def test_can_parse(self):
        parser = Parser("k2")
        try:
            parser.start()
        except Exception:
            self.fail('Error occured while parsing: "k2"')

    def test_can_parse_single_stitch(self):
        parser = Parser("k2")
        expected_row = Row(1, [Stitch("k"), Stitch("k")])
        expected = Part(caston=2, rows=[expected_row])
        
        self.assertEqual(expected, parser.start())

    def test_can_parse_single_stitch_sequence(self):
        parser = Parser("k2, p2")
        expected_row = Row(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")])
        expected = Part(caston=4, rows=[expected_row])
        
        self.assertEqual(expected, parser.start())

    def test_can_parse_single_row_without_caston(self):
        parser = Parser("row 1: k, p2")
        expected_row = Row(1, [Stitch("k"), Stitch("p"), Stitch("p")])
        expected = Part(caston=3, rows=[expected_row])
        
        self.assertEqual(expected, parser.start())

    def test_can_parse_single_row_with_caston(self):
        parser = Parser("cast on 4 stitches\n"
                        "k2, p2")
        expected_row = Row(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")])
        expected = Part(4, [expected_row])

        self.assertEqual(expected, parser.start())

    def test_can_parse_multiple_rows_with_caston(self):
        parser = Parser("cast on 4 stitches\n"
                        "row 1: k2, p2\n"
                        "row 2: p2, k2\n"
                        "row 3: k2, p2")
        expected = Part(4, [
            Row(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")]),
            Row(2, [Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")]),
            Row(3, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")])
        ])
        
        self.assertEqual(expected, parser.start())

    def test_cannot_parse_multiple_rows_without_caston(self):
        parser = Parser("row 1: k2, p2\n"
                        "row 2: p2, k2\n"
                        "row 3: k2, p2")
        
        with self.assertRaises(TypeError) as err:
            parser.start()
        self.assertEqual(str(err.exception), "Part caston must be type int, got type <class 'NoneType'>")

    def test_can_parse_non_number_specified_repeats(self):
        parser = Parser("cast on 12 st\n"
            "k3, *p2, k2*, k1")
        expected_row = Row(
            1, [Stitch("k"), Stitch("k"), Stitch("k"),
            Repeat(elements=[Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")], num_times=None),
            Stitch("k")]
        )
        expected = Part(12, [expected_row])
        actual = parser.start()
        self.assertEqual(expected, actual, f"expected part was Part({expected.caston}, [Row({expected_row.number}, [{expected_row.instructions}])]).\n actual was Part({actual.caston}, [Row({actual.rows[0].number}, [{actual.rows[0].instructions}])])")

    def test_repeat_cannot_parse_without_caston(self):
        ...


if __name__ == "__main__":
    unittest.main()