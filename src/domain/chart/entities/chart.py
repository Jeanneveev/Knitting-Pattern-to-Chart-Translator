"""Holds semantic logic for the entities related to charts"""

from copy import deepcopy
from enum import Enum
from src.domain.pattern.entities import Pattern, ExpandedRow

class CellType(Enum):
    EMPTY = "empty"
    STITCH = "stitch"

# values are the same as StitchType, exists for layer separation reasons
class CellStitchType(Enum):
    REGULAR = "reg"
    INCREASE = "incr"
    DECREASE = "decr"

class Cell:
    def __init__(self, type:CellType, symbol:str|None=None, st_type:CellStitchType|None=None):
        if type == CellType.EMPTY:
            symbol = "X"
            st_type = None
        
        if type == CellType.STITCH and symbol is None:
            raise ValueError("Stitch cells must be initialized with a symbol")
        if type == CellType.STITCH and st_type is None:
            raise ValueError("Stitch cells must be initialized with a stitch type")

        self.type = type
        self.symbol = symbol
        self.st_type = st_type

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        
        if (self.type == other.type) and (self.symbol == other.symbol) and (self.st_type == other.st_type):
            return True
        return False
    
    def __repr__(self):
        return f"Cell({self.symbol}, {self.st_type})"

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
            cell_st_type = CellStitchType(st_type_value)
            cells.append(Cell(CellType.STITCH, symbol, cell_st_type))

        return cells
    
    def arrange_ws_row(self, row:ExpandedRow) -> list[Cell]:
        symbols = row.get_symbols_ws()

        cells:list[Cell] = []
        for i, symbol in enumerate(symbols):
            st_type_value = row.stitches[i].type.value
            cell_st_type = CellStitchType(st_type_value)
            cells.append(Cell(CellType.STITCH, symbol, cell_st_type))

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
    
    @property
    def has_increases(self) -> bool:
        return any(cell.st_type == CellStitchType.INCREASE for cell in self.cells)
    
    @property
    def has_decreases(self) -> bool:
        return any(cell.st_type == CellStitchType.DECREASE for cell in self.cells)
    
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

class Chart:
    def __init__(self, pattern:Pattern):
        self.pattern = pattern
        
        # Build rows
        rows:list[ChartRow] = []
        for row in self.pattern.rows:
            chart_row = ChartRow(row)
            rows.append(chart_row)

        self.rows = rows

    @property
    def width(self) -> int:
        return self.pattern.get_max_length()
    
    @property
    def height(self) -> int:
        return len(self.rows)

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
