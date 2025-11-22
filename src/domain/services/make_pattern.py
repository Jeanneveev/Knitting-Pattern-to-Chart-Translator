"""Contains the logic necessary in turning a Part with rows of repeat into a Pattern with rows of stitches
Plus other functions for getting/calculating Pattern-relevant info
"""

from ordered_set import OrderedSet
from src.domain.model.model import Stitch, Repeat, Row, Part

class ExpandedRow:
    def __init__(self, number:int, stitches:list[Stitch], start_st_count: int):
        if len(stitches) == 0:
            raise ValueError("ExpandedRow must contain at least one instruction")
        
        if start_st_count < 1:
            raise ValueError("There must be at least one stitch at the start of the row")
        
        count = 0
        for stitch in stitches:
            count += stitch.stitches_consumed
        if count != start_st_count:
            raise ValueError((
                f"Start_st_count is incorrect, {start_st_count} was given "
                f"when it should be {count}"
            ))
                
        self.number = number
        self.stitches = stitches
        self.start_st_count = start_st_count

    def __eq__(self, other):
        if not isinstance(other, ExpandedRow):
            return False
        
        if ((self.number == other.number) and
            (self.stitches == other.stitches) and
            (self.start_st_count == other.start_st_count)
        ):
            return True
        
        return False
    
    @property
    def end_st_count(self):
        end_st_count = self.start_st_count
        for stitch in self.stitches:
            end_st_count += stitch.stitches_produced - stitch.stitches_consumed
        
        return end_st_count

    def get_symbols_rs(self) -> list[str]:
        """Return the right-side symbols of each stitch in the row"""
        return [stitch.symbol_rs for stitch in self.stitches]
        
    def get_symbols_ws(self) -> list[str]:
        """Return the wrong-side symbols of each stitch in the row"""
        return [stitch.symbol_ws for stitch in self.stitches]

class Pattern:
    def __init__(self, rows:list[ExpandedRow]):
        if len(rows) == 0:
            raise ValueError("Pattern must contain at least one row")
        
        # sort rows by number if not already
        rows = sorted(rows, key=lambda x: x.number)

        # row validation
        for idx, row in enumerate(rows):
            if idx == 0:
                continue

            prev_row = rows[idx-1]
            # confirm row numbers are unique and sequential
            if row.number == prev_row.number:
                raise ValueError("Row numbers must be unique")
            if row.number != prev_row.number+1:
                raise ValueError("Row numbers must be sequential")

            # confirm start length of each row is the same as the end length of the previous
            ## leaving it to ExpandedRow to confirm start and end length is right internally
            prev_end = prev_row.end_st_count
            curr_start = row.start_st_count
            if prev_end != curr_start:
                raise ValueError((
                    f"Error on row {row.number}. "
                    "The start length of each row must be equal to the end length of the previous row"
                ))

        self.rows = rows
    
    def __eq__(self, other):
        if not isinstance(other, Pattern):
            return False
        
        if self.rows == other.rows:
            return True
        
        return False

    def get_row(self, num) -> Row:
        return next((row for row in self.rows if row.number == num))
    
    def get_max_length(self) -> int:
        """Get the length of the longest row in the pattern"""
        max_len = 0
        for row in self.rows:
            max_len = max(max_len, row.end_st_count)

        return max_len

    def get_stitches_used(self) -> list[str]:
        """Get the abbreviations of all stitches used in the pattern"""
        used = OrderedSet()

        for row in self.rows:
            for stitch in row.stitches:
                used.add(stitch.abbrev)

        return list(used)


class PatternBuilder:
    """Contains all the functions needed to build a Pattern out of a Part"""
    def __init__(self, part:Part):
        self.part = part
    
    def build_pattern(self) -> Pattern:
        expanded_rows:list[ExpandedRow] = []
        for i, row in enumerate(self.part.rows):
            if i == 0:
                expanded_row = self.build_expanded_row(row, self.part.caston)
                expanded_rows.append(expanded_row)
                continue

            prev_stitch_count:int = expanded_rows[-1].end_st_count
            expanded_row = self.build_expanded_row(row, prev_stitch_count)
            expanded_rows.append(expanded_row)

        return Pattern(expanded_rows)
    
    def build_expanded_row(self, row:Row, prev_st_count:int) -> ExpandedRow:
        number = row.number
        flattened = self.expand_row(row, prev_st_count)
        stitches = flattened.instructions
        
        return ExpandedRow(number, stitches, prev_st_count)
    
    def expand_row(self, row:Row, prev_row_st_count:int):
        """Expand any Repeats in a given Row into a flat list of Stitches"""
        stitches = []
        prev_stitches_knitted = 0

        for instruction in row.instructions:
            if isinstance(instruction, Stitch):
                stitches.append(instruction)
                prev_stitches_knitted += instruction.stitches_consumed
            elif isinstance(instruction, Repeat):
                remaining_stitches = prev_row_st_count - prev_stitches_knitted
                expanded:list[Stitch] = self.expand_repeat(row, instruction, remaining_stitches)
                stitches.extend(expanded)
                
                for stitch in expanded:
                    prev_stitches_knitted += stitch.stitches_consumed

        expanded_row = Row(row.number, stitches)
        return expanded_row

    def expand_repeat(self, row:Row, repeat:Repeat, remaining_sts:int) -> list[Stitch]:
        """Expand a given Repeat of a given Row into a flat number of Stitches"""
        # Repeat repeats explicit number of times
        if repeat.has_num_times:
            return repeat.elements * repeat.num_times
        
        # Repeat repeats implicit number of times
        if repeat.stitches_after == None:   # hasn't been calculated yet
            self.resolve_implicit_repeat(row)

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
        # print(f"stitches after are {stitches_after}")
        implicit_repeat.stitches_after = stitches_after