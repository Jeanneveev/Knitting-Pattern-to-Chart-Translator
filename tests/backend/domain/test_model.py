import re
import pytest
from src.backend.domain.model import Stitch, Repeat, Row, Section, StitchType

def test_stitch_type_has_limited_values():
    stitch_types = ["reg", "incr", "decr"]
    for st in stitch_types:
        assert StitchType(st) is not None
    
    invalid_type = "smth"
    with pytest.raises(ValueError, match=re.escape(f"'{invalid_type}' is not a valid StitchType")):
        StitchType(invalid_type)

def test_can_create_stitch_by_abbreviation():
    stitch = Stitch(abbrev="k")
    assert stitch.name == "knit"

def test_can_create_stitch_with_different_stitch_type():
    st = StitchType("incr")
    stitch = Stitch(abbrev="k", type=st)
    assert stitch.name == "knit"

def test_setting_repeat_with_num_times_sets_has_num_times():
    repeat = Repeat(elements=[Stitch("k"), Stitch("p")], num_times=3)
    assert repeat.has_num_times == True

def test_setting_repeat_without_num_times_sets_has_num_times_to_false():
    repeat = Repeat(elements=[Stitch("k"), Stitch("p")])
    assert repeat.has_num_times == False

def test_repeats_cannot_be_nested_one_level():
    assert Repeat(elements=[Repeat(elements=[Stitch("k")])]) is not None

def test_repeats_cannot_be_nested_more_than_one_level():
    with pytest.raises(SyntaxError, match="Repeats cannot be nested more than once"):
        overnested = Repeat(elements=[Repeat(elements=[Repeat(elements=[])])])

def test_can_expand_fixed_num_time_repeat():
    repeat = Repeat(elements=[Stitch("k"), Stitch("p")], num_times=3)
    assert repeat.expand() == [Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p")]

def test_can_expand_repeat_with_a_given_number_of_remaining_stitches():
    repeat = Repeat(elements=[Stitch("k"), Stitch("p")])
    assert repeat.expand(remaining_stitches=8) == [Stitch("k"), Stitch("p")] * 4

def test_can_expand_repeat_with_stitches_afterwards():
    repeat = Repeat(elements=[Stitch("k"), Stitch("p")], stitches_after=1)
    assert repeat.expand(remaining_stitches=5) == [Stitch("k"), Stitch("p")] * 2

def test_rows_must_be_initialized_with_number_and_instructions():
    row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("k")])
    
    with pytest.raises(TypeError, match=re.escape("Row.__init__() missing 1 required positional argument: 'instructions'")):
        row_invalid = Row(2)

def test_row_stitches_equal_row_instructions_if_no_repeats_in_instructions():
    row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("k")])
    assert row.stitches == [Stitch("k"), Stitch("p"), Stitch("k")]

def test_row_stitches_can_expand_fixed_timed_repeats_in_row_instructions():
    row = Row(number=1, instructions=[
        Repeat([Stitch("p"), Stitch("k")], 2),
        Stitch("k"),
        Repeat([Stitch("p"), Stitch("k")], 3),
        Stitch("k")
    ])
    assert row.stitches == [
        Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"),
        Stitch("k"),
        Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"),
        Stitch("k")
    ]

def test_current_row_stitch_count_equals_previous_stitch_count_if_row_only_contains_regular_type_stitches():
    row = Row(number=1, instructions=[Stitch("k"), Repeat([Stitch("p"), Stitch("k")])])
    assert row.get_stitch_count(5) == 5

## TODO: HANDLE REPEATS WITH UNDEFINED REPEAT COUNTS

def test_section_must_include_caston_num_and_rows():
    section = Section(caston=1, rows=[Row(1, [Stitch("p")])])

    with pytest.raises(TypeError, match=re.escape("Section.__init__() missing 2 required positional arguments: 'caston' and 'rows'")):
        section_invalid = Section()

# def test_section_pattern_includes_row_number_and_row_stitch_count():
#     row_1 = Row(1, [Stitch("p"), Stitch("k"), Stitch("p")])
#     row_2 = Row(2, [Stitch("k"), Stitch("p"), Stitch("k")])
#     section = Section(caston=3, rows=[row_1, row_2])
    
#     assert section.pattern == [(1, 3), (2, 3)]