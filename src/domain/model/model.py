from dataclasses import dataclass
from enum import Enum
from ordered_set import OrderedSet
from typing import List, Union

class StitchType(Enum):
    REGULAR = "reg"
    INCREASE = "incr"
    DECREASE = "decr"

@dataclass(frozen=True)
class Stitch:
    abbrev: str
    
    # The current dictionary of stitch abbreviations and their names and symbols
    STITCH_BY_ABBREV = {
        "k":    {"name": "knit",            "type": "reg",  "stitches_consumed": 1, "stitches_produced": 1,  "rs": " ", "ws": "-"},
        "p":    {"name": "purl",            "type": "reg",  "stitches_consumed": 1, "stitches_produced": 1,  "rs": "-", "ws": " "},
        "yo":   {"name": "yarn over",       "type": "incr", "stitches_consumed": 0, "stitches_produced": 1,  "rs": "O", "ws": "O"},
        "k2tog":{"name": "knit 2 together", "type": "decr", "stitches_consumed": 2, "stitches_produced": 1, "rs": "/", "ws": "/"},
        "ssk":  {"name": "slip slip knit",  "type": "decr", "stitches_consumed": 2, "stitches_produced": 1, "rs": "\\", "ws": "\\"},
    }

    @property
    def name(self) -> str:
        return self.STITCH_BY_ABBREV[self.abbrev]["name"]
    
    @property
    def type(self) -> StitchType:
        return StitchType(self.STITCH_BY_ABBREV[self.abbrev]["type"])
    
    @property
    def stitches_consumed(self) -> int:
        return self.STITCH_BY_ABBREV[self.abbrev]["stitches_consumed"]

    @property
    def stitches_produced(self) -> int:
        return self.STITCH_BY_ABBREV[self.abbrev]["stitches_produced"]

    @property
    def symbol_rs(self) -> str:
        return self.STITCH_BY_ABBREV[self.abbrev]["rs"]
    
    @property
    def symbol_ws(self) -> str:
        return self.STITCH_BY_ABBREV[self.abbrev]["ws"]

@dataclass
class Repeat:
    elements:List[Union[Stitch, "Repeat"]] # List[Union[a, "b"]] allows type-hints for class b in class b
    num_times:int = None
    stitches_after:int = None
    has_num_times = False   # placeholder for post_init

    def __post_init__(self):
        # set the actual value of has_num_times
        self.has_num_times = True if self.num_times is not None else False

        # error checking for nesting
        for element in self.elements:
            if isinstance(element, Repeat): # one layer of nesting, ok
                for subelement in element.elements:
                    if isinstance(subelement, Repeat): # multiple layers of nesting, NOT ok
                        raise SyntaxError("Repeats cannot be nested more than once")

    def __eq__(self, other):
        if not isinstance(other, Repeat):
            return False
        
        if (self.elements == other.elements) and (self.num_times == other.num_times) and (self.stitches_after == other.stitches_after):
            return True
        return False

class Row:
    def __init__(self, number:int, instructions:list[Stitch | Repeat]):
        # Check that, if there is an implicit repeat in the row, it is the last one
        repeats = [instruction for instruction in instructions if isinstance(instruction, Repeat)]
        if len(repeats) != 0:
            implicit_repeats = [repeat for repeat in repeats if repeat.has_num_times == False]
            
            if len(implicit_repeats) > 1:
                raise SyntaxError("A row may only have one implicit repeat")
            
            if len(implicit_repeats) != 0:
                implicit_repeat = implicit_repeats[0]
                if implicit_repeat != repeats[-1]:
                    raise SyntaxError("An implicit repeat must be the last Repeat in the Row")
        
        self.number = number
        self.instructions = instructions

    def __eq__(self, other):
        if not isinstance(other, Row):
            return False
        
        if (self.number == other.number) and (self.instructions == other.instructions):
            return True
    
    def expand(self, prev_row_st_count:int):
        """Expand any Repeats in the Row and get the total count of stitches in the Row"""
        stitches = []
        prev_stitches_knitted = 0

        for instruction in self.instructions:
            if isinstance(instruction, Stitch):
                stitches.append(instruction)
                prev_stitches_knitted += instruction.stitches_consumed
            elif isinstance(instruction, Repeat):
                remaining_stitches = prev_row_st_count - prev_stitches_knitted
                expanded:list[Stitch] = self._expand_repeat(instruction, remaining_stitches)
                stitches.extend(expanded)
                
                for stitch in expanded:
                    prev_stitches_knitted += stitch.stitches_consumed

        expanded_row = Row(self.number, stitches)
        return expanded_row
    
    def _expand_repeat(self, repeat:Repeat, remaining_sts:int):
        # Repeat repeats explicit number of times
        if repeat.has_num_times:
            return repeat.elements * repeat.num_times
        
        # Repeat repeats implicit number of times
        if repeat.stitches_after == None:   # hasn't been calculated yet
            resolve_implicit_repeat(self)

        if remaining_sts != 0:
            repeat_length = remaining_sts - repeat.stitches_after
            num_repeats:float = repeat_length / len(repeat.elements)

            if not num_repeats.is_integer():
                raise ValueError(f"The length of the repeat is {repeat_length}, which does not match with the number of elements in the repeat {len(repeat.elements)}")
            
            num_repeats = int(num_repeats)
            return repeat.elements * num_repeats
        
        raise ValueError("Not enough information to expand repeat")
    
    def get_symbols_rs(self) -> list[str]:
        """Return the right-side symbols of the row if it has no Repeats"""
        if any(isinstance(instruction, Repeat) for instruction in self.instructions):
            raise ValueError("Cannot get symbols of rows with Repeats")
        
        return [stitch.symbol_rs for stitch in self.instructions]
        
    def get_symbols_ws(self) -> list[str]:
        """Return the wrong-side symbols of the row if it has no Repeats"""
        if any(isinstance(instruction, Repeat) for instruction in self.instructions):
            raise ValueError("Cannot get symbols of rows with Repeats")
        
        return [stitch.symbol_ws for stitch in self.instructions]
        


