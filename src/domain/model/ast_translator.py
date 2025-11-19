from src.domain.ast.nodes import StitchNode, RepeatNode, RowNode, PartNode
from src.domain.model.model import Stitch, Repeat, Row, Part

class ASTtoModelTranslator:
    def _validate_stitch_node(self, node:StitchNode):
        if not isinstance(node.name, str):
            raise TypeError(f"StitchNode name must be type str, got type {type(node.name)}")
        
    def translate_stitch(self, node:StitchNode) -> Stitch:
        self._validate_stitch_node(node)

        return Stitch(abbrev=node.name)
    
    def _validate_repeat_node(self, node:RepeatNode):
        if not isinstance(node.elements, list):
            raise TypeError(f"RepeatNode elements must be type list, got type {type(node.elements)}")
        
        for element in node.elements:
            if not isinstance(element, (StitchNode, RepeatNode)):
                raise TypeError(f"All RepeatNode elements must be of type StitchNode or RepeatNode, got type {type(element)}")
        
        if not isinstance(node.num_times, (int, type(None))):
            raise TypeError(f"RepeatNode num_times must be type int or None, got type {type(node.num_times)}")

    def translate_repeat(self, node:RepeatNode) -> Repeat:
        self._validate_repeat_node(node)

        translated_elements = []
        for element in node.elements:
            if isinstance(element, StitchNode):
                translated_elements.append(self.translate_stitch(element))
            elif isinstance(element, RepeatNode):
                translated_elements.append(self.translate_repeat(element))

        return Repeat(elements=translated_elements, num_times=node.num_times)
    
    def _validate_row_node(self, node:RowNode):
        if not isinstance(node.number, int):
            raise TypeError(f"RowNode number must be type int, got type {type(node.number)}")
        
        if not isinstance(node.instructions, list):
            raise TypeError(f"RowNode instructions must be type list, got type {type(node.instructions)}")
        
        for instruction in node.instructions:
            if not isinstance(instruction, (StitchNode, RepeatNode)):
                raise TypeError(f"Items in RowNode instructions must be of type StitchNode or RepeatNode, got type {type(instruction)}")
        
    def translate_row(self, node:RowNode) -> Row:
        self._validate_row_node(node)

        translated_instructions = []
        for instruction in node.instructions:
            if isinstance(instruction, StitchNode):
                translated_instructions.append(self.translate_stitch(instruction))
            elif isinstance(instruction, RepeatNode):
                translated_instructions.append(self.translate_repeat(instruction))

        return Row(number=node.number, instructions=translated_instructions)

    def _validate_part_node(self, node:PartNode):
        if not isinstance(node.caston, int):
            raise TypeError(f"PartNode caston must be type int, got type {type(node.caston)}")
        
        if not isinstance(node.rows, list):
            raise TypeError(f"PartNode rows must be type list, got type {type(node.rows)}")
        
        for row in node.rows:
            if not isinstance(row, RowNode):
                raise TypeError(f"Items in PartNode rows must be of type RowNode, got type {type(row)}")

    def translate_part(self, node:PartNode) -> Part:
        self._validate_part_node(node)

        translated_rows = []
        for row in node.rows:
            translated_rows.append(self.translate_row(row))
        return Part(caston=node.caston, rows=translated_rows)
    
    # Entrypoint function
    def translate_ast(self, root_node:PartNode) -> Part:
        return self.translate_part(root_node)