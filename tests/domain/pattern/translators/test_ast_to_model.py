import unittest
from src.domain.parser.ast.nodes import StitchNode, RepeatNode, RowNode, PartNode
from src.domain.pattern.translators.ast_to_model import ASTtoModelTranslator
from src.domain.pattern.entities.model import Stitch, Repeat, Row, Part

class ASTTranslatorTest(unittest.TestCase):
    def test_can_translate_stitch_node(self):
        translator = ASTtoModelTranslator()
        stitch_node = StitchNode("k")

        expected = Stitch("k")
        actual = translator.translate_stitch(stitch_node)

        self.assertEqual(expected, actual)

    def test_can_translate_repeat_node(self):
        translator = ASTtoModelTranslator()
        repeat_node = RepeatNode(elements=[StitchNode("k")])

        result = translator.translate_repeat(repeat_node)

        self.assertEqual(Repeat, type(result))

    def test_translating_repeat_node_translates_nodes_inside(self):
        translator = ASTtoModelTranslator()
        repeat_node = RepeatNode(elements=[StitchNode("k"), StitchNode("p")], num_times=4)

        expected = Repeat(elements=[Stitch("k"), Stitch("p")], num_times=4)
        actual = translator.translate_repeat(repeat_node)

        self.assertEqual(expected, actual)

    def test_can_translate_row_node(self):
        translator = ASTtoModelTranslator()
        row_node = RowNode(number=1, instructions=[StitchNode("k")])

        result = translator.translate_row(row_node)

        self.assertEqual(Row, type(result))

    def test_translating_row_node_translates_nodes_inside(self):
        translator = ASTtoModelTranslator()
        repeat_node = RepeatNode(elements=[StitchNode("k"), StitchNode("p"), StitchNode("k")])
        row_node = RowNode(number=1, instructions=[StitchNode("k"), repeat_node, StitchNode("k")])

        expected_repeat = Repeat(elements=[Stitch("k"), Stitch("p"), Stitch("k")])
        expected = Row(number=1, instructions=[Stitch("k"), expected_repeat, Stitch("k")])
        actual = translator.translate_row(row_node)

        self.assertEqual(expected, actual, f"Numbers were: {expected.number} vs {actual.number}. Rows were {expected.instructions} vs {actual.instructions}")

    def test_can_translate_part_node(self):
        translator = ASTtoModelTranslator()
        part_node = PartNode(caston=2, rows=[RowNode(1, [StitchNode("k"), StitchNode("k")])])

        result = translator.translate_part(part_node)

        self.assertEqual(Part, type(result))

    def test_translating_part_node_translates_nodes_inside(self):
        translator = ASTtoModelTranslator()
        part_node = PartNode(caston=2, rows=[RowNode(1, [StitchNode("k"), StitchNode("k")])])

        expected = Part(caston=2, rows=[Row(1, [Stitch("k"), Stitch("k")])])
        actual = translator.translate_part(part_node)

        self.assertEqual(expected, actual)

class TranslatorValidationTest(unittest.TestCase):
    def test_stitch_node_name_must_be_of_type_str(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_st_node = StitchNode(name=1)
            translator.translate_stitch(invalid_st_node)
        self.assertEqual("StitchNode name must be type str, got type <class 'int'>", str(err.exception))

    def test_repeat_node_elements_must_be_type_list(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_repeat_node = RepeatNode(elements="wrong")
            translator.translate_repeat(invalid_repeat_node)
        self.assertEqual("RepeatNode elements must be type list, got type <class 'str'>", str(err.exception))

    def test_each_repeat_node_element_must_be_type_stitchnode_or_repeatnode(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_repeat_node = RepeatNode(elements=["wrong"])
            translator.translate_repeat(invalid_repeat_node)
        self.assertEqual("All RepeatNode elements must be of type StitchNode or RepeatNode, got type <class 'str'>", str(err.exception))

    def test_repeat_node_elements_must_be_type_int_or_nonetype(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_repeat_node = RepeatNode(elements=[StitchNode("k")], num_times="wrong")
            translator.translate_repeat(invalid_repeat_node)
        self.assertEqual("RepeatNode num_times must be type int or None, got type <class 'str'>", str(err.exception))

    def test_row_node_number_must_be_type_int(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_repeat_node = RowNode(number="wrong", instructions=[StitchNode("k")])
            translator.translate_row(invalid_repeat_node)
        self.assertEqual("RowNode number must be type int, got type <class 'str'>", str(err.exception))

    def test_row_node_instructions_must_be_type_list(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_repeat_node = RowNode(number=1, instructions=(StitchNode("k"),))
            translator.translate_row(invalid_repeat_node)
        self.assertEqual("RowNode instructions must be type list, got type <class 'tuple'>", str(err.exception))

    def test_each_row_node_instruction_must_be_type_stitchnode_or_repeatnode(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_repeat_node = RowNode(number=1, instructions=[5])
            translator.translate_row(invalid_repeat_node)
        self.assertEqual("Items in RowNode instructions must be of type StitchNode or RepeatNode, got type <class 'int'>", str(err.exception))

    def test_part_node_caston_must_be_type_int(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_part_node = PartNode(caston="wrong", rows=[RowNode(1, [StitchNode("k")])])
            translator.translate_part(invalid_part_node)
        self.assertEqual("PartNode caston must be type int, got type <class 'str'>", str(err.exception))

    def test_part_node_rows_must_be_type_list(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_part_node = PartNode(caston=1, rows=(RowNode(number=1, instructions=[StitchNode("k")]),))
            translator.translate_part(invalid_part_node)
        self.assertEqual("PartNode rows must be type list, got type <class 'tuple'>", str(err.exception))

    def test_each_part_node_row_must_be_type_rownode(self):
        with self.assertRaises(TypeError) as err:
            translator = ASTtoModelTranslator()
            invalid_repeat_node = PartNode(caston=8, rows=[8])
            translator.translate_part(invalid_repeat_node)
        self.assertEqual("Items in PartNode rows must be of type RowNode, got type <class 'int'>", str(err.exception))

if __name__ == "__main__":
    unittest.main()