def resolve_implicit_repeat(row:Row) -> None:
    """
    Calculates the number of stitches after a Repeat object inside a given row with no specified number of repeats
    and modifies the "stitches_after" attribute of that Repeat in-place

    Handles the semantics of Repeats with no given number of repeats
    """
    
    instructions = row.instructions
    idxs = [i for i, instruction in enumerate(instructions) if isinstance(instruction, Repeat)]
    
    if len(idxs) == 0:  # There are no implicit repeats
        return

    idx = idxs[-1]  # An implicit Repeat, if it exists, is always the last Repeat
    
    repeat = instructions[idx]
    if repeat.has_num_times:    # Last repeat is explicit, there are no implicit repeats
        return

    instrs_after = instructions[idx + 1 :]
    stitches_after = sum(instr.stitches_consumed for instr in instrs_after if isinstance(instr, Stitch))

    # modify Repeat
    # print(f"stitches after are {stitches_after}")
    repeat.stitches_after = stitches_after
    
class Part:
    def __init__(self, caston:int, rows:list[Row], name:str="main"):
        # error checking types
        if not isinstance(name, str):
            raise TypeError(f"Part name must be type str, got type {type(name)}")

        self.caston = caston
        self.rows = rows
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, Part):
            return False
        
        if (self.caston == other.caston) and (self.rows == other.rows) and (self.name == other.name):
            return True
        return False
    
    def get_row_stitch_count(self, row:Row, prev_row_st_count:int) -> int:
        """Get the stitch count of a row"""
        if any(isinstance(instruction, Repeat) for instruction in row.instructions):
            row = row.expand(prev_row_st_count)

        count = 0
        for stitch in row.instructions:
            count += stitch.stitches_produced

        return count

    @property
    def pattern(self) -> list[tuple[Row, int]]:
        """Creates a list of tuples of expanded Rows and their stitch counts"""
        row_and_stitch_count:list[tuple[Row, int]] = []

        for idx, row in enumerate(self.rows):
            if idx == 0:
                expanded_row = row.expand(self.caston)
                stitch_count = self.get_row_stitch_count(expanded_row, self.caston)
                row_and_stitch_count.append((expanded_row, stitch_count))
                continue
            
            prev_stitch_count:int = row_and_stitch_count[-1][1] # get the stitch_count previously appended
            expanded_row = row.expand(prev_stitch_count)
            stitch_count = self.get_row_stitch_count(expanded_row, prev_stitch_count)

            row_and_stitch_count.append((expanded_row, stitch_count))
        
        return row_and_stitch_count
            
    def get_row(self, num) -> Row:
        """Get the expanded version of a row of the pattern by its row number"""
        return self.pattern[num-1][0]
    
    def get_max_length(self) -> int:
        """Get the length of the longest row in the pattern"""
        max_len = 0
        for row, count in self.pattern:
            max_len = max(max_len, count)
        return max_len
    
    @property
    def stitches_used(self) -> list[str]:
        used = OrderedSet()

        for row in self.rows:
            for instruction in row.instructions:
                if isinstance(instruction, Stitch):
                    used.add(instruction.abbrev)
                if isinstance(instruction, Repeat):
                    for element in instruction.elements:
                        if isinstance(element, Stitch):
                            used.add(element.abbrev)
                        if isinstance(element, Repeat): # nested Repeat, has to have all Stitches
                            for el in element.elements:
                                used.add(el.abbrev)
        
        return list(used)

    
