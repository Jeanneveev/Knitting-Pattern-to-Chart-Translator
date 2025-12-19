import math
from src.domain.pattern.entities import Pattern, Stitch, StitchType, ExpandedRow

class Cell:
    def __init__(self, symbol:str, offset:int):
        self.symbol = symbol
        self.offset = offset

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        if (self.symbol == other.symbol) and (self.offset == other.offset):
            return True
        return False
    
    def __repr__(self):
        return f"Cell({self.symbol}, {self.offset})"

class ChartRow:
    def __init__(self, number:int, cells:list[Cell]):
        self.number = number
        # TODO: Maybe add checking to confirm cell offset is in decreasing order
        self.cells = cells

    def __eq__(self, other):
        if not isinstance(other, ChartRow):
            return False
        if (self.number == other.number) and (self.cells == other.cells):
            return True
        return False
    
    def __repr__(self):
        return f"ChartRow({self.number}, {self.cells})"

class Chart:
    def __init__(self, pattern:Pattern):
        self.pattern = pattern

    # def hypothesize_normal_next_row(self, curr_row:ExpandedRow, prev_chart_row:ChartRow):
    #     """Hypothesize the next row of a row with no net increases or decreases on either side"""
    #     print(f"row {curr_row.number} is normal, hypothesizing normal next row")
    #     hypothetical_cells = []
    #     if curr_row.is_rs:
    #         stitches = list(reversed(curr_row.stitches))
    #     else:
    #         stitches = curr_row.stitches
    #     print(f"stitches are: {stitches}")

    #     for i, instruction in enumerate(stitches):

    #         symbol = instruction.symbol_rs
    #         offset = prev_chart_row.cells[i].offset
    #         cell = Cell(symbol, offset)
    #         hypothetical_cells.append(cell)

    #     return ChartRow(curr_row.number, hypothetical_cells)

    def hypothesize_regular_next_row(self, stitches:list[Stitch]):
        for i, stitch in stitches:


    def hypothesize_chart_rows(self) -> list[int]:
        """Row by row, plot out the maximum shape of the next row
        Description: For each row in the pattern's rows, identify their order in the chart.
        Then, find the offset for each stitch of the next row based on the type and location
        of the stitches in the current row
        """
        # NOTE: The cells in hypothetical cells should be ordered
        hypothetical_row_offsets:list[int] = []
        for i, curr_row in enumerate(self.pattern.rows):
            print(f"row {curr_row.number}")
            if i == 0:
                # add the first row to the start
                cells = [Cell(st.symbol_rs, x) for x, st in enumerate(curr_row.stitches)]
                cells.reverse()
                hypothetical_row_offsets.append(ChartRow(curr_row.number, cells))

            # Split row into left and right halves
            middle_point = len(curr_row.stitches) / 2
            # NOTE: Below handles non-even row lengths,
            #  and is working on the assumption that if an increase/decrease were to occur in the middle of the row,
            #  the added/subtracted stitch would lend to the direction of the end of the row, and thus be a part of that side
            if curr_row.is_rs:
                middle_point = int(math.ceil(middle_point))
                stitches = list(reversed(curr_row.stitches))
                left_stitches = stitches[:middle_point]
                right_stitches = stitches[middle_point:]
            else:
                middle_point = int(math.floor(middle_point))
                left_stitches = curr_row.stitches[:middle_point]
                right_stitches = curr_row.stitches[middle_point:]
            # print(f"middle point is: {middle_point}")
            print(f"left stitches are: {left_stitches}, right_stitches are: {right_stitches}")

            # Find the stitch delta of the left and right stitches between start and end of row
            left_delta = 0
            for stitch in left_stitches:
                left_delta += stitch.stitches_produced - stitch.stitches_consumed

            right_delta = 0
            for stitch in right_stitches:
                right_delta += stitch.stitches_produced - stitch.stitches_consumed

            print(f"Left delta is: {left_delta}, right delta is: {right_delta}")

            # If there was no net stitch change, predict that the next row will have the same shape and placements as the current row
            if left_delta == 0 and right_delta == 0:
                hypothetical_row_offsets.append(self.hypothesize_regular_next_row())

            # a normal row produces a next row with the same size and places
            # if all(instruction.type == StitchType.REGULAR for instruction in row.stitches):
            #     hypothetical_row = self.hypothesize_normal_next_row(row, hypothetical_rows[i-1])

            #     hypothetical_rows.append(hypothetical_row)
            # else:
            #     # split row into left and right halves
            #     
            #     if row.is_rs:
            #         middle_point = int(math.ceil(middle_point))
            #         stitches = list(reversed(row.stitches))
            #         left_stitches = stitches[:middle_point]
            #         right_stitches = stitches[middle_point:]
            #     else:
            #         middle_point = int(math.floor(middle_point))
            #         left_stitches = row.stitches[:middle_point]
            #         right_stitches = row.stitches[middle_point:]
            #     print(f"middle point is: {middle_point}")
            #     print(f"left stitches are: {left_stitches}, right_stitches are: {right_stitches}")
                
                # calculate net increase/decrease for each side

        
        return hypothetical_row_offsets

                    