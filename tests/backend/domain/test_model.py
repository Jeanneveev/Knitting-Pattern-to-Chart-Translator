import unittest
from src.backend.domain.model import Stitch, Repeat, Row, Part, StitchType, Project, Chart, resolve_implicit_repeat

class TestStitch(unittest.TestCase):
    def test_stitch_type_has_limited_values(self):
        stitch_types = ["reg", "incr", "decr"]
        for st in stitch_types:
            self.assertNotEqual(None, StitchType(st))
        
        invalid_type = "smth"
        with self.assertRaises(ValueError) as err:
            StitchType(invalid_type)
        self.assertEqual(f"'{invalid_type}' is not a valid StitchType", str(err.exception))

    def test_can_create_stitch_by_abbreviation(self):
        stitch = Stitch(abbrev="k")
        self.assertEqual("knit", stitch.name)

    def test_certain_stitches_have_set_values(self):
        stitch = Stitch(abbrev="k")
        self.assertEqual("knit", stitch.name)
        self.assertEqual(" ", stitch.symbol_rs)
        self.assertEqual(1, stitch.stitches_produced)

        stitch = Stitch(abbrev="p")
        self.assertEqual("purl", stitch.name)
        self.assertEqual("-", stitch.symbol_rs)
        self.assertEqual(1, stitch.stitches_produced)

class TestRepeat(unittest.TestCase):
    def test_setting_repeat_with_num_times_sets_has_num_times(self):
        repeat = Repeat(elements=[Stitch("k"), Stitch("p")], num_times=3)
        self.assertEqual(True, repeat.has_num_times)

    def test_setting_repeat_without_num_times_sets_has_num_times_to_false(self):
        repeat = Repeat(elements=[Stitch("k"), Stitch("p")])
        self.assertEqual(False, repeat.has_num_times)

    def test_repeats_cannot_be_nested_one_level(self):
        self.assertNotEqual(None, Repeat(elements=[Repeat(elements=[Stitch("k")])]))

    def test_repeats_cannot_be_nested_more_than_one_level(self):
        with self.assertRaises(SyntaxError) as err:
            overnested = Repeat(elements=[Repeat(elements=[Repeat(elements=[])])])
        self.assertEqual("Repeats cannot be nested more than once", str(err.exception))

class TestRow(unittest.TestCase):
    def test_rows_must_be_initialized_with_number_and_instructions(self):
        row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("k")])
        
        with self.assertRaises(TypeError) as err:
            row_invalid = Row(2)
        self.assertEqual("Row.__init__() missing 1 required positional argument: 'instructions'", str(err.exception))

    def test_rows_cannot_have_multiple_implicit_repeats(self):
        with self.assertRaises(SyntaxError) as err:
            row = Row(number=1, instructions=[
                Repeat([Stitch("p"), Stitch("k")]), Stitch("p"),
                Repeat([Stitch("k"), Stitch("p"), Stitch("k")])
            ])
        self.assertEqual("A row may only have one implicit repeat", str(err.exception))

    def test_rows_can_have_some_explicit_repeats_and_one_implicit_repeat(self):
        try:
            row = Row(number=1, instructions=[
                Repeat([Stitch("p"), Stitch("k")], num_times=2), Stitch("p"),
                Repeat([Stitch("p"), Stitch("k")], num_times=2), Stitch("p"),
                Repeat([Stitch("k"), Stitch("p"), Stitch("k")])
            ])
        except Exception as err:
            self.fail(f"An exception unexpectantly occured: {err}")

    def test_rows_implicit_repeat_must_be_last_repeat(self):
        with self.assertRaises(SyntaxError) as err:
            row = Row(number=1, instructions=[
                Repeat([Stitch("p"), Stitch("k")]), Stitch("p"),
                Repeat([Stitch("k"), Stitch("p"), Stitch("k")], num_times=2)
            ])
        self.assertEqual("An implicit repeat must be the last Repeat in the Row", str(err.exception))

    def test_can_expand_row_of_all_stitches(self):
        row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("k")])
        self.assertEqual(row, row.expand(prev_row_st_count=3))

    def test_can_expand_row_with_some_explicit_repeats(self):
        row = Row(number=1, instructions=[Stitch("k"), Repeat([Stitch("p"), Stitch("k")], num_times=2)])
        expected_row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k")])
        self.assertEqual(expected_row, row.expand(prev_row_st_count=5))

    def test_can_expand_row_with_a_implicit_repeat(self):
        row = Row(number=1, instructions=[Stitch("k"), Repeat([Stitch("p"), Stitch("k")]), Stitch("k")])
        expected_row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("k")])
        self.assertEqual(expected_row, row.expand(6))

    def test_can_get_right_side_symbols_of_row(self):
        row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("p")])
        expected = [" ", "-", "-"]
        self.assertEqual(expected, row.get_symbols_rs())

    def test_cannot_get_right_side_symbols_of_row_with_repeats(self):
        row = Row(number=1, instructions=[Repeat([Stitch("k"), Stitch("p")], 2), Stitch("p")])
        
        with self.assertRaises(ValueError) as err:
            row.get_symbols_rs()
        self.assertEqual("Cannot get symbols of rows with Repeats", str(err.exception))

    def test_can_get_wrong_side_symbols_of_row(self):
        row = Row(number=1, instructions=[Stitch("k"), Stitch("p"), Stitch("p")])
        expected = ["-", " ", " "]
        self.assertEqual(expected, row.get_symbols_ws())

    def test_cannot_get_wrong_side_symbols_of_row_with_repeats(self):
        row = Row(number=1, instructions=[Repeat([Stitch("k"), Stitch("p")], 2), Stitch("p")])
        
        with self.assertRaises(ValueError) as err:
            row.get_symbols_ws()
        self.assertEqual("Cannot get symbols of rows with Repeats", str(err.exception))

