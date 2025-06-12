from dataclasses import dataclass, field

@dataclass(frozen=True)
class Stitch:
    STITCH_MAP = {
        "k": {"name": "Knit", "rs": "⬤", "ws": "〇"},
        "p": {"name": "Purl", "rs": "〇", "ws": "⬤"}
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

class Row:
    def __init__(self, number:int, stitches:list[Stitch]):
        self.number = number
        self.stitches = stitches
        
class Pattern:
    def __init__(self, rows:list[Row]):
        self.rows = rows

    def get_row(self, number):
        for row in self.rows:
            if row.number == number:
                return row.stitches
        raise ValueError(f"Row {number} not found")