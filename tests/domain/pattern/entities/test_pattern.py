import unittest
from src.domain.pattern.entities.model import Stitch, Repeat, Row, Part
from src.domain.pattern.entities.pattern import ExpandedRow, Pattern

class TestExpandedRow(unittest.TestCase):
    def test_expandedrow_must_be_initalized_with_number_stitches_and_start_count(self):
        ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p")])

        with self.assertRaises(TypeError) as err:
            ExpandedRow(2)
        self.assertEqual("ExpandedRow.__init__() missing 1 required positional argument: 'stitches'", str(err.exception))

    def test_start_st_count_must_be_equal_to_stitch_length_if_no_increases(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p"), Stitch("k")])
        self.assertEqual(3, row.start_st_count)

    def test_start_st_count_must_be_less_than_stitch_length_if_increases(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("yo"), Stitch("k")])
        self.assertEqual(2, row.start_st_count)

    def test_start_st_count_must_be_more_than_stitch_length_if_decreases(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("ssk"), Stitch("k")])
        self.assertEqual(4, row.start_st_count)

    def test_end_st_count_increases_if_there_are_increasing_stitches(self):
        row = ExpandedRow(2, [Stitch("k"), Stitch("yo"), Stitch("k")])
        self.assertEqual(row.end_st_count, 3)

    def test_end_st_count_decreases_if_there_are_decreasing_stitches(self):
        row = ExpandedRow(2, [Stitch("k"), Stitch("ssk"), Stitch("k")])
        self.assertEqual(row.end_st_count, 3)

    def test_num_instructions_is_based_off_number_of_stitches(self):
        row_1 = ExpandedRow(1, [Stitch("k"), Stitch("ssk"), Stitch("k")])
        self.assertEqual(row_1.num_instructions, 3)
        row_2 = ExpandedRow(2, [Stitch("k"), Stitch("yo"), Stitch("k")])
        self.assertEqual(row_2.num_instructions, 3)

    def test_can_get_right_side_symbols_of_expandedrow(self):
        row = ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p"), Stitch("p")])
        expected = [" ", "-", "-"]
        self.assertEqual(expected, row.get_symbols_rs())

    def test_can_get_wrong_side_symbols_of_row(self):
        row = ExpandedRow(1, [Stitch("k"), Stitch("p"), Stitch("p")])
        expected = ["-", " ", " "]
        self.assertEqual(expected, row.get_symbols_ws())

class TestPattern(unittest.TestCase):
    def test_pattern_must_be_initialized_with_rows(self):
        Pattern(rows=[ExpandedRow(1, [Stitch("k")])])

        with self.assertRaises(TypeError) as err:
            Pattern()
        self.assertEqual("Pattern.__init__() missing 1 required positional argument: 'rows'", str(err.exception))

    def test_sorts_rows_by_number_on_initialization(self):
        row_1 = ExpandedRow(1, [Stitch("k"), Stitch("yo")])
        row_2 = ExpandedRow(2, [Stitch("k"), Stitch("p")])
        row_3 = ExpandedRow(3, [Stitch("ssk")])
        pattern = Pattern(rows=[row_2, row_3, row_1])

        expected = [row_1, row_2, row_3]
        actual = pattern.rows

        self.assertEqual(expected, actual)

    def test_row_numbers_must_be_unique(self):
        row_a = ExpandedRow(1, [Stitch("k")])
        row_b = row_a
        
        with self.assertRaises(ValueError) as err:
            Pattern([row_a, row_b])
        self.assertEqual("Row numbers must be unique", str(err.exception))

    def test_row_numbers_must_be_sequential(self):
        row_1 = ExpandedRow(1, [Stitch("k")])
        row_3 = ExpandedRow(3, [Stitch("k")])

        with self.assertRaises(ValueError) as err:
            Pattern([row_1, row_3])
        self.assertEqual("Row numbers must be sequential", str(err.exception))

    def test_row_lengths_must_be_congruent(self):
        with self.assertRaises(ValueError) as err:
            Pattern(rows=[
                ExpandedRow(1, [Stitch("k"), Stitch("p")]),
                ExpandedRow(2, [Stitch("p"), Stitch("k"), Stitch("p")])
            ])
        self.assertEqual(
            "Error on row 2. The start length of each row must be equal to the end length of the previous row",
            str(err.exception)
        )

    def test_can_get_row_by_number(self):
        pattern = Pattern(rows=[
            ExpandedRow(1, [Stitch("k")]),
            ExpandedRow(3, [Stitch("k"), Stitch("k")]),
            ExpandedRow(2, [Stitch("p"), Stitch("yo")])
        ])

        expected = ExpandedRow(2, [Stitch("p"), Stitch("yo")])
        actual = pattern.get_row(2)

        self.assertEqual(expected, actual)

    def test_can_get_max_length_of_pattern_of_regular_stitches(self):
        pattern = Pattern(rows=[
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k")]),
            ExpandedRow(2, [Stitch("p"), Stitch("p"), Stitch("p"), Stitch("p")]),
        ])

        expected = 4
        actual = pattern.get_max_length()

        self.assertEqual(expected, actual)

    def test_can_get_max_length_of_pattern_with_increases(self):
        pattern = Pattern(rows=[
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("k")]),
            ExpandedRow(2, [Stitch("p"), Stitch("yo"), Stitch("p"), Stitch("yo"), Stitch("p")]),
        ])

        expected = 5
        actual = pattern.get_max_length()

        self.assertEqual(expected, actual)

    def test_can_get_max_length_of_pattern_with_decreases(self):
        pattern = Pattern(rows=[
            ExpandedRow(1, [Stitch("k"), Stitch("k"), Stitch("k")]),
            ExpandedRow(2, [Stitch("p"), Stitch("ssk")]),
        ])

        expected = 3
        actual = pattern.get_max_length()

        self.assertEqual(expected, actual)

    def test_can_get_used_stitches_in_pattern(self):
        pattern = Pattern([
            ExpandedRow(1, [Stitch("k"), Stitch("p"), Stitch("yo"), Stitch("p"), Stitch("k")])
        ])

        expected = ["k", "p", "yo"]
        actual = pattern.get_stitches_used()

        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()