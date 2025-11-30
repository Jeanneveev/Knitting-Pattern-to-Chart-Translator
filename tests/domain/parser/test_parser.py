import unittest
from src.domain.parser.lexer import Token, TokenType
from src.domain.parser.parser import Parser, ParserError
from src.domain.ast.nodes import StitchNode, RepeatNode, RowNode, PartNode

class TestParserHelpers(unittest.TestCase):
    def test_can_expect_value_given_single_value(self):
        text = "test text"
        parser = Parser(text)

        expected = Token(TokenType.WORD, "test")
        actual = parser.expect_value(["test"])

        self.assertEqual(expected, actual)
    
    def test_can_expect_value_given_multiple_values(self):
        text = "test text"
        parser = Parser(text)

        expected = Token(TokenType.WORD, "test")
        actual = parser.expect_value(["smth", "test", "example"])

        self.assertEqual(expected, actual)

    def test_raise_error_if_current_token_value_not_expected(self):
        text = "test text"
        parser = Parser(text)

        with self.assertRaises(ParserError) as err:
            parser.expect_value(["other"])

        self.assertEqual((
            "PARSER ERROR DETECTED:\n"
            "Found the token: \"test\"\n"
            "But was expecting one of: [\"other\"]"
        ), str(err.exception))

    def test_can_expect_type_given_single_type(self):
        text = "test text"
        parser = Parser(text)

        expected = Token(TokenType.WORD, "test")
        actual = parser.expect_type([TokenType.WORD])

        self.assertEqual(expected, actual)

    def test_can_expect_type_given_multiple_types(self):
        text = "test text"
        parser = Parser(text)

        expected = Token(TokenType.WORD, "test")
        actual = parser.expect_type([TokenType.ASTERISK, TokenType.WORD])

        self.assertEqual(expected, actual)

    def test_raise_error_if_current_token_type_not_expected(self):
        text = "test text"
        parser = Parser(text)

        with self.assertRaises(ParserError) as err:
            parser.expect_type([TokenType.COLON])

        self.assertEqual((
            "PARSER ERROR DETECTED:\n"
            "Found token of type: \"WORD\"\n"
            "But was expecting one of: [\"COLON\"]"
        ), str(err.exception))

    def test_can_expect_series(self):
        text = "test text with many words"
        parser = Parser(text)

        expected = Token(TokenType.WORD, "many")
        actual = parser.expect_series(["test", "text", "with"])

        self.assertEqual(expected, actual)

    def test_raise_error_if_token_value_series_not_expected(self):
        text = "test text with many words"
        parser = Parser(text)

        with self.assertRaises(ParserError) as err:
            parser.expect_series(["test", "test", "text"])

        self.assertEqual((
            "PARSER ERROR DETECTED:\n"
            "Found the token: \"text\"\n"
            "But was expecting: \"test\""
        ), str(err.exception))

    def test_can_check_current_token_value_and_advance_given_one_value(self):
        text = "test text with many words"
        parser = Parser(text)

        expected = True
        actual = parser.is_value(["test"])

        self.assertEqual(expected, actual)
        self.assertEqual("text", parser._curr_token.value)

    def test_can_check_current_token_value_and_advance_given_multiple_values(self):
        text = "test text with many words"
        parser = Parser(text)

        expected = True
        actual = parser.is_value(["test", "smth", "else"])

        self.assertEqual(expected, actual)
        self.assertEqual("text", parser._curr_token.value)

    def test_can_check_current_token_value_isnt_in_given_values(self):
        text = "test text with many words"
        parser = Parser(text)

        expected = False
        actual = parser.is_value(["smth", "else"])

        self.assertEqual(expected, actual)
        self.assertEqual("test", parser._curr_token.value)

    def test_can_check_value_and_not_advance_given_one_value(self):
        text = "test text with many words"
        parser = Parser(text)

        expected = True
        actual = parser.check_value(["test"])

        self.assertEqual(expected, actual)
        self.assertEqual("test", parser._curr_token.value)

    def test_can_check_value_and_not_advance_given_multiple_values(self):
        text = "test text with many words"
        parser = Parser(text)

        expected = True
        actual = parser.check_value(["smth", "test"])

        self.assertEqual(expected, actual)
        self.assertEqual("test", parser._curr_token.value)

    def test_can_check_value_isnt_in_given_values(self):
        text = "test text with many words"
        parser = Parser(text)

        expected = False
        actual = parser.check_value(["smth", "else"])

        self.assertEqual(expected, actual)
        self.assertEqual("test", parser._curr_token.value)

    def test_can_check_type_and_not_advance_given_one_type(self):
        text = "test text"
        parser = Parser(text)

        expected = True
        actual = parser.check_type([TokenType.WORD])

        self.assertEqual(expected, actual)
        self.assertEqual("test", parser._curr_token.value)

    def test_can_check_type_and_not_advance_given_multiple_types(self):
        text = "test text"
        parser = Parser(text)

        expected = True
        actual = parser.check_type([TokenType.WORD, TokenType.NUMBER])

        self.assertEqual(expected, actual)
        self.assertEqual("test", parser._curr_token.value)

    def test_can_check_type_isnt_in_given_types(self):
        text = "test text"
        parser = Parser(text)

        expected = False
        actual = parser.check_type([TokenType.SEMICOLON])

        self.assertEqual(expected, actual)
        self.assertEqual("test", parser._curr_token.value)

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

    def test_can_parse_single_stitch_sequence_with_caston(self):
        parser = Parser("cast on 4 stitches\n"
                        "k2, p2")
        expected_row = RowNode(1, [StitchNode("k"), StitchNode("k"), StitchNode("p"), StitchNode("p")])
        expected = PartNode(4, [expected_row])

        self.assertEqual(expected, parser.start())

    def test_can_parse_single_row_with_caston(self):
        parser = Parser("cast on 4 stitches\n"
                        "row 1: k2, p2")
        expected_row = RowNode(1, [StitchNode("k"), StitchNode("k"), StitchNode("p"), StitchNode("p")])
        expected = PartNode(4, [expected_row])

        self.assertEqual(expected, parser.start())

    def test_can_caston_with_multiple_terms(self):
        parser_1 = Parser("caston 2 stitches\n"
                          "k2")
        parser_2 = Parser("cast on 3 sts\n"
                          "k2, p")
        parser_3 = Parser("CO 4 st\n"
                          "k2, p2")
        
        expected_row_1 = RowNode(1, [StitchNode("k"), StitchNode("k")])
        expected_row_2 = RowNode(1, [StitchNode("k"), StitchNode("k"), StitchNode("p")])
        expected_row_3 = RowNode(1, [StitchNode("k"), StitchNode("k"), StitchNode("p"), StitchNode("p")])
        expected_1 = PartNode(2, [expected_row_1])
        expected_2 = PartNode(3, [expected_row_2])
        expected_3 = PartNode(4, [expected_row_3])
        actual_1 = parser_1.start()
        actual_2 = parser_2.start()
        actual_3 = parser_3.start()

        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)
        self.assertEqual(expected_3, actual_3)

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

    def test_cannot_parse_repeat_without_caston(self):
        parser = Parser(
            "k3, *p2, k2*; repeat from * to * 2 times, k1"
        )

        with self.assertRaises(ParserError) as err:
            parser.start()

        self.assertEqual((
            "PARSER ERROR DETECTED:\n"
            "Cannot parse repeat without caston number"
        ), str(err.exception))

    def test_can_parse_implicit_repeats_in_multiple_ways(self):
        parser_1 = Parser("cast on 4 sts\n"
                          "*k, p*")
        parser_2 = Parser("caston 4 sts\n"
                          "(k, p)")
        parser_3 = Parser("caston 4 sts\n"
                          "[k, p]")
        
        expected_repeat = RepeatNode([StitchNode("k"), StitchNode("p")], num_times=None)
        expected = PartNode(4, [RowNode(1, [expected_repeat])])
        actual_1 = parser_1.start()
        actual_2 = parser_2.start()
        actual_3 = parser_3.start()

        self.assertEqual(expected, actual_1)
        self.assertEqual(expected, actual_2)
        self.assertEqual(expected, actual_3)

    def test_can_parse_explicit_repeats_in_multiple_ways(self):
        parser_1 = Parser("cast on 6 sts\n"
                          "*k, p, k*; repeat 2 times")
        parser_2 = Parser("caston 6 sts\n"
                          "(k, p, k) x 2")
        parser_3 = Parser("caston 6 sts\n"
                          "[k, p, k] 2 times")
        
        expected_repeat = RepeatNode([StitchNode("k"), StitchNode("p"), StitchNode("k")], 2)
        expected = PartNode(6, [RowNode(1, [expected_repeat])])
        actual_1 = parser_1.start()
        actual_2 = parser_2.start()
        actual_3 = parser_3.start()

        self.assertEqual(expected, actual_1)
        self.assertEqual(expected, actual_2)
        self.assertEqual(expected, actual_3)


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