import re
import pytest
from src.parser.parser import Parser
from src.models.model import Stitch, Row, Pattern

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
