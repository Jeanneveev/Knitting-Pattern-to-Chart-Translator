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
    
    def _pad_item(self, symbol:str, width:int) -> str:
        """Pad item to given width"""
        item_len = width + 2    # +2 for padding
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
        max_sym_len = self._get_max_chart_sym_len()
        symbols = [cell.symbol for cell in row.cells]
        symbols.reverse()   # reverse because symbols are originally right-to-left
        
        result = "|"
        for symbol in symbols:
            padded = self._pad_item(symbol, max_sym_len)
            result += f"{padded}|"

        padded_row_num = self._pad_item(str(row_num), max_sym_len)
        spacer = " " * len(padded_row_num)

        if row_num % 2 == 1:    #rs
            result = spacer + result + padded_row_num + "\n"
        else:   # ws
            result = padded_row_num + result + spacer + "\n"

        return result
    
    def render_chart(self) -> str:
        border = self._build_border()

        result = border
        rows = list(reversed(self.padded_rows))
        for row in rows:
            result += self._build_row(row.number)
            result += border
        
        return result
    
    # def _get_longest_key_val(self) -> int:        
    #     key = self.chart.key
    #     values:list[str] = []
    #     for k, v in key.items():
    #         values.append(k)    # symbol
    #         values.extend(list(v.values())) # rs and ws names
    #     values.extend(["Symbol", "Meaning", "RS", "WS"])    # headers

    #     max_len = 0
    #     for value in values:
    #         max_len = max(len(value), max_len)
        
    #     return max_len

    def _get_column_width(self, contents:list[str]) -> int:
        """Gets the width of the longest string in the chart contents"""
        width = 0
        for value in contents:
            width = max(len(value), width)
        
        return width + 2

    def render_key(self) -> str:
        key = ""
        
        symbols = list(self.chart.key.keys())
        symbol_names = symbols + ["SYMBOL"]
        right_sides = [names["rs"] for _, names in self.chart.key.items()]
        rs_names = right_sides + ["RS"]
        wrong_sides = [names["ws"] for _, names in self.chart.key.items()]
        ws_names = wrong_sides + ["WS"]

        symbol_width = self._get_column_width(symbol_names)
        rs_width = self._get_column_width(rs_names)
        ws_width = self._get_column_width(ws_names)
        
        sym_pad_width = symbol_width - 2
        rs_pad_width = rs_width - 2
        ws_pad_width = ws_width - 2
        meaning_width = rs_width + ws_width + 1     # for the | between them
        meaning_pad_width = meaning_width - 2

        header = ""
        # Header row 1
        symbol_border = f"+{'-' * symbol_width}"
        meaning_border = f"+{'-' * meaning_width}"
        header_border_1 = symbol_border + meaning_border + "+\n"

        header_body_1 = "| SYMBOL |" + self._pad_item("MEANING", meaning_pad_width) + "|\n"
        header = header_border_1 + header_body_1 + header_border_1

        # Header row 2
        header_body_2 = f"|{' ' * symbol_width}|"
        header_body_2 += self._pad_item("RS", rs_pad_width) + "|" + self._pad_item("WS", ws_pad_width) + "|\n"
        header_border_2 = symbol_border + f"+{'-' * rs_width}" + f"+{'-' * ws_width}" + "+\n"

        header += header_body_2 + header_border_2

        key = header

        # Body
        for i, symbol in enumerate(symbols):
            padded_symbol = self._pad_item(symbol, sym_pad_width)
            padded_rs = self._pad_item(right_sides[i], rs_pad_width)
            padded_ws = self._pad_item(wrong_sides[i], ws_pad_width)

            key += f"|{padded_symbol}|{padded_rs}|{padded_ws}|\n"
            key += header_border_2

        return key
