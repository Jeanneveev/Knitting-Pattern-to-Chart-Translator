from src.ports.parser_port import ParserPort
from src.domain import Parser, ParserError, Pattern, ASTtoModelTranslator, ModelToPatternTranslator

class ParsingError(Exception): 
    """Exception raised for errors during the parsing process"""
    def __init__(self, message): 
        super().__init__(message)

class ParserAdapter(ParserPort):
    def parse(self, pattern:str) -> Pattern:
        parser = Parser(pattern)
        try:
            ast = parser.start()
        except ParserError as e:
            raise ParsingError(f"Error occurred during parsing: {repr(e)}") from e
        except Exception as e:  # also catch any other error
            raise ParsingError(f"Unknown error occurred during parsing: {repr(e)}") from e
        
        try:
            model = ASTtoModelTranslator().translate_ast(ast)
        except TypeError as e:
            raise ParsingError(f"Error occurred during AST to model translation: {repr(e)}") from e
            
        try:
            pattern = ModelToPatternTranslator().translate_model(model)
        except Exception as e:
            raise ParsingError(f"Error occurred during model to pattern translation: {repr(e)}") from e
        return pattern