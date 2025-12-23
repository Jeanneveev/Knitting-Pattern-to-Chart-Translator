from enum import Enum
from src.domain.pattern.entities import Pattern
from src.domain.chart.entities.key import Key

class CellType(Enum):
    STITCH = "stitch"
    EMPTY = "empty"

# NOTE: Remember that the numbers increase leftwards
class Cell:
    def __init__(self, symbol:str, start_point:int, end_point:int, type:CellType=CellType.STITCH):
        if type == CellType.EMPTY:
            symbol = "X"

        self.symbol = symbol
        self.start_point = start_point
        self.end_point = end_point
        self.type = type

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        if (self.symbol == other.symbol and
            self.start_point == other.start_point and
            self.end_point == other.end_point and
            self.type == other.type
        ):
            return True
        return False
    
    def __repr__(self):
        return f"Cell({self.symbol}, {self.start_point})"

class ChartRow:
    def __init__(self, number:int, cells:list[Cell]):
        self.number = number
        # TODO: Maybe add checking to confirm cell offset is in decreasing order
        self.cells = cells
        self.start_point = 0
        self.end_point = len(cells)
        self.width = len(cells)

    def __eq__(self, other):
        if not isinstance(other, ChartRow):
            return False
        
        if (self.number == other.number and
            self.cells == other.cells and
            self.start_point == other.start_point and
            self.width == other.width
        ):
            return True
        return False
    
    def __repr__(self):
        return f"ChartRow({self.number}, {self.cells})"

class Chart:
    def _build_rows(self, pattern:Pattern) -> list[ChartRow]:
        """Creates right aligned ChartRows based on the given pattern"""
        chart_rows:list[ChartRow] = []
        for row in pattern.rows:
            # print(f"Row {row.number}")
            cells = []
            stitches = row.stitches if row.is_rs else list(reversed(row.stitches))
            for i, s in enumerate(stitches):
                # print(f"Stitch {i} is: {s}")
                symbol = s.symbol_rs if row.is_rs else s.symbol_ws
                # NOTE: If I ever implement cables, this'll have to change
                start_point = i
                end_point = i + 1
                cells.append(Cell(symbol, start_point, end_point))

            chart_rows.append(ChartRow(row.number, cells))
        
        return chart_rows

    def __init__(self, pattern:Pattern):
        self.pattern = pattern
        rows = self._build_rows(pattern)
        self.rows = rows
        self.height = len(rows)
        self.width = pattern.get_max_length()
        self.key = Key(pattern.get_symbols_used()).KEY_BY_SYMBOLS

    def get_row(self, row_num:int) -> ChartRow:
        result = None
        for row in self.rows:
            if row.number == row_num:
                result = row
        
        if result is None:
            raise ValueError(f"No chart row of number: {row_num} found")
        
        return result

    def shift_row_left(self, row_num:int, amount:int):
        """Shift a row to the left by the given amount"""
        row = self.get_row(row_num)

        if row.width + amount > self.width:
            raise IndexError("Shift goes beyond chart bounds")

        for cell in row.cells:
            cell.start_point += amount
            cell.end_point += amount

    def shift_row_right(self, row_num:int, amount:int):
        """Shift a row to the right by the given amount"""
        row = self.get_row(row_num)

        if row.cells[0].start_point - amount < 0:
            raise IndexError("Shift goes beyond chart bounds")

        for cell in row.cells:
            cell.start_point -= amount
            cell.end_point -= amount

    def get_padded_row(self, row_num:int, width:int) -> ChartRow:
        """Pad the given row with empty cells on either side until cells length equals given width"""
        row = self.get_row(row_num)
        row_start = row.cells[0].start_point
        row_end = row.cells[-1].end_point

        cells = row.cells
        for i in range(0, row_start):
            cells.insert(0, Cell("X", i, i+1, CellType.EMPTY))
        
        for i in range(row_end, width):
            cells.append(Cell("X", i, i+1, CellType.EMPTY))

        return ChartRow(row_num, cells)