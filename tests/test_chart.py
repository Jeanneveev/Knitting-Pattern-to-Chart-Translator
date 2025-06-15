import pytest
from src.models.model import Stitch, Row, Pattern, Chart
from src.parser.parser import Parser

def generate_pattern(num_rows:int) -> Pattern:
    statement = ""
    for i in range(1, num_rows+1):
        if i == num_rows:
            statement += f"row {i}: k2, p2"
            break
        statement += f"row {i}: k2, p2\n "
    return Parser(statement).start()
        
def test_get_one_right_side_row_symbols():
    pattern = generate_pattern(1)
    assert Chart(pattern).get_row_symbols(1) == {1: ["X", "X", " ", " "]}

def test_get_one_wrong_side_row_symbols():
    pattern = generate_pattern(3)
    assert Chart(pattern).get_row_symbols(2) == {2: ["X", "X", " ", " "]}

def test_render_ascii_grid_one_row():
    pattern = generate_pattern(1)
    expected = (
        "---+---+---+---+---+---\n"
        "   | X | X |   |   | 1 \n"
        "---+---+---+---+---+---"
    )
    assert Chart(pattern).render_grid() == expected

def test_render_ascii_grid_multiple_rows():
    pattern = generate_pattern(3)
    expected = (
        "---+---+---+---+---+---\n"
        "   | X | X |   |   | 1 \n"
        "---+---+---+---+---+---\n"
        " 2 | X | X |   |   |   \n"
        "---+---+---+---+---+---\n"
        "   | X | X |   |   | 3 \n"
        "---+---+---+---+---+---"
    )
    assert Chart(pattern).render_grid() == expected