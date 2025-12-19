"""Holds semantic logic and constant attribute value checking for the entities of and related to Patterns"""

from ordered_set import OrderedSet
from src.domain.pattern.entities.model import Stitch, Repeat, Row, Part

class ExpandedRow:
    def __init__(self, number:int, stitches:list[Stitch]):
        if len(stitches) == 0:
            raise ValueError("ExpandedRow must contain at least one instruction")
                
        self.number = number
        self.stitches = stitches
        self.num_instructions = len(stitches)

    def __eq__(self, other):
        if not isinstance(other, ExpandedRow):
            return False
        
        if ((self.number == other.number) and (self.stitches == other.stitches)):
            return True
        
        return False
    
    @property
    def start_st_count(self):
        st_count = 0
        for stitch in self.stitches:
            st_count += stitch.stitches_consumed
        return st_count

    @property
    def end_st_count(self):
        end_st_count = self.start_st_count
        for stitch in self.stitches:
            end_st_count += stitch.stitches_produced - stitch.stitches_consumed
        
        return end_st_count
    
    @property
    def is_rs(self):
        return self.number % 2 == 1
    
    @property
    def is_ws(self):
        return self.number % 2 == 0

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

    def get_row(self, num) -> ExpandedRow:
        return next((row for row in self.rows if row.number == num))
    
    def get_max_length(self) -> int:
        """Get the length of the longest row in the pattern"""
        # return max(self.get_max_start_length(), self.get_max_end_length())
        max_len = 0
        for row in self.rows:
            max_len = max(max_len, row.num_instructions)
        return max_len

    def get_stitches_used(self) -> list[str]:
        """Get the abbreviations of all stitches used in the pattern"""
        used = OrderedSet()

        for row in self.rows:
            for stitch in row.stitches:
                used.add(stitch.abbrev)

        return list(used)
    
    def get_symbols_used(self) -> list[str]:
        """Get the symbols of all stitches used in the pattern"""
        used = OrderedSet()

        for row in self.rows:
            for stitch in row.stitches:
                used.add(stitch.symbol_rs if row.number % 2 == 1 else stitch.symbol_ws)
        
        return list(used)