@dataclass
class Chart:
    pattern:Part

    def get_row_symbols(self, n:int) -> dict:
        """Display a row of a pattern using the stitches' symbols.
        Note that odd rows are on the right side and use rs symbols while even rows are on
        the wrong side and use ws symbols.
        """
        if n%2==1:  #right-side, display in reverse
            # print("right-side")
            row = self.pattern.get_row(n)
            symbols = row.get_symbols_rs()
            symbols.reverse()
            return {n: symbols}
        else:   #wrong-side, display normally
            # print("wrong-side")
            row = self.pattern.get_row(n)
            symbols = row.get_symbols_ws()
            return {n: symbols}
        
    def _build_border(self, length:int) -> str:
        border = "---+---"
        for _ in range(length):
            border += "+---"

        return border
    
    def _build_row(self, row_num:int) -> str:
        result = "|"
        symbols = self.get_row_symbols(row_num)[row_num]
        
        for symbol in symbols:
            result += f" {symbol} |"

        if row_num % 2 == 1:    #right-side, display in reverse
            # print("right-side")
            result = "   " + result + f" {row_num} "
        else:               #wrong-side, display normally
            # print("wrong-side")
            result = f" {row_num} " + result + "   "

        return result

    def render_grid(self) -> str:
        pattern = self.pattern.pattern
        last_row = pattern[-1][0]

        max_length = self.pattern.get_max_length()
        border = self._build_border(max_length)
        
        inner_rows = []
        for row, _ in pattern:
            inner_rows.append(self._build_row(row.number) + "\n")
            if row != last_row:    # add a horizontal line after all rows except the last one
                inner_rows.append(border + "\n")
        inner_rows.reverse()

        inner = ""
        for row in inner_rows:
            inner += row

        grid = border + "\n" + inner + border
        # print(f"grid is:\n {grid}")
        return grid
    
    def _get_column_width(self, contents:list[str]) -> int:
        """Get the width (length) of the longest string in the column, +2 for padding"""
        max_width = 0
        for string in contents:
            max_width = max(max_width, len(string))

        return max_width + 2
    
    def _get_padded_column(self, column_contents, column_width) -> list[str]:
        padded_contents = []
        for content in column_contents:
            text_width = len(content)
            if (column_width - text_width) % 2 == 0:
                space_width = int((column_width - text_width) / 2)
                padding = " " * space_width
                padded_contents.append(padding + content + padding) 
            else:
                space_width = int((column_width - text_width - 1) / 2)
                padding_left = " " * (space_width + 1)
                padding_right = " " * space_width
                padded_contents.append(padding_left + content + padding_right)

        return padded_contents
    
    def render_key(self) -> str:
        key = ""
        names = []
        right_sides = []
        wrong_sides = []
        abbreviations = self.pattern.stitches_used
        for stitch in abbreviations:
            stitch_info = Stitch.STITCH_BY_ABBREV[stitch]
            names.append(stitch_info.get("name").title())
            right_sides.append(stitch_info.get("rs"))
            wrong_sides.append(stitch_info.get("ws"))
        
        names.insert(0, "Name")
        abbreviations.insert(0, "Abbrev")
        right_sides.insert(0, "RS Symbol")
        wrong_sides.insert(0, "WS Symbol")
        
        name_col_width = self._get_column_width(names)
        abbrev_col_width = self._get_column_width(abbreviations)
        rs_col_width = self._get_column_width(right_sides)
        ws_col_width = self._get_column_width(wrong_sides)

        names_padded = self._get_padded_column(names, name_col_width)
        abbrev_padded = self._get_padded_column(abbreviations, abbrev_col_width)
        rs_padded = self._get_padded_column(right_sides, rs_col_width)
        ws_padded = self._get_padded_column(wrong_sides, ws_col_width)

        border = (
            "+" + ("-" * name_col_width) +
            "+" + ("-" * abbrev_col_width) +
            "+" + ("-" * rs_col_width) +
            "+" + ("-" * ws_col_width) +
            "+" + "\n"
        )

        key += border
        for idx in range(len(abbreviations)):
            key += (
                "|" + names_padded[idx] +
                "|" + abbrev_padded[idx] +
                "|" + rs_padded[idx] +
                "|" + ws_padded[idx] +
                "|" + "\n"
            )
            key += border

        return key
        

class Project:
    def __init__(self, name:str, parts:list[Part]):
        self.name = name
        self.parts = parts