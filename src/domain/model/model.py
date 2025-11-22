"""Holds semantic logic and constant attribute value checking"""

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
        if self.abbrev == "":
            raise ValueError("Stitch abbreviation must be a non-empty string")
    
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

class Repeat:
    def __init__(self, elements:List[Union[Stitch, "Repeat"]], num_times:int = None, stitches_after:int = None):
        if len(elements) == 0:
            raise ValueError("Repeat must contain at least one element")
    
        if num_times is not None and num_times < 1:
            raise ValueError("num_times must be >= 1")
        
        for element in elements:
            if isinstance(element, Repeat): # one layer of nesting, ok
                for subelement in element.elements:
                    if isinstance(subelement, Repeat): # multiple layers of nesting, NOT ok
                        raise SyntaxError("Repeats cannot be nested more than once")
                    
        self.elements = elements
        self.num_times = num_times
        self.has_num_times = True if self.num_times is not None else False
        self.stitches_after:int = None

    def __eq__(self, other):
        if not isinstance(other, Repeat):
            return False
        
        if (self.elements == other.elements) and (self.num_times == other.num_times) and (self.stitches_after == other.stitches_after):
            return True
        return False

class Row:
    def __init__(self, number:int, instructions:list[Stitch | Repeat]):
        if number < 0:
            raise ValueError("Row number must be a positive integer")
        
        if len(instructions) == 0:
            raise ValueError("Row must have at least one instruction")

        # Check that, if there is an implicit repeat in the row, it is the last one
        repeats = [instruction for instruction in instructions if isinstance(instruction, Repeat)]
        if len(repeats) != 0:
            implicit_repeats = [repeat for repeat in repeats if repeat.has_num_times == False]
            
            if len(implicit_repeats) > 1:
                raise SyntaxError("A row may only have one implicit repeat")
        
        self.number = number
        self.instructions = instructions

    def __eq__(self, other):
        if not isinstance(other, Row):
            return False
        
        if (self.number == other.number) and (self.instructions == other.instructions):
            return True
    
class Part:
    def __init__(self, caston:int, rows:list[Row]):
        if caston < 1:
            raise ValueError("Caston number must be at least 1")
        
        # Row numbers must be unique and sequential
        row_numbers:list[int] = []
        for i, row in enumerate(rows):
            if i == 0:
                row_numbers.append(row.number)
                continue
            
            prev_row_num = row_numbers[-1]
            if row.number != prev_row_num + 1:
                raise ValueError((
                    f"Row numbers must be unique and sequential."
                    f"Row number {i-1} is {prev_row_num} and row number {i} is {row.number}"
                ))

        self.caston = caston
        self.rows = rows

    def __eq__(self, other):
        if not isinstance(other, Part):
            return False
        
        if (self.caston == other.caston) and (self.rows == other.rows):
            return True
        return False

# class Project:
#     def __init__(self, name:str, parts:list[Part]):
#         self.name = name
#         self.parts = parts