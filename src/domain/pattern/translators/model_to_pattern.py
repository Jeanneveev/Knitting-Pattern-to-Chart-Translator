from src.domain.pattern.entities.model import Stitch, Repeat, Row, Part
from src.domain.pattern.entities.pattern import ExpandedRow, Pattern

class ModelToPatternTranslator:
    """A wrapper around PatternBuilder to mimic the format of ASTtoModelTranslator"""
    def translate_model(self, model:Part) -> Pattern:
        return PatternBuilder(model).build_pattern()

class PatternBuilder:
    """Creates a Pattern object from a given Part object"""
    def __init__(self, part:Part):
        # Fix assumed caston, if necessary
        if part.assumed_caston == True:
            first_row = part.rows[0]
            stitch_count = sum(st.stitches_consumed for st in first_row.instructions)
            part.caston = stitch_count
            part.assumed_caston = False

        self.part = part

    def _validate_caston(self, caston:int, first_row:ExpandedRow):
        if caston != first_row.start_st_count:
            raise ValueError("First row does not contain as many stitches as caston")

    def build_pattern(self) -> Pattern:
        expanded_rows:list[ExpandedRow] = []
        for i, row in enumerate(self.part.rows):
            if i == 0:
                expanded_row = self.build_expanded_row(row, self.part.caston)
                self._validate_caston(self.part.caston, expanded_row)
                expanded_rows.append(expanded_row)
                continue

            prev_stitch_count:int = expanded_rows[-1].end_st_count
            expanded_row = self.build_expanded_row(row, prev_stitch_count)
            expanded_rows.append(expanded_row)

        return Pattern(expanded_rows)
    
    def build_expanded_row(self, row:Row, prev_st_count:int) -> ExpandedRow:
        expander = RowExpander(row, prev_st_count)
        
        return expander.expand()
    
class RowExpander:
    def __init__(self, row:Row, prev_row_st_count:int):
        # TODO: Add validation?
        self.row = row
        self.prev_row_st_count = prev_row_st_count

    def expand(self) -> ExpandedRow:
        """Expands any Repeats in the row into a flat list of Stitches and creates an ExpandedRow from it"""
        stitches = []
        prev_stitches_knitted = 0

        for instruction in self.row.instructions:
            if isinstance(instruction, Stitch):
                stitches.append(instruction)
                prev_stitches_knitted += instruction.stitches_consumed
            elif isinstance(instruction, Repeat):
                remaining_stitches = self.prev_row_st_count - prev_stitches_knitted
                expanded:list[Stitch] = self.expand_repeat(instruction, remaining_stitches)
                stitches.extend(expanded)
                
                for stitch in expanded:
                    prev_stitches_knitted += stitch.stitches_consumed

        expanded_row = Row(self.row.number, stitches)
        return ExpandedRow(expanded_row.number, expanded_row.instructions)
    
    def expand_repeat(self, repeat:Repeat, remaining_sts:int) -> list[Stitch]:
        """Expand a given Repeat of the row into a flat number of Stitches"""
        # Repeat repeats explicit number of times
        if repeat.has_num_times:
            return repeat.elements * repeat.num_times
        
        # Repeat repeats implicit number of times
        if repeat.stitches_after == None:   # hasn't been calculated yet
            self.resolve_implicit_repeat(self.row)

        if remaining_sts != 0:
            repeat_length = remaining_sts - repeat.stitches_after
            num_repeats:float = repeat_length / len(repeat.elements)

            if not num_repeats.is_integer():
                raise ValueError(f"The length of the repeat is {repeat_length}, which does not match with the number of elements in the repeat {len(repeat.elements)}")
            
            num_repeats = int(num_repeats)
            return repeat.elements * num_repeats
        
        raise ValueError("Not enough information to expand repeat")
    
    def resolve_implicit_repeat(self, row:Row) -> None:
        """
        Calculates the number of stitches after a Repeat object inside a given row with no specified number of repeats
        and modifies the "stitches_after" attribute of that Repeat in-place

        Handles the semantics of Repeats with no given number of repeats
        """
        
        instructions = row.instructions
        
        implicit_repeat = None
        implicit_repeat_idx = 0
        for idx, instruction in enumerate(instructions):
            if isinstance(instruction, Repeat):
                if instruction.has_num_times == False:
                    implicit_repeat = instruction
                    implicit_repeat_idx = idx
            
        if implicit_repeat == None: # there are no implicit repeats
            return

        instrs_after = instructions[implicit_repeat_idx + 1 :]
        stitches_after = 0
        for instr in instrs_after:
            if isinstance(instr, Stitch):
                stitches_after += instr.stitches_consumed
            if isinstance(instr, Repeat):   # has to be an explicit repeat
                stitches_after += (len(instr.elements) * instr.num_times)

        # modify Repeat
        implicit_repeat.stitches_after = stitches_after