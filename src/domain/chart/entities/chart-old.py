"""Holds semantic logic for the entities related to charts"""

from copy import deepcopy
import math
from dataclasses import dataclass
from enum import Enum
from src.domain.pattern.entities import Pattern, ExpandedRow, Stitch

class CellType(Enum):
    EMPTY = "empty"
    STITCH = "stitch"

class Cell:
    def __init__(self, type:CellType, symbol:str|None=None):
        if type == CellType.EMPTY:
            symbol = "X"
        
        if type == CellType.STITCH and symbol is None:
            raise ValueError("Stitch cells must be initialized with a symbol")

        self.type = type
        self.symbol = symbol

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        
        if (self.type == other.type) and (self.symbol == other.symbol):
            return True
        return False
    
    def __repr__(self):
        return f"Cell({self.symbol})"

    # NOTE: Maybe should move to render/
    def pad_cell(self, num_spaces:int):
        """Pad the cell's value with spaces"""
        padded = self.symbol
        for i in range(num_spaces):
            if i % 2 == 0:
                padded = " " + padded
            else:
                padded = padded + " "
        
        return padded

class ChartRow:
    def arrange_rs_row(self, row:ExpandedRow) -> list[Cell]:
        symbols = row.get_symbols_rs()
        symbols.reverse()   # NOTE: right-side rows are displayed in reverse

        cells:list[Cell] = []
        for i, symbol in enumerate(symbols):
            st_type_value = row.stitches[i].type.value
            cells.append(Cell(CellType.STITCH, symbol))

        return cells
    
    def arrange_ws_row(self, row:ExpandedRow) -> list[Cell]:
        symbols = row.get_symbols_ws()

        cells:list[Cell] = []
        for i, symbol in enumerate(symbols):
            st_type_value = row.stitches[i].type.value
            cells.append(Cell(CellType.STITCH, symbol))

        return cells

    def __init__(self, row:ExpandedRow):
        self.number = row.number
        self.row = row

        if row.number % 2 == 1:
            cells = self.arrange_rs_row(row)
        else:
            cells = self.arrange_ws_row(row)
            
        self.cells:list[Cell] = cells

    def __eq__(self, other):
        if not isinstance(other, ChartRow):
            return False
        
        if (self.number == other.number) and (self.row == other.row) and (self.cells == other.cells):
            return True
        return False
    
    def __repr__(self):
        return f"ChartRow({self.number}, {self.cells})"
    
    @property
    def width(self) -> int:
        return len(self.cells)
    
    @property
    def has_padding(self) -> bool:
        return any(cell.type == CellType.EMPTY for cell in self.cells)
    
    # NOTE: Maybe move to render/
    def pad_row(self, to_pad_left:int, to_pad_right:int):
        """Modifies the ChartRow's cells to be padded on either side by the given amounts"""
        padded = deepcopy(self.cells)
        for _ in range(to_pad_left):
            padded.insert(0, Cell(CellType.EMPTY))
        for _ in range(to_pad_right):
            padded.insert(len(padded), Cell(CellType.EMPTY))
        
        self.cells = padded

        return padded
    
    def get_padding_counts(self) -> dict:
        """Get the counts on each side of all, if any, padding cells in the row"""
        all_padding = {"left": 0, "right": 0}
        # NOTE: The index of where the Xs stop is also the number of Xs there are
        all_padding["left"] = next(i for i, cell in enumerate(self.cells) if cell.type != CellType.EMPTY)
        all_padding["right"] = next(i for i, cell in enumerate(list(reversed(self.cells))) if cell.type != CellType.EMPTY)
        
        return all_padding

