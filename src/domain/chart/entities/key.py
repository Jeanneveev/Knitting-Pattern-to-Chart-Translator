from src.domain.stitch_by_abbrev import STITCH_BY_ABBREV

class Key:
    def __init__(self, symbols:None|list[str]=None):
        self.symbols = [] if symbols is None else symbols

    @property
    def canonical_key(self) -> dict[str, dict]:
        """All the key symbols and values"""
        # KEY = {symbol: {"rs": rs_name, "ws": ws_name}}
        key = {}
        for _, d in STITCH_BY_ABBREV.items():
            rs_sym = d["rs"]
            ws_sym = d["ws"]
            
            if rs_sym in key.keys():
                key[rs_sym]["rs"] = d["name"]
            else:
                key[rs_sym] = {"rs": d["name"]}

            if ws_sym in key.keys():
                key[ws_sym]["ws"] = d["name"]
            else:
                key[ws_sym] = {"ws": d["name"]}

        return key
    
    @property
    def KEY_BY_SYMBOLS(self) -> dict[str, dict]:
        """Canonical key reduced to only the entries of the symbols given"""
        key_by_syms = {}
        for symbol in self.symbols:
            try:
                values = self.canonical_key[symbol]
                key_by_syms[symbol] = values
            except:
                raise IndexError(f"Symbol not found: \"{symbol}\"")
        
        return key_by_syms