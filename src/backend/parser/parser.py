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

import re
from src.backend.domain.model import Stitch, Repeat, Row, Part

class ParserError(Exception): 
    """Exception raised for errors during the parsing process"""
    def __init__(self, message): 
        super().__init__(f'PARSER ERROR DETECTED:\n{message}') 


class Parser:
    EOI = "? end of input ?"
    _curr_st_num:int|None = None
    _stitches_parsed = 0

    def __init__(self, input:str):
        """Initializes the parser instance and gets the first token
        of the input string"""
        self._tokens = iter(self.tokenize(input))
        # print(f"tokens are: {self.tokenize(input)}")
        self._curr_token = None
        self.advance()  # start iteration

    def tokenize(self, input:str)->list[str]:
        """Tokenize the input into a list of strings"""
        pattern = r"[a-z]+|\d+|,|:|\n|\*|;"
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
    
    def expect_series(self, expected_token_series:list[list[str]]) -> str:
        """Checks if the next series of tokens matches the given series of expected tokens,
        if so, advances to the token after them, else, error.
        """
        for expected_tokens in expected_token_series:
            if self._curr_token not in expected_tokens:
                token_found_str = f'"{self._curr_token}"'
                expected_tokens_str = \
                    ", ".join([f'"{token}"' for token in expected_tokens])
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
        self.expect([self.EOI])
        return result

    # pattern = [cast_on] , ( stitch_sequence | [ row , { ? newline ? , row } ] ) ;
    def pattern(self) -> Part:
        caston = None

        if self._curr_token == "cast":
            caston = self.cast_on()
            # print(f"caston is {caston}")
            self._curr_st_num = caston
            self.advance() #skip the newline token

        if self._curr_token in ["k", "p"]:  # One row, unlabeled
            instructions = self.stitch_sequence()
            if caston == None:
                caston = len(instructions)
            return Part(caston=caston, rows=[Row(number=1, instructions=instructions)])
        
        result = [self.row()]
        while self._curr_token == "\n":
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
        self.expect(["stitches", "st", "sts"])
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
    
    # stitch_sequence = = repeat | stitch, {"," , repeat | stitch } ;
    def stitch_sequence(self) -> list[Stitch]:
        result = []
        if self._curr_token == "*": # repeat
            # print("repeat encountered")
            result.append(self.repeat())
        else:   # | stitch
            result.extend(self.stitch())
        # print("appended first stitch in sequence")
        while self._curr_token == ",":
            # print("appending another stitch in sequence")
            self.advance()
            if self._curr_token == "*": # repeat
                # print("repeat encountered")
                result.append(self.repeat())
            else:   # | stitch
                result.extend(self.stitch())
        return result
    
    # repeat = "*" , stitch_sequence , "*" , [";" , "repeat" , "from" , "*" , "to" , "*" , ? integer ? , "times" , ","] ;
    def repeat(self) -> Repeat:
        if self._curr_st_num is None:
            raise ParserError("The number of stitches cast-on must be specified in patterns with repeats")
        self.expect(["*"])
        repeat_section = self.stitch_sequence()
        # print(f"repeat section is: {repeat_section}")
        self.expect(["*"])
        if self._curr_token != ";":
            return Repeat(repeat_section)
        # print("repeat number specified")
        self.expect_series([[";"], ["repeat"], ["from"], ["*"], ["to"], ["*"]])

        if not self._curr_token.isdigit():
            raise ParserError(f"Expected an integer, recieved {self._curr_token}")
        num_repeats = int(self._curr_token)
        self.advance()
        self.expect(["times"])
        return Repeat(repeat_section, num_times=num_repeats)

    # stitch = STITCH_TYPE , ? integer ? ;
    def stitch(self) -> list[Stitch]:
        result = self.stitch_type()
        if not self._curr_token.isdigit():  # just one stitch (e.g.: "k")
            self._stitches_parsed += 1
            return [result]
        multiplier = int(self._curr_token)
        self.advance()
        # print(f"stitch parsed, next token is {self._curr_token}")
        self._stitches_parsed += multiplier
        return [result] * multiplier

    # STITCH_TYPE = "k" | "p" | "yo" ;
    def stitch_type(self) -> Stitch:
        current = self._curr_token
        if self._curr_token == "yo":    #increase
            self._curr_st_num += 1
            # print(f"increase found, curr_st is: {self._curr_st_num}")
        self.expect(["k", "p", "yo"])

        return Stitch(current)
    

# if __name__ == "__main__": 
#     example = "k2, p2, k2"
#     expected = ["k", "k", "p", "p", "k", "k"]


