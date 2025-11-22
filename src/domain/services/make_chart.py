from src.domain.services.make_pattern import Pattern
from src.domain.model.model import Stitch

class Chart:
    def __init__(self, pattern:Pattern):
        self.pattern = pattern

    def get_row_symbols(self, row_num:int) -> dict:
        """Get the symbols of a row in the pattern by its row number"""
        ## NOTE: odd rows are on the right side and use rs symbols
        # while even rows are on the wrong side and use ws symbols.
        if row_num % 2 == 1:  #right-side, display in reverse
            # print("right-side")
            row = self.pattern.get_row(row_num)
            symbols = row.get_symbols_rs()
            symbols.reverse()
            return {row_num: symbols}
        else:   #wrong-side, display normally
            # print("wrong-side")
            row = self.pattern.get_row(row_num)
            symbols = row.get_symbols_ws()
            return {row_num: symbols}
        
    def _build_border(self) -> str:
        length = self.pattern.get_max_length()
        border = "---+---"
        for _ in range(length):
            border += "+---"

        return border + "\n"
    
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

        return result + "\n"

    def render_grid(self) -> str:
        border = self._build_border()        
        body = []
        rows = list(reversed(self.pattern.rows))
        for row in rows:
            body.append(self._build_row(row.number))

        grid = ""
        for row in body:
            grid += border
            grid += row
        grid += border

        # print(f"grid is:\n {grid}")
        return grid
    
    def _get_column_width(self, contents:list[str]) -> int:
        """Get the width of the longest value in the column"""
        max_width = 0
        for string in contents:
            max_width = max(max_width, len(string))

        return max_width + 2    # +2 for padding
    
    def _pad_column(self, column_contents) -> list[str]:
        column_width = self._get_column_width(column_contents)
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
        abbreviations = self.pattern.get_stitches_used()
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

        names_padded = self._pad_column(names)
        abbrev_padded = self._pad_column(abbreviations)
        rs_padded = self._pad_column(right_sides)
        ws_padded = self._pad_column(wrong_sides)

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