@dataclass(frozen=False)
class RowAnalysis:
    row:ExpandedRow
    left_offset:int = None
    right_offset:int = None
    
    @property
    def ordered_stitches(self):
        # Order stitches to get the correct left and right sides of the row
        ordered_stitches:list[Stitch] = []
        if self.row.number % 2 == 1:
            ordered_stitches = list(reversed(self.row.stitches))
        else:
            ordered_stitches = self.row.stitches
        
        return ordered_stitches
    
    @property
    def left_stitches(self):
        middle_point = math.ceil(self.row.num_instructions / 2)
        return self.ordered_stitches[:middle_point]
    
    @property
    def right_stitches(self):
        middle_point = math.ceil(self.row.num_instructions / 2)
        return self.ordered_stitches[middle_point:]

    @property
    def left_growth(self):
        """Get the amount of net stitch count change on the left side"""
        left_deltas:list[int] = []
        for stitch in self.left_stitches:
            left_deltas.append(stitch.stitches_produced - stitch.stitches_consumed)

        return sum(left_deltas)
    
    @property
    def right_growth(self):
        """Get the amount of net stitch count change on the right side"""
        right_deltas:list[int] = []
        for stitch in self.right_stitches:
            right_deltas.append(stitch.stitches_produced - stitch.stitches_consumed)

        return sum(right_deltas)

class Chart:
    def set_left_offsets(self, row_analyses:list[RowAnalysis]):
        total_left_offset = 0
        for row_analysis in row_analyses:
            total_left_offset += row_analysis.left_growth
            row_analysis.left_offset = total_left_offset
            # row_analysis.left_extent = total_left_offset
        return row_analyses

    def set_right_offsets(self, row_analyses:list[RowAnalysis]):
        total_right_offset = 0
        for row_analysis in row_analyses:
            total_right_offset += row_analysis.right_growth
            row_analysis.right_offset = total_right_offset
        return row_analyses

    def __init__(self, pattern:Pattern):
        self.pattern = pattern
        
        # Build rows and row analyses
        rows:list[ChartRow] = []
        row_analyses:list[RowAnalysis] = []
        for row in self.pattern.rows:
            chart_row = ChartRow(row)
            rows.append(chart_row)

            row_analysis = RowAnalysis(row)
            row_analyses.append(row_analysis)
        row_analyses = self.set_left_offsets(row_analyses)
        row_analyses = self.set_right_offsets(row_analyses)

        self.rows = rows
        self.row_analyses = row_analyses

    @property
    def width(self) -> int:
        return self.pattern.get_max_length()
    
    @property
    def height(self) -> int:
        return len(self.rows)
    
    @property
    def max_left(self):
        """Get the longest left half row length"""
        # left_lengths:list[int] = []
        # for row_analysis in self.row_analyses:
        #     left_lengths.append(len(row_analysis.left_stitches))
        
        # return max(left_lengths)
        return max(ra.left_offset for ra in self.row_analyses)
    
    @property
    def max_right(self):
        """Get the longest right half row length"""
        # right_lengths:list[int] = []
        # for row_analysis in self.row_analyses:
        #     right_lengths.append(len(row_analysis.right_stitches))
        
        # return max(right_lengths)
        return max(ra.right_offset for ra in self.row_analyses)

    def get_max_cell_length(self) -> int:
        """Get the length of the longest value of a cell"""
        symbols_used = self.pattern.get_symbols_used()
        
        max_sym_len = 0
        for symbol in symbols_used:
            sym_len = len(symbol)
            if "\\" in symbol:
                sym_len - 1
            max_sym_len = max(sym_len, max_sym_len)
        # Row number is also a cell value
        last_row_number = self.pattern.rows[-1].number
        longest_item = max(max_sym_len, len(str(last_row_number)))

        return longest_item
    

    def pad_chart(self):
        for i, row in enumerate(self.rows):
            row_analysis:RowAnalysis = self.row_analyses[i]
            print(f"row {row.number}")
            left_padding = row_analysis.left_offset - self.max_left
            print(f"max left is: {self.max_left}, left padding is: {left_padding}")
            right_padding = row_analysis.right_offset - self.max_right
            print(f"max right is: {self.max_right}, right padding is: {right_padding}")

            row.pad_row(left_padding, right_padding)