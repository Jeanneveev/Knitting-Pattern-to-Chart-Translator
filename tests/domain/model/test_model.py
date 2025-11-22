import unittest
from src.domain.model.model import Stitch, Repeat, Row, Part, StitchType

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
            overnested = Repeat(elements=[Repeat(elements=[Repeat(elements=[Stitch("k")])])])
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

class TestPart(unittest.TestCase):
    def test_part_must_include_caston_num_and_rows(self):
        part = Part(caston=1, rows=[Row(1, [Stitch("p")])])

        with self.assertRaises(TypeError) as err:
            part_invalid = Part()
        self.assertEqual(str(err.exception), "Part.__init__() missing 2 required positional arguments: 'caston' and 'rows'")

# class TestProject(unittest.TestCase):
#     def test_projects_must_have_name_and_one_or_more_parts(self):
#         project = Project(name="test", parts=[Part(caston=1, rows=[Row(1, [Stitch("p")])])])

#         with self.assertRaises(TypeError) as err:
#             project_invalid = Project()
#         self.assertEqual("Project.__init__() missing 2 required positional arguments: 'name' and 'parts'", str(err.exception))

if __name__ == "__main__":
    unittest.main()