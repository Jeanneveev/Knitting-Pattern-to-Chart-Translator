"""A parser of knitting patterns to a list of stitch names

Grammar
-----------

start           = pattern , ? end of input ? ;
pattern         = [cast_on] , ( stitch_sequence | [ row , { ? newline ? , row } ] ) ;
cast_on         = "cast on", ? integer ? , "stitches"
row             = "row" , ? integer ? ":" , stitch_sequence ;
stitch_sequence = stitch, {"," , stitch } ;
stitch          = STITCH_TYPE , ? integer ? ;
STITCH_TYPE     = "k" | "p" ;

? integer ? : Represents a sequence of one or more digits (0 - 9). Examples include 0, 17, and 987.
? newline ? : Represents a newline ("/n") or some other kind of line divider
"""

import re
from src.models.model import Stitch, Row, Pattern

class ParserError(Exception): 
    """Exception raised for errors during the parsing process"""
    def __init__(self, message): 
        super().__init__(f'PARSER ERROR DETECTED:\n{message}') 


class Parser:
    EOI = "? end of input ?"

    def __init__(self, input:str):
        """Initializes the parser instance and gets the first token
        of the input string"""
        self._tokens = iter(self.tokenize(input))
        # print(f"tokens are: {self.tokenize(input)}")
        self._curr_token = None
        self.advance()  # start iteration

    def tokenize(self, input:str)->list[str]:
        """Tokenize the input into a list of strings"""
        pattern = r"[a-z]+|\d+|,|:|\n"
        tokens = re.findall(pattern, input)
        tokens.append(self.EOI)
        return tokens

    def advance(self):
        """Advances the iteration along the list of tokens"""
        try:
            self._curr_token = next(self._tokens)
        except StopIteration:   #if there is no next token, you're on the EOI
            self._curr_token = None

    def expect(self, expected_tokens:list[str])->str:
        """Checks if the current token matches the given expected value,
        if so, advance to the next token, else, error
        """
        if self._curr_token not in expected_tokens:
            token_found_str = f'"{self._curr_token}"'
            expected_tokens_str = \
                ", ".join([f'"{token}"' for token in expected_tokens])
            message = (f'Found the token: {token_found_str}\n'
                       f'But was expecting one of: {expected_tokens_str}')
            raise ParserError(message)
        
        original_curr_token = self._curr_token
        self.advance()
        return original_curr_token
    
    ## PARSING METHODS

    # start = pattern , ? end of input ? ;
    def start(self) -> Pattern:
        result = self.pattern()
        self.expect([self.EOI])
        return result

    # pattern = [cast_on] , ( stitch_sequence | [ row , { ? newline ? , row } ] ) ;
    def pattern(self) -> Pattern:
        caston = None

        if self._curr_token == "cast":
            caston = self.cast_on()
            self.advance() #skip the newline token

        if self._curr_token in ["k", "p"]:
            return Pattern(caston=caston, rows=[Row(1, self.stitch_sequence())])
        
        result = [self.row()]
        while self._curr_token == "\n":
            self.advance()
            result.append(self.row())
        return Pattern(caston=caston, rows=result)
    
    # cast_on = "cast on", ? integer ? , "stitches"
    def cast_on(self):
        self.expect(["cast"])
        self.expect(["on"])
        if not self._curr_token.isdigit():
            wrong_token = f'"{self._curr_token}"' 
            message = (f'Found the token: {wrong_token}\n'
                    f'But was expecting an integer')
            raise ParserError(message)
        # else: ? integer ?
        caston_num = int(self._curr_token)
        self.advance()  # move onto the next token
        self.expect(["stitches"])
        return caston_num
    
    # row = "row" , ? integer ? , ":" , stitch_sequence ;
    def row(self) -> Row:
        self.expect(["row"])
        if not self._curr_token.isdigit():
            wrong_token = f'"{self._curr_token}"' 
            message = (f'Found the token: {wrong_token}\n'
                    f'But was expecting an integer')
            raise ParserError(message)
        # else: ? integer ?
        row_num = int(self._curr_token)
        self.advance()  # move onto the next token
        self.expect([":"])
        return Row(row_num, self.stitch_sequence())
    
    # stitch_sequence = stitch, {"," , stitch } ;
    def stitch_sequence(self) -> list[Stitch]:
        result = []
        result.extend(self.stitch())
        # print("appended first stitch in sequence")
        while self._curr_token == ",":
            # print("appending another stitch in sequence")
            self.advance()
            result.extend(self.stitch())
        return result

    # stitch = STITCH_TYPE , ? integer ? ;
    def stitch(self) -> list[Stitch]:
        result = self.stitch_type()
        if not self._curr_token.isdigit():
            return [result]
        multiplier = int(self._curr_token)
        self.advance()
        # print(f"stitch parsed, next token is {self._curr_token}")
        return [result] * multiplier
        
    # STITCH_TYPE = "k" | "p" ;
    def stitch_type(self) -> Stitch:
        current = self._curr_token
        self.expect(["k", "p"])
        return Stitch(current)
    

if __name__ == "__main__": 
    example = "k2, p2, k2"
    expected = ["k", "k", "p", "p", "k", "k"]