class TestComputeStitchesAfter(unittest.TestCase):
    def test_can_insert_stitches_after_into_row_repeat(self):
        row = Row(number=1, instructions=[
            Stitch("k"), Repeat([Stitch("p"), Stitch("k")], num_times=2), Stitch("k"),
            Repeat([Stitch("p"), Stitch("k")]), Stitch("k"), Stitch("k")
        ])
        
        resolve_implicit_repeat(row)

        self.assertEqual(2, row.instructions[3].stitches_after)

class TestPart(unittest.TestCase):
    def test_part_must_include_caston_num_and_rows(self):
        part = Part(caston=1, rows=[Row(1, [Stitch("p")])])

        with self.assertRaises(TypeError) as err:
            part_invalid = Part()
        self.assertEqual(str(err.exception), "Part.__init__() missing 2 required positional arguments: 'caston' and 'rows'")

    def test_part_pattern_includes_row_and_row_stitch_count(self):
        row_1 = Row(1, [Stitch("p"), Stitch("k"), Stitch("p")])
        row_2 = Row(2, [Stitch("k"), Stitch("p"), Stitch("k")])
        part = Part(caston=3, rows=[row_1, row_2])
        
        self.assertEqual([(row_1, 3), (row_2, 3)], part.pattern)

    def test_can_get_stitch_count_of_flat_row(self):
        row = Row(1, [Stitch("k"), Stitch("k"), Stitch("k"), Stitch("k")])
        part = Part(caston=4, rows=[row])

        self.assertEqual(4, part.get_row_stitch_count(row, 4))
    
    def test_can_get_stitch_count_of_row_with_repeats(self):
        row = Row(1, [Repeat([Stitch("p"), Stitch("k")], 2)])
        part = Part(caston=4, rows=[row])

        self.assertEqual(4, part.get_row_stitch_count(row, 4))

    def test_can_get_stitch_count_of_row_with_increases(self):
        row = Row(1, [Stitch("k"), Stitch("p"), Stitch("yo"), Stitch("p"), Stitch("k")])
        part = Part(4, rows=[row])

        self.assertEqual(5, part.get_row_stitch_count(row, 4))

    def test_can_get_stitch_count_of_row_with_decreases(self):
        row = Row(1, [Stitch("k"), Stitch("p"), Stitch("ssk"), Stitch("p"), Stitch("k")])
        part = Part(caston=6, rows=[row])

        self.assertEqual(5, part.get_row_stitch_count(row, 6))

    def test_can_get_row_by_number(self):
        row_1 = Row(1, [Stitch("k"), Stitch("p"), Stitch("k")])
        row_2 = Row(2, [Stitch("p"), Stitch("k"), Stitch("p")])
        part = Part(3, [row_1, row_2])
        
        self.assertEqual(Row(2, [Stitch("p"), Stitch("k"), Stitch("p")]), part.get_row(2))

    def test_can_get_expanded_row_by_number(self):
        row_1 = Row(1, [Repeat([Stitch("k"), Stitch("p")])])
        row_2 = Row(2, [Repeat([Stitch("p"), Stitch("k")])])
        part = Part(6, [row_1, row_2])

        expected = Row(1, [Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p")])
        actual = part.get_row(1)
        self.assertEqual(expected, actual, f"got Row({actual.instructions})")

    def test_can_get_length_of_longest_row_in_pattern(self):
        part = Part(4, [
            Row(1, [Stitch("k"), Stitch("yo"), Stitch("p"), Stitch("p"), Stitch("yo"), Stitch("k")]), # 6
            Row(2, [Stitch("k"), Stitch("yo"), Repeat([Stitch("p")]), Stitch("yo"), Stitch("k")]), # 8
        ])
        # print(part.pattern)
        
        self.assertEqual(8, part.get_max_length())


class TestChart(unittest.TestCase):
    def test_can_get_symbols_of_right_side_row(self):
        row = Row(1, [Stitch("k"), Stitch("p"), Stitch("k"), Stitch("p")])
        part = Part(4, [row])
        chart = Chart(part)

        expected = {1: ["-", " ", "-", " "]}
        actual = chart.get_row_symbols(1)

        self.assertEqual(expected, actual)
    
    def test_can_get_symbols_of_wrong_side_row(self):
        row_1 = Row(1, [Stitch("k"), Stitch("yo"), Stitch("k")])
        row_2 = Row(2, [Stitch("k"), Stitch("k2tog"), Stitch("k")])
        part = Part(4, [row_1, row_2])
        chart = Chart(part)

        expected = {2: ["-", "/", "-"]}
        actual = chart.get_row_symbols(2)

        self.assertEqual(expected, actual)
    

class TestProject(unittest.TestCase):
    def test_projects_must_have_name_and_one_or_more_parts(self):
        project = Project(name="test", parts=[Part(caston=1, rows=[Row(1, [Stitch("p")])])])

        with self.assertRaises(TypeError) as err:
            project_invalid = Project()
        self.assertEqual("Project.__init__() missing 2 required positional arguments: 'name' and 'parts'", str(err.exception))

if __name__ == "__main__":
    unittest.main()