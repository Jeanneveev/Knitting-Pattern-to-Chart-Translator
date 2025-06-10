import re
import pytest
from parser.parser import Parser

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
    assert parser.start() == ["k", "k"]