from src.ports.parser_port import ParserPort
from src.domain import Parser, ParserError, Pattern, ASTtoModelTranslator, ModelToPatternTranslator

class ParserAdapter(ParserPort):
    def parse(self, pattern:str) -> Pattern:
        try:
            parser = Parser(pattern)
        except ParserError as err:
            raise err
        except Exception as e:  # also catch any other error
            raise ParserError(f"Unknown error occurred during parsing:\n") from e
        
        ast = parser.start()
        model = ASTtoModelTranslator().translate_ast(ast)
        pattern = ModelToPatternTranslator().translate_model(model)
        return pattern