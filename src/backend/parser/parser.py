"""A parser of knitting patterns to a list of stitch names

Grammar
-----------

start           = pattern , ? end of input ? ;
pattern         = [cast_on] , ( stitch_sequence | [ row , { ? newline ? , row } ] ) ;
cast_on         = "cast on", ? integer ? , "stitches" | "st" | "sts" ;
row             = "row" , ? integer ? ":" , stitch_sequence ;
stitch_sequence = repeat | stitch , {"," , repeat | stitch } ;
repeat          = "*" , stitch_sequence , "*" , [";" , "repeat" , "from" , "*" , "to" , "*" , ? integer ? , "times" , ","] ;
stitch          = STITCH_TYPE , ? integer ? ;
STITCH_TYPE     = "k" | "p" ;

? integer ? : Represents a sequence of one or more digits (0 - 9). Examples include 0, 17, and 987.
? newline ? : Represents a newline ("/n") or some other kind of line divider
"""

from src.backend.domain.model import Stitch, Repeat, Row, Part
from src.backend.parser.lexer import Lexer, TokenType

class ParserError(Exception): 
    """Exception raised for errors during the parsing process"""
    def __init__(self, message): 
        super().__init__(f'PARSER ERROR DETECTED:\n{message}') 


class Parser:
    # EOI = "? end of input ?"
    _caston_num:int|None = None
    _stitches_parsed = 0

    def __init__(self, input:str):
        """Initializes the parser instance and gets the first token
        of the input string"""
        self._tokens = iter(Lexer(input).tokenize())
        # print(f"tokens are: {self.tokenize(input)}")
        self._curr_token = None
        self.advance()  # start iteration

    def advance(self):
        """Advances the iteration along the list of tokens"""
        try:
            self._curr_token = next(self._tokens)
        except StopIteration:   #if there is no next token, you're on the EOI
            self._curr_token = None

    def expect_value(self, expected_token_values:list[str])->str:
        """Checks if the current token matches the given expected value,
        if so, advances to the next token, else, error
        """
        if self._curr_token.value not in expected_token_values:
            token_found_str = f'"{self._curr_token.value}"'
            expected_tokens_str = \
                ", ".join([f'"{token}"' for token in expected_token_values])
            message = (f'Found the token: {token_found_str}\n'
                       f'But was expecting one of: {expected_tokens_str}')
            raise ParserError(message)
        
        original_curr_token = self._curr_token
        self.advance()
        return original_curr_token
    
    def expect_type(self, expected_token_types:list[TokenType]) -> str:
        """Checks if the current token matches the given expected token type,
        if so, advances to the next token, else error
        """
        if self._curr_token.type not in expected_token_types:
            token_found_str = f'"{self._curr_token.type.name}"'
            expected_tokens_str = \
                ", ".join([f'"{token.name}"' for token in expected_token_types])
            message = (f'Found the token: {token_found_str}\n'
                       f'But was expecting one of: {expected_tokens_str}')
            raise ParserError(message)
        
        original_curr_token = self._curr_token
        self.advance()
        return original_curr_token
    
    def expect_series(self, expected_token_series:list[list[str]]) -> str:
        """Checks if the next series of tokens matches the given series of expected tokens,
        if so, advances to the token after them, else, error.
        """
        for expected_token_values in expected_token_series:
            if self._curr_token.value not in expected_token_values:
                token_found_str = f'"{self._curr_token}"'
                expected_tokens_str = \
                    ", ".join([f'"{token}"' for token in expected_token_values])
                message = (f'Found the token: {token_found_str}\n'
                        f'But was expecting one of: {expected_tokens_str}')
                raise ParserError(message)
            self.advance()
        last_token = self._curr_token
        return last_token


    ## PARSING METHODS

    # start = pattern , ? end of input ? ;
    def start(self) -> Part:
        result = self.pattern()
        self.expect_type([TokenType.EOI])
        return result

    # pattern = [cast_on] , ( stitch_sequence | [ row , { ? newline ? , row } ] ) ;
    def pattern(self) -> Part:
        caston = None

        if self._curr_token.value == "cast":
            caston = self.cast_on()
            # print(f"caston is {caston}")
            self._caston_num = caston
            self.advance() #skip the newline token

        if self._curr_token.value in ["k", "p"]:  # One row, unlabeled
            instructions = self.stitch_sequence()
            if caston == None:
                caston = len(instructions)
            return Part(caston=caston, rows=[Row(number=1, instructions=instructions)])
        
        result = [self.row()]
        while self._curr_token.value == "\n":
            self.advance()
            self._stitches_parsed = 0   # reset counter
            result.append(self.row())

        if (len(result) == 1) and (caston == None):     # One row, labeled, but w/o caston
            # print("No caston given")
            return Part(caston=len(result[0].instructions), rows=result)
        
        # print(f"caston given. caston is {caston}")
        return Part(caston=caston, rows=result)         # Any number of rows, labeled, w/ caston
    
    # cast_on = "cast on", ? integer ? , "stitches" | "st" | "sts"
    def cast_on(self):
        self.expect_value(["cast"])
        self.expect_value(["on"])
        if not self._curr_token.type == TokenType.NUMBER:
            wrong_token = f'"{self._curr_token}"' 
            message = (f'Found the token: {wrong_token}\n'
                    f'But was expecting an integer')
            raise ParserError(message)
        # else: ? integer ?
        caston_num = int(self._curr_token.value)
        self.advance()  # move onto the next token
        self.expect_value(["stitches", "st", "sts"])
        return caston_num
    
    # row = "row" , ? integer ? , ":" , stitch_sequence ;
    def row(self) -> Row:
        self.expect_value(["row"])
        if not self._curr_token.type == TokenType.NUMBER:
            wrong_token = f'"{self._curr_token}"' 
            message = (f'Found the token: {wrong_token}\n'
                    f'But was expecting an integer')
            raise ParserError(message)
        # else: ? integer ?
        row_num = int(self._curr_token.value)
        self.advance()  # move onto the next token
        self.expect_value([":"])
        return Row(row_num, self.stitch_sequence())
    
    # stitch_sequence = = repeat | stitch, {"," , repeat | stitch } ;
    def stitch_sequence(self) -> list[Stitch]:
        result = []
        if self._curr_token.value == "*": # repeat
            # print("repeat encountered")
            result.append(self.repeat())
        else:   # | stitch
            result.extend(self.stitch())
        # print("appended first stitch in sequence")
        while self._curr_token.value == ",":
            # print("appending another stitch in sequence")
            self.advance()
            if self._curr_token.value == "*": # repeat
                # print("repeat encountered")
                result.append(self.repeat())
            else:   # | stitch
                result.extend(self.stitch())
        return result
    
    # repeat = "*" , stitch_sequence , "*" , [";" , "repeat" , "from" , "*" , "to" , "*" , ? integer ? , "times" , ","] ;
    def repeat(self) -> Repeat:
        if self._caston_num is None:
            raise ParserError("The number of stitches cast-on must be specified in patterns with repeats")
        self.expect_value(["*"])
        repeat_section = self.stitch_sequence()
        # print(f"repeat section is: {repeat_section}")
        self.expect_value(["*"])
        if self._curr_token.value != ";":
            return Repeat(repeat_section)
        # print("repeat number specified")
        self.expect_series([[";"], ["repeat"], ["from"], ["*"], ["to"], ["*"]])

        if not self._curr_token.type == TokenType.NUMBER:
            raise ParserError(f"Expected an integer, recieved {self._curr_token}")
        num_repeats = int(self._curr_token.value)
        self.advance()
        self.expect_value(["times"])
        return Repeat(repeat_section, num_times=num_repeats)

    # stitch = STITCH_TYPE , ? integer ? ;
    def stitch(self) -> list[Stitch]:
        result = self.stitch_type()
        if not self._curr_token.type == TokenType.NUMBER:  # just one stitch (e.g.: "k")
            self._stitches_parsed += 1
            return [result]
        multiplier = int(self._curr_token.value)
        self.advance()
        # print(f"stitch parsed, next token is {self._curr_token}")
        self._stitches_parsed += multiplier
        return [result] * multiplier

    # STITCH_TYPE = "k" | "p" | "yo" ;
    def stitch_type(self) -> Stitch:
        current = self._curr_token.value
        self.expect_type([TokenType.STITCH])

        return Stitch(current)

