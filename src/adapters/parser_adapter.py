from src.ports.parser_port import ParserPort
from src.domain.model.model import Chart
from src.domain.parser.parser import Parser

class ParserAdapter(ParserPort):
    def parse(self, pattern:str) -> Chart:
        parser = Parser(pattern)
        return parser.start()