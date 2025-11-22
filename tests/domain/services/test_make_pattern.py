import unittest
from src.domain.model.model import Stitch, Repeat, Row, Part
from src.domain.services.make_pattern import ExpandedRow, Pattern, PatternBuilder

class TestExpandedRow(unittest.TestCase):
    def test_expandedrow_must_be_initalized_with_number_stitches_and_start_count(self):
        ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p")], start_st_count=2)

        with self.assertRaises(TypeError) as err:
            ExpandedRow(2)
        self.assertEqual("ExpandedRow.__init__() missing 2 required positional arguments: 'stitches' and 'start_st_count'", str(err.exception))

    def test_start_st_count_must_be_equal_to_stitch_length_if_no_increases(self):
        with self.assertRaises(ValueError) as err:
            ExpandedRow(1, [Stitch("k"), Stitch("p"), Stitch("k")], 2)
        self.assertEqual("Start_st_count is incorrect, 2 was given when it should be 3", str(err.exception))

    def test_start_st_count_must_be_less_than_stitch_length_if_increases(self):
        with self.assertRaises(ValueError) as err:
            ExpandedRow(1, [Stitch("k"), Stitch("yo"), Stitch("k")], 4)
        self.assertEqual("Start_st_count is incorrect, 4 was given when it should be 2", str(err.exception))

    def test_start_st_count_must_be_more_than_stitch_length_if_decreases(self):
        with self.assertRaises(ValueError) as err:
            ExpandedRow(1, [Stitch("k"), Stitch("ssk"), Stitch("k")], 3)
        self.assertEqual("Start_st_count is incorrect, 3 was given when it should be 4", str(err.exception))

    def test_end_st_count_increases_if_there_are_increasing_stitches(self):
        row = ExpandedRow(2, [Stitch("k"), Stitch("yo"), Stitch("k")], 2)
        self.assertEqual(row.end_st_count, 3)

    def test_end_st_count_decreases_if_there_are_decreasing_stitches(self):
        row = ExpandedRow(2, [Stitch("k"), Stitch("ssk"), Stitch("k")], 4)
        self.assertEqual(row.end_st_count, 3)

    def test_can_get_right_side_symbols_of_expandedrow(self):
        row = ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p"), Stitch("p")], start_st_count=3)
        expected = [" ", "-", "-"]
        self.assertEqual(expected, row.get_symbols_rs())

    def test_can_get_wrong_side_symbols_of_row(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p"), Stitch("p")], 3)
        expected = ["-", " ", " "]
        self.assertEqual(expected, row.get_symbols_ws())

class TestBuildExpandedRow(unittest.TestCase):
    def test_can_compute_stitches_after_implicit_repeat_with_only_stitches_after(self):
        row = Row(number=1, instructions=[
            Stitch("k"), Repeat([Stitch("p"), Stitch("k")], num_times=2), Stitch("k"),
            Repeat([Stitch("p"), Stitch("k")]), Stitch("k"), Stitch("k")
        ])
        builder = PatternBuilder(Part(6, [row]))
        
        builder.resolve_implicit_repeat(row)

        expected = 2
        actual = row.instructions[3].stitches_after

        self.assertEqual(expected, actual)

    def test_can_compute_stitches_after_implicit_repeat_with_explicit_repeat_after(self):
        row = Row(number=1, instructions=[
            Stitch("p"),
            Repeat([Stitch("p"), Stitch("k")]),
            Repeat([Stitch("k"), Stitch("p")], num_times=2),
            Stitch("p")
        ])
        part = Part(12, [row])
        builder = PatternBuilder(part)

        builder.resolve_implicit_repeat(row)

        expected = 5
        actual = row.instructions[1].stitches_after

        self.assertEqual(expected, actual)

    def test_can_expand_row_of_all_stitches(self):
        row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("k")])
        part = Part(3, [row])
        builder = PatternBuilder(part)

        expected = ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p"), Stitch("k")], start_st_count=3)
        actual = builder.build_expanded_row(row, part.caston)

        self.assertEqual(expected, actual)

    def test_can_expand_row_with_some_explicit_repeats(self):
        row = Row(number=1, instructions=[Stitch("k"), Repeat([Stitch("p"), Stitch("k")], num_times=2)])
        part = Part(5, [row])
        builder = PatternBuilder(part)

        expected = ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k")], start_st_count=5)
        actual = builder.build_expanded_row(row, part.caston)

        self.assertEqual(expected, actual)

    def test_can_expand_row_with_a_implicit_repeat(self):
        row = Row(number=1, instructions=[Stitch("k"), Repeat([Stitch("p"), Stitch("k")]), Stitch("k")])
        part = Part(6, [row])
        builder = PatternBuilder(part)

        expected = ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("k")], start_st_count=6)
        actual = builder.build_expanded_row(row, part.caston)

        self.assertEqual(expected, actual)
        
