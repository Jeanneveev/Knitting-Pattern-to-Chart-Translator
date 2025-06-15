import pytest
from src.models.model import Stitch, Row, Pattern

def test_can_create_stitch():
    stitch = Stitch("k")
    assert stitch.abbrev == "k"

def test_can_get_stitch_symbol():
    stitch = Stitch("k")
    assert stitch.symbol_rs == " "
    assert stitch.symbol_ws == "X"

def test_can_create_row():
    row = Row(1, [Stitch("k"), Stitch("p"), Stitch("k")])
    assert row.number == 1
    assert len(row.stitches) == 3
    assert row.stitches[1].abbrev == "p"

def test_can_create_pattern():
    row1 = Row(1, [Stitch("k"), Stitch("p"), Stitch("k")])
    row2 = Row(2, [Stitch("p"), Stitch("k"), Stitch("p")])
    pattern = Pattern([row1, row2])
    assert len(pattern.rows) == 2
    assert pattern.rows[0].stitches[2].abbrev == "k"

def test_can_get_row_by_number():
    row1 = Row(1, [Stitch("k"), Stitch("p"), Stitch("k")])
    row2 = Row(2, [Stitch("p"), Stitch("k"), Stitch("p")])
    pattern = Pattern([row1, row2])
    assert pattern.get_row(2) == Row(2, [Stitch("p"), Stitch("k"), Stitch("p")])
