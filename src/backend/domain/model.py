from dataclasses import dataclass
from enum import Enum
from typing import List, Union

class StitchType(Enum):
    REGULAR = "reg"
    INCREASE = "incr"
    DECREASE = "decr"

@dataclass(frozen=True)
class Stitch:
    abbrev: str

    def __post_init__(self):
        # error checking
        if not isinstance(self.abbrev, str):
            raise TypeError(f"Stitch abbrev must be type str, got type {type(self.abbrev)}")
    
    # The current dictionary of stitch abbreviations and their names and symbols
    STITCH_BY_ABBREV = {
        "k": {"name": "knit", "type": "reg", "stitches_consumed": 1, "rs": " ", "ws": "-"},
        "p": {"name": "purl", "type": "reg", "stitches_consumed": 1, "rs": "-", "ws": " "},
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
    def symbol_rs(self) -> str:
        return self.STITCH_BY_ABBREV[self.abbrev]["rs"]
    
    @property
    def symbol_ws(self) -> str:
        return self.STITCH_BY_ABBREV[self.abbrev]["ws"]

@dataclass
class Repeat:
    elements:List[Union[Stitch, "Repeat"]] # List[Union[a, "b"]] allows type-hints for class b in class b
    num_times:int=None
    stitches_after:int=0
    has_num_times = False   # placeholder for post_init

    def __post_init__(self):
        # error checking types
        if not isinstance(self.elements, list):
            raise TypeError(f"Repeat elements must be type list, got type {type(self.elements)}")
        if not all(isinstance(el, (Stitch, Repeat)) for el in self.elements):
            raise TypeError(f"Items in Repeat elements must be of type Stitch or Repeat")
        if not isinstance(self.stitches_after, int):
            raise TypeError(f"Repeat stitches_after must be type int, got type {type(self.stitches_after)}")

        # set the actual value of has_num_times
        self.has_num_times = True if self.num_times is not None else False

        # error checking for nesting
        for element in self.elements:
            if isinstance(element, Repeat): # one layer of nesting, ok
                for subelement in element.elements:
                    if isinstance(subelement, Repeat): # multiple layers of nesting, NOT ok
                        raise SyntaxError("Repeats cannot be nested more than once")

    def expand(self, remaining_stitches=0):
        if self.has_num_times:
            return self.elements * self.num_times
        
        if remaining_stitches != 0:
            repeat_length = remaining_stitches - self.stitches_after
            num_repeats:float = repeat_length / len(self.elements)

            if not num_repeats.is_integer():
                raise ValueError(f"The length of the repeat is {repeat_length}, which does not match with the number of elements in the repeat {len(self.elements)}")
            
            num_repeats = int(num_repeats)
            return self.elements * num_repeats
        
        raise ValueError("Not enough information to expand repeat")
        
class Row:
    def __init__(self, number:int, instructions:list[Stitch | Repeat]):
        # error checking types
        if not isinstance(number, int):
            raise TypeError(f"Row number must be type int, got type {type(number)}")
        if not isinstance(instructions, list):
            raise TypeError(f"Row instructions must be type int, got type {type(instructions)}")
        if not all(isinstance(instruction, (Stitch, Repeat)) for instruction in instructions):
            raise TypeError(f"Items in Row instructions must be of type Stitch or Repeat")
        
        self.number = number
        self.instructions = instructions

    def __eq__(self, other):
        if not isinstance(other, Row):
            return False
        
        if (self.number == other.number) and (self.instructions == other.instructions):
            return True
    
    def expand(self, prev_stitch_count:int):
        """Expand any Repeats in the Row and get the total count of stitches in the Row"""
        stitches = []
        count = 0
        prev_stitches_knitted = 0

        for instruction in self.instructions:
            if isinstance(instruction, Stitch):
                stitches.append(instruction)
                prev_stitches_knitted += instruction.stitches_consumed
                count += 1
            elif isinstance(instruction, Repeat):
                remaining_stitches = prev_stitch_count - prev_stitches_knitted
                expanded = instruction.expand(remaining_stitches)
                stitches.extend(expanded)
                
                for stitch in expanded:
                    prev_stitches_knitted += stitch.stitches_consumed

                count += len(expanded)

        expanded_row = Row(self.number, stitches)
        return (expanded_row, count)
    
class Part:
    def __init__(self, caston:int, rows:list[Row], name:str="main"):
        # error checking types
        if not isinstance(caston, int):
            raise TypeError(f"Part caston must be type int, got type {type(caston)}")
        if not isinstance(rows, list):
            raise TypeError(f"Part rows must be type list, got type {type(rows)}")
        if not all(isinstance(row, Row) for row in rows):
            raise TypeError(f"Items in Part rows must be of type Row")
        if not isinstance(name, str):
            raise TypeError(f"Part caston must be type str, got type {type(name)}")

        self.caston = caston
        self.rows = rows
        self.name = name

    @property
    def pattern(self):
        row_and_stitch_count:list[tuple[int, int]] = []

        for idx, row in enumerate(self.rows):
            if idx == 0:
                row_and_stitch_count.append((row, self.caston))
                continue
            
            prev_stitch_count:int = row_and_stitch_count[-1][1] # get the stitch_count previously appended
            expanded_row, stitch_count = row.expand(prev_stitch_count)

            row_and_stitch_count.append((expanded_row, stitch_count))
        
        return row_and_stitch_count
    
class Project:
    def __init__(self, name:str, parts:list[Part]):
        self.name = name
        self.parts = parts