class TestPattern(unittest.TestCase):
    def test_pattern_must_be_initialized_with_rows(self):
        Pattern(rows=[ExpandedRow(1, [Stitch("k")], 1)])

        with self.assertRaises(TypeError) as err:
            Pattern()
        self.assertEqual("Pattern.__init__() missing 1 required positional argument: 'rows'", str(err.exception))

    def test_sorts_rows_by_number_on_initialization(self):
        row_1 = ExpandedRow(1, [Stitch("k"), Stitch("yo")], 1)
        row_2 = ExpandedRow(2, [Stitch("k"), Stitch("p")], 2)
        row_3 = ExpandedRow(3, [Stitch("ssk")], 2)
        pattern = Pattern(rows=[row_2, row_3, row_1])

        expected = [row_1, row_2, row_3]
        actual = pattern.rows

        self.assertEqual(expected, actual)

    def test_row_numbers_must_be_unique(self):
        row_a = ExpandedRow(1, [Stitch("k")], 1)
        row_b = row_a
        
        with self.assertRaises(ValueError) as err:
            Pattern([row_a, row_b])
        self.assertEqual("Row numbers must be unique", str(err.exception))

    def test_row_numbers_must_be_sequential(self):
        row_1 = ExpandedRow(1, [Stitch("k")], 1)
        row_3 = ExpandedRow(3, [Stitch("k")], 1)

        with self.assertRaises(ValueError) as err:
            Pattern([row_1, row_3])
        self.assertEqual("Row numbers must be sequential", str(err.exception))

    def test_row_lengths_must_be_congruent(self):
        with self.assertRaises(ValueError) as err:
            Pattern(rows=[
                ExpandedRow(1, [Stitch("k"), Stitch("p")], 2),
                ExpandedRow(2, [Stitch("p"), Stitch("k"), Stitch("p")], 3)
            ])
        self.assertEqual(
            "Error on row 2. The start length of each row must be equal to the end length of the previous row",
            str(err.exception)
        )

    def test_can_get_row_by_number(self):
        pattern = Pattern(rows=[
            ExpandedRow(1, [Stitch("k")], 1),
            ExpandedRow(3, [Stitch("k"), Stitch("k")], 2),
            ExpandedRow(2, [Stitch("p"), Stitch("yo")], 1)
        ])

        expected = ExpandedRow(2, [Stitch("p"), Stitch("yo")], 1)
        actual = pattern.get_row(2)

        self.assertEqual(expected, actual)

    def test_can_get_max_length_of_pattern_of_regular_stitches(self):
        pattern = Pattern(rows=[
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k")], 4),
            ExpandedRow(2, [Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")], 4),
        ])

        expected = 4
        actual = pattern.get_max_length()

        self.assertEqual(expected, actual)

    def test_can_get_max_length_of_pattern_with_increases(self):
        pattern = Pattern(rows=[
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("k")], 3),
            ExpandedRow(2, [Stitch("p"), Stitch("yo"), Stitch("p"), Stitch("yo"), Stitch("p")], 3),
        ])

        expected = 5
        actual = pattern.get_max_length()

        self.assertEqual(expected, actual)

    def test_can_get_max_length_of_pattern_with_decreases(self):
        pattern = Pattern(rows=[
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("k")], 3),
            ExpandedRow(2, [Stitch("p"), Stitch("ssk")], 3),
        ])

        expected = 3
        actual = pattern.get_max_length()

        self.assertEqual(expected, actual)

    def test_can_get_used_stitches_in_pattern(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("p"), Stitch("yo"), Stitch("p"), Stitch("k")], 4)
        ])

        expected = ["k", "p", "yo"]
        actual = pattern.get_stitches_used()

        self.assertEqual(expected, actual)

class TestBuildPattern(unittest.TestCase):
    def test_can_correct_assumed_caston(self):
        part = Part(7, [
            Row(1, [Stitch("p"), Stitch("ssk"), Stitch("p"), Stitch("yo"), Stitch("p"), Stitch("ssk"), Stitch("p")]),
            Row(2, [Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p")]),
        ], assumed_caston=True)
        builder = PatternBuilder(part)
        
        expected = Part(8, [
            Row(1, [Stitch("p"), Stitch("ssk"), Stitch("p"), Stitch("yo"), Stitch("p"), Stitch("ssk"), Stitch("p")]),
            Row(2, [Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p")]),
        ], assumed_caston=False)
        actual = builder.part

        self.assertEqual(expected, actual)

    def test_can_build_pattern_from_part(self):
        row = Row(number=1, instructions=[
            Stitch("k"), Repeat([Stitch("p"), Stitch("k")], num_times=2), Stitch("k"),
            Repeat([Stitch("p"), Stitch("k")]), Stitch("p"), Stitch("p")
        ])
        builder = PatternBuilder(Part(12, [row]))

        expected = Pattern([
            ExpandedRow(1, [
                Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("k"),
                Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("p")
            ], 12)
        ])
        actual = builder.build_pattern()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()