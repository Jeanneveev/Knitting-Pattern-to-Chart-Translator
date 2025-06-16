import re
import pytest
from src.parser.parser import Parser, ParserError
from src.models.model import Stitch, Repeat, Row, Pattern

def test_can_create_parser():
    parser = Parser("k")
    assert parser is not None

def test_parser_must_initialize_with_input():
    with pytest.raises(TypeError, match=re.escape("Parser.__init__() missing 1 required positional argument: 'input'")):
        parser = Parser()

def test_can_parse():
    parser = Parser("k2")
    try:
        parser.start()
    except Exception:
        pytest.fail('Error occured while parsing: "k2"')

def test_can_parse_single_stitch():
    parser = Parser("k2")
    expected_result_row = Row(1, [Stitch("k"), Stitch("k")])
    assert parser.start() == Pattern([expected_result_row])

def test_can_parse_single_stitch_sequence():
    parser = Parser("k2, p2")
    expected_result_row = Row(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")])
    assert parser.start() == Pattern([expected_result_row])

def test_can_parse_single_row():
    parser = Parser("row 1: k, p2")
    expected_result_row = Row(1, [Stitch("k"), Stitch("p"), Stitch("p")])
    assert parser.start() == Pattern([expected_result_row])

def test_can_parse_multiple_rows():
    parser = Parser("row 1: k2, p2\n"
                    "row 2: p2, k2\n"
                    "row 3: k2, p2")
    assert parser.start() == Pattern([
        Row(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")]),
        Row(2, [Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")]),
        Row(3, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")])
    ])

def test_can_parse_caston_row():
    parser = Parser("cast on 4 stitches\n"
                    "k2, p2")
    expected_result_row = Row(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")], 4)
    assert parser.start() == Pattern([expected_result_row], 4)

def test_can_parse_caston_and_multiple_rows():
    parser = Parser("cast on 4 stitches\n"
                    "row 1: k2, p2\n"
                    "row 2: p2, k2\n"
                    "row 3: k2, p2")
    expected_rows = [
        Row(1, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")], 4),
        Row(2, [Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")], 4),
        Row(3, [Stitch("k"), Stitch("k"), Stitch("p"), Stitch("p")], 4)
    ]
    assert parser.start() == Pattern(expected_rows, 4)

def test_can_parse_non_number_specified_repeats():
    parser = Parser("cast on 12 st\n"
        "k3, *p2, k2*, k1")
    expected_row = Row(1, [Stitch("k"), Stitch("k"), Stitch("k"),
                        Repeat(stitches=[Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")], until="end"),
                        Stitch("k")
                    ], 12)
    assert parser.start() == Pattern([expected_row], 12)

def test_can_parse_number_specified_repeats():
    parser = Parser("cast on 12 st\n"
        "k3, *p2, k2*; repeat from * to * 2 times, k1")
    expected_row = Row(1, [Stitch("k"), Stitch("k"), Stitch("k"),
                        Repeat(stitches=[Stitch("p"), Stitch("p"), Stitch("k"), Stitch("k")], times=2),
                        Stitch("k")
                    ], 12)
    assert parser.start() == Pattern([expected_row], 12)

def test_can_only_parse_repeat_if_caston_set():
    with pytest.raises(ParserError, match="The number of stitches cast-on must be specified in patterns with repeats"):
        parser = Parser("k3, *p2, k2*, k1")
        parser.start()
