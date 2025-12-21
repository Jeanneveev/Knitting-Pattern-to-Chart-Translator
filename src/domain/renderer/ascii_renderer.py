"""Functions and entities related to rendering a Chart into ASCII"""

import math
from copy import deepcopy
from src.domain.chart.entities.chart import Chart, ChartRow
from src.domain.pattern.entities import StitchType

class ASCIIRender:
    def _add_padding(self):
        """Add padding to chart rows and set it to .padded_rows"""
        width = self.chart.width

        self.padded_rows:list[ChartRow] = []
        for row in self.chart.rows:
            self.padded_rows.append(self.chart.get_padded_row(row.number, width))

    def __init__(self, chart:Chart):
        self.chart = chart
        self.width = chart.width
        self.padded_rows: None|list[ChartRow] = None
        self._add_padding()

    # PADDING
    def _get_max_row_sym_len(self, row_num) -> int:
        """Get the length of the longest symbol in the row"""
        row = self.chart.get_row(row_num)
        symbols = [cell.symbol for cell in row.cells]
        symbols.append(str(row.number))  # Row numbers also count
        max_sym_len = 0

        for symbol in symbols:
            sym_len = len(symbol)
            if "\\" in symbol:
                sym_len - 1
            max_sym_len = max(sym_len, max_sym_len)

        return max_sym_len
    
    def _get_max_chart_sym_len(self) -> int:
        """Get the length of the longest symbol in the chart"""
        # NOTE: When adding ability to change symbols, this'll need to be changed
        longest_sym = 0
        for row in self.chart.rows:
            longest_sym = max(self._get_max_row_sym_len(row.number), longest_sym)
        
        return longest_sym

    # PADDING
    def _get_padded_row(self, row_num:int) -> ChartRow:
        """Get a padded row by the row number"""
        for padded_row in self.padded_rows:
            if padded_row.number == row_num:
                return padded_row
            
        raise ValueError(f"Padded row of number {row_num} not found")

    # PUTTING THE GRID TOGETHER
    def _build_border(self) -> str:
        """Create the border line to the width of the chart"""
        # Calculate many dashes there should be per item
        length = self.width
        dash_num = self._get_max_chart_sym_len() + 2 # +2 for the padding on either side

        # Build border
        border_line = "-" * dash_num
        border = border_line
        for _ in range(length + 1): # +1 is for the last space 
            border += f"+{border_line}"

        return border + "\n"
    
    def _pad_item(self, symbol:str) -> str:
        item_len = self._get_max_chart_sym_len() + 2    # +2 for padding
        sym_len = len(symbol)
        to_pad = item_len - sym_len # always < 2

        padded_item = symbol
        for i in range(to_pad):
            if i % 2 == 0:
                padded_item = " " + padded_item
            else:
                padded_item = padded_item + " "

        return padded_item

    def _build_row(self, row_num) -> str:
        """Create a row of symbols based on given chart row"""
        row = self._get_padded_row(row_num)
        symbols = [cell.symbol for cell in row.cells]
        symbols.reverse()   # reverse because symbols are originally right-to-left
        
        result = "|"
        for symbol in symbols:
            padded = self._pad_item(symbol)
            result += f"{padded}|"

        padded_row_num = self._pad_item(str(row_num))
        spacer = " " * len(padded_row_num)

        if row_num % 2 == 1:    #rs
            result = spacer + result + padded_row_num + "\n"
        else:   # ws
            result = padded_row_num + result + spacer + "\n"

        return result
    
    def render_ascii_chart(self) -> str:
        border = self._build_border()

        result = border
        rows = list(reversed(self.padded_rows))
        for row in rows:
            result += self._build_row(row.number)
            result += border
        
        return result