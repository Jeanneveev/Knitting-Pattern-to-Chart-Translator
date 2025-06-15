from dataclasses import dataclass

@dataclass(frozen=True)
class Stitch:
    STITCH_MAP = {
        "k": {"name": "Knit", "rs": " ", "ws": "X"},
        "p": {"name": "Purl", "rs": "X", "ws": " "}
    }
    
    abbrev: str
    
    @property
    def name(self)->str:
        return self.STITCH_MAP[self.abbrev]["name"]

    @property
    def symbol_rs(self)->str:
        return self.STITCH_MAP[self.abbrev]["rs"]
    
    @property
    def symbol_ws(self)->str:
        return self.STITCH_MAP[self.abbrev]["ws"]

@dataclass(frozen=True)
class Row:
    number:int
    stitches:list[Stitch]

    def __len__(self) -> int:
        return len(self.stitches)

    def get_symbols_rs(self) -> list[str]:
        """Return the right-side symbols of the row"""
        result = []
        for stitch in self.stitches:
            result.append(stitch.symbol_rs)
        return result
    
    def get_symbols_ws(self) -> list[str]:
        """Return the wrong-side symbols of the row"""
        result = []
        for stitch in self.stitches:
            result.append(stitch.symbol_ws)
        return result

@dataclass(frozen=True)  
class Pattern:
    rows:list[Row]

    @property
    def last_row(self) -> Row:
        return self.rows[-1]

    def get_row(self, number) -> Row:
        for row in self.rows:
            if row.number == number:
                return row
        raise ValueError(f"Row {number} not found")
    
    def max_length(self) -> int:
        max_len = 0
        for row in self.rows:
            if len(row) > max_len:
                max_len = len(row)
        return max_len

@dataclass 
class Chart:
    pattern:Pattern

    def get_row_symbols(self, n:int) -> dict:
        """Display a row of a pattern using the stitches' symbols.
        Note that odd rows are on the right side and use rs symbols while even rows are on
        the wrong side and use ws symbols.
        """
        if n%2==1:  #right-side, display in reverse
            # print("right-side")
            row = self.pattern.get_row(n)
            symbols = row.get_symbols_rs()
            symbols.reverse()
            return {n: symbols}
        else:   #wrong-side, display normally
            print("wrong-side")
            row = self.pattern.get_row(n)
            symbols = row.get_symbols_ws()
            return {n: symbols}
        
    def _build_border(self, length) -> str:
        border = "---+---"
        for _ in range(length):
            border += "+---"
        return border
    def _build_row(self, row_num:int):
        result = "|"
        symbols = self.get_row_symbols(row_num)[row_num]
        for symbol in symbols:
            result += f" {symbol} |"
        if row_num%2==1:    #right-side, display in reverse
            print("right-side")
            result = "   " + result + f" {row_num} "
        else:               #wrong-side, display normally
            print("wrong-side")
            result = f" {row_num} " + result + "   "
        return result

    def render_grid(self) -> str:
        inner = ""
        length = self.pattern.max_length()
        border = self._build_border(length)
        for row in self.pattern.rows:
            inner = inner + self._build_row(row.number) + "\n"
            if row != self.pattern.last_row:    # add a horizontal line after all rows except the last one
                inner = inner + border + "\n"

        grid = border + "\n" + inner + border
        print(f"grid is:\n {grid}")
        return grid
        # return border + "\n"

        
                
