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
    type: StitchType = StitchType.REGULAR

    def __post_init__(self):
        # error checking
        if not isinstance(self.abbrev, str):
            raise TypeError(f"Stitch abbrev must be type str, got type {type(self.abbrev)}")
        if not isinstance(self.type, StitchType):
            raise TypeError(f"Stitch type must be type StitchType, got type {type(self.type)}")
    
    # The current dictionary of stitch abbreviations and their names and symbols
    STITCH_BY_ABBREV = {
        "k": {"name": "knit", "rs": " ", "ws": "-"},
        "p": {"name": "purl", "rs": "-", "ws": " "},
    }

    @property
    def name(self) -> str:
        return self.STITCH_BY_ABBREV[self.abbrev]["name"]

    @property
    def symbol_rs(self) -> str:
        return self.STITCH_BY_ABBREV[self.abbrev]["rs"]
    
    @property
    def symbol_ws(self) -> str:
        return self.STITCH_BY_ABBREV[self.abbrev]["ws"]

@dataclass
class Repeat:
    elements:List[Union[Stitch, "Repeat"]]
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

    # def get_stitch_count(self, prev_stitch_count:int):
    #     increases = 0
    #     decreases = 0

    #     for instruction in self.instructions:
    #         if isinstance(instruction, Stitch): # if the instruction is a stitch, check if it's regular
    #             if instruction.type != StitchType.REGULAR:
    #                 all_reg = False
    #         elif isinstance(instruction, Repeat): # if the instruction is a repeat, check if its stitches are regular
    #             for element in instruction.elements:
    #                 if isinstance(element, Stitch):
    #                     if element.type != StitchType.REGULAR:
    #                         all_reg = False
    #                 elif isinstance(element, Repeat): # if the element is a repeat, check if its stitches are regular
    #                     if any(stitch_type != StitchType.REGULAR for stitch_type in element.elements):
    #                         all_reg = False

    @property
    def stitches(self) -> list[Stitch]:
        # if there aren't any repeats in the instructions, those are the stitches
        if not any(isinstance(x, Repeat) for x in self.instructions):
            return self.instructions
        
        # if there are, expand them starting from the last repeat
        repeat_indexes = []
        for idx, val in enumerate(self.instructions):
            if isinstance(val, Repeat):
                repeat_indexes.append(idx)

        print(f"repeat_indexes are {repeat_indexes}")

        instructions = self.instructions
        print(f"instructions are {instructions}")
        while len(repeat_indexes) != 0:
            i = repeat_indexes.pop()
            print(f"i is {i}")
            repeat:Repeat = instructions[i]

            expanded = repeat.expand()
            instructions = instructions[:i] + expanded + instructions[i+1:] # replace the Repeat with the expanded stitches
            
            print(f"instructions are now {instructions}")

        return instructions
    
class Section:
    def __init__(self, caston:int, rows:list[Row], name:str="main"):
        self.caston = caston
        self.rows = rows
        self.name = name

    @property
    def pattern(self):
        row_idxs_and_counts:list[tuple[int, int]] = []

        for idx, row in enumerate(self.rows):
            if idx == 0:
                row_idxs_and_counts.append((row.number, self.caston))
                continue
            
            # get the stitch count of the current row by the previous row's
            stitch_count = row.get_stitch_count(prev_stitch_count=row_idxs_and_counts[-1][1])