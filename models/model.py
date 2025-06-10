class Stitch:
    def __init__(self, name:str=None, symbol:str=None):
        self.name = name
        self.symbol = symbol

class Row:
    def __init__(self, stitches:list[Stitch]=None):
        self.stitches = stitches