import unittest
from src.domain.parser.parser import Parser, ParserError
from src.domain.ast.nodes import StitchNode, RepeatNode, RowNode, PartNode

class TestParser(unittest.TestCase):
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
        expected_row = RowNode(1, [StitchNode("k"), StitchNode("k")])
        expected = PartNode(caston=2, rows=[expected_row], assumed_caston=True)
        
        self.assertEqual(expected, parser.start())

    def test_can_parse_single_stitch_sequence(self):
        parser = Parser("k2, p2")
        expected_row = RowNode(1, [StitchNode("k"), StitchNode("k"), StitchNode("p"), StitchNode("p")])
        expected = PartNode(caston=4, rows=[expected_row], assumed_caston=True)
        
        self.assertEqual(expected, parser.start())

    def test_can_parse_single_row_without_caston(self):
        parser = Parser("row 1: k, p2")
        expected_row = RowNode(1, [StitchNode("k"), StitchNode("p"), StitchNode("p")])
        expected = PartNode(caston=3, rows=[expected_row])
        
        self.assertEqual(expected, parser.start())

    def test_can_parse_single_row_with_caston(self):
        parser = Parser("cast on 4 stitches\n"
                        "k2, p2")
        expected_row = RowNode(1, [StitchNode("k"), StitchNode("k"), StitchNode("p"), StitchNode("p")])
        expected = PartNode(4, [expected_row])

        self.assertEqual(expected, parser.start())

    def test_can_parse_multiple_rows_with_caston(self):
        parser = Parser("cast on 4 stitches\n"
                        "row 1: k2, p2\n"
                        "row 2: p2, k2\n"
                        "row 3: k2, p2")
        expected = PartNode(4, [
            RowNode(1, [StitchNode("k"), StitchNode("k"), StitchNode("p"), StitchNode("p")]),
            RowNode(2, [StitchNode("p"), StitchNode("p"), StitchNode("k"), StitchNode("k")]),
            RowNode(3, [StitchNode("k"), StitchNode("k"), StitchNode("p"), StitchNode("p")])
        ])
        
        self.assertEqual(expected, parser.start())

    def test_can_parse_implicit_repeats(self):
        parser = Parser("cast on 12 st\n"
                        "k3, *p2, k2*, k1")
        expected_row = RowNode(
            1, [StitchNode("k"), StitchNode("k"), StitchNode("k"),
            RepeatNode(elements=[StitchNode("p"), StitchNode("p"), StitchNode("k"), StitchNode("k")], num_times=None),
            StitchNode("k")]
        )
        expected = PartNode(12, [expected_row])
        actual = parser.start()
        self.assertEqual(expected, actual, f"expected part was PartNode({expected.caston}, [RowNode({expected_row.number}, [{expected_row.instructions}])]).\n actual was PartNode({actual.caston}, [RowNode({actual.rows[0].number}, [{actual.rows[0].instructions}])])")

    def test_can_parse_explicit_repeats(self):
        parser = Parser(
            "cast on 12 st\n"
            "k3, *p2, k2*; repeat from * to * 2 times, k1"
        )
        expected_row = RowNode(1, [
            StitchNode("k"), StitchNode("k"), StitchNode("k"),
            RepeatNode([StitchNode("p"), StitchNode("p"), StitchNode("k"), StitchNode("k")], num_times=2),
            StitchNode("k")
        ])
        expected = PartNode(12, [expected_row])
        actual = parser.start()
        self.assertEqual(expected, actual)

    def test_can_parse_increase(self):
        parser = Parser("cast on 5 sts\n"
                        "k2, yo, k1, yo, k2")
        expected_row = RowNode(1, [
            StitchNode("k"), StitchNode("k"), StitchNode("yo"), StitchNode("k"), StitchNode("yo"), StitchNode("k"), StitchNode("k")
        ])
        expected = PartNode(5, [expected_row])
        actual = parser.start()
        self.assertEqual(expected, actual)

    def test_can_parse_decrease(self):
        parser = Parser("cast on 7 sts\n"
                        "k1, k2tog, k1, ssk, k")
        expected_row = RowNode(1, [
            StitchNode("k"), StitchNode("k2tog"), StitchNode("k"), StitchNode("ssk"), StitchNode("k")
        ])
        expected = PartNode(7, [expected_row])
        actual = parser.start()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()