import unittest
from src.domain.pattern.entities import Stitch, Repeat, Row, Part, ExpandedRow, Pattern
from src.domain.pattern.translators.model_to_pattern import RowExpander, PatternBuilder

class TestBuildExpandedRow(unittest.TestCase):
    def test_can_compute_stitches_after_implicit_repeat_with_only_stitches_after(self):
        row = Row(number=1, instructions=[
            Stitch("k"), Repeat([Stitch("p"), Stitch("k")], num_times=2), Stitch("k"),
            Repeat([Stitch("p"), Stitch("k")]), Stitch("k"), Stitch("k")
        ])
        builder = RowExpander(row, 6)
        
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
        builder = RowExpander(row, 12)

        builder.resolve_implicit_repeat(row)

        expected = 5
        actual = row.instructions[1].stitches_after

        self.assertEqual(expected, actual)

    def test_can_expand_row_of_all_stitches(self):
        row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("k")])
        builder = RowExpander(row, 3)

        expected = ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p"), Stitch("k")])
        actual = builder.expand()

        self.assertEqual(expected, actual)

    def test_can_expand_row_with_some_explicit_repeats(self):
        row = Row(number=1, instructions=[Stitch("k"), Repeat([Stitch("p"), Stitch("k")], num_times=2)])
        builder = RowExpander(row, 5)

        expected = ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k")])
        actual = builder.expand()

        self.assertEqual(expected, actual)

    def test_can_expand_row_with_a_implicit_repeat(self):
        row = Row(number=1, instructions=[Stitch("k"), Repeat([Stitch("p"), Stitch("k")]), Stitch("k")])
        part = Part(6, [row])
        builder = PatternBuilder(part)

        expected = ExpandedRow(number=1, stitches=[Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("k")])
        actual = builder.build_expanded_row(row, part.caston)

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
            ])
        ])
        actual = builder.build_pattern()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()