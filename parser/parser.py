"""A parser of knitting patterns to a list of stitch names

Grammar
-----------

start           = pattern , ? end of input ? ;
pattern         = stitch_sequence | [ row , { ? newline ? , row } ] ;
row             = "row" , ? integer ? ":" , stitch_sequence ;
stitch_sequence = stitch, {"," , stitch } ;
stitch          = STITCH_TYPE , ? integer ? ;
STITCH_TYPE     = "k" | "p" ;

? integer ? : Represents a sequence of one or more digits (0 - 9). Examples include 0, 17, and 987.
? newline ? : Represents a newline ("/n") or some other kind of line divider
"""

import re

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
        print(f"tokens are: {self.tokenize(input)}")
        self._curr_token = None
        self.advance()  # start iteration

    def tokenize(self, input:str)->list[str]:
        """Tokenize the input into a list of strings"""
        tokens = []

        for part in input.split(","):
            part = part.strip()
            stitch_match = re.fullmatch(r'([a-z]+)(\d+)', part)
            single_stitch_match = re.fullmatch(r'([a-z]+)', part)
            if stitch_match:    #split the stitch name and count into their own tokens
                stitch_type, count = stitch_match.groups()
                tokens.extend([stitch_type, count])
            elif single_stitch_match:   #if it's just one stitch w/ no count
                tokens.append(single_stitch_match)
            else:
                raise ParserError(f"Invalid stitch syntax: {part}")
            
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
    def start(self):
        self.pattern()
        self.expect([self.EOI])

    # pattern = stitch_sequence | [ row , { ? newline ? , row } ] ;
    def pattern(self):
        if self._curr_token in ["k", "p"]:
            self.stitch_sequence()
        else:
            self.row()
            while self._curr_token == "\n":
                self.advance()
                self.row()
    
    # row = "row" , ? integer ? , ":" , stitch_sequence ;
    def row(self):
        self.expect(["row"])
        if not self._curr_token.isdigit():
            wrong_token = f'"{self._curr_token}"' 
            message = (f'Found the token: {wrong_token}\n'
                    f'But was expecting an integer')
            raise ParserError(message)
        # else: ? integer ?
        self.advance()  # move onto the next token
        self.expect([":"])
        self.stitch_sequence()
    
    # stitch_sequence = stitch, {"," , stitch } ;
    def stitch_sequence(self):
        self.stitch()
        while self._curr_token == ",":
            self.advance()
            self.stitch()

    # stitch = STITCH_TYPE , ? integer ? ;
    def stitch(self):
        self.stitch_type()
        if not self._curr_token.isdigit():
            wrong_token = f'"{self._curr_token}"' 
            message = (f'Found the token: {wrong_token}\n'
                    f'But was expecting an integer')
            raise ParserError(message)
        multiplier = int(self._curr_token)
        self.advance()
        
    # STITCH_TYPE = "k" | "p" ;
    def stitch_type(self):
        self.expect(["k", "p"])
    

if __name__ == "__main__": 
    example = "k2, p2, k2"
    expected = ["k", "k", "p", "p", "k", "k"]


