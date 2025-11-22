from src.ports.parser_port import ParserPort
from src.domain import Part, Parser, ASTtoModelTranslator

class ParserAdapter(ParserPort):
    def parse(self, pattern:str) -> Part:
        parser = Parser(pattern)
        ast = parser.start()
        model = ASTtoModelTranslator().translate_ast(ast)
        return model