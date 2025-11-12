"""A lexer to translate knitting patterns into primitive tokens, then recombine them into tokens to feed the parser

Primitive Tokens
----------------

primitve_word           = { ? alpha ? } ;
primitive_number        = { ? digit ? } ;
primitive_symbol        = "," | "*" | ":" | ";" ;
primitive_whitespace    = " " | "\t" ;
primitve_newline        = "\n" | "\r\n" ;

? alpha ? : Alphabetical letter
? digit ? : Numeric digit

Complex Tokens
--------------

complex_stitch  = primitive_word [ primitive_numbers primitive_word ] ;
complex_number  = primitive_number ;
complex_symbol  = primitive_symbol ;
complex_newline = primitive_newline ;
"""

from enum import Enum
from dataclasses import dataclass

class LexerError(Exception):
    """Exception raised for errors during lexing process"""
    def __init__(self, message):
        super().__init__(f"LEXING ERROR DETECTED:\n{message}")

class TokenType(Enum):
    WORD = "word"
    NUMBER = "number"
    SYMBOL = "symbol"
    NEWLINE = "newline"
    
    STITCH = "stitch"
    EOI = "? end of input ?"

@dataclass(frozen=True)
class Token:
    type:TokenType
    value:str

class Lexer:
    def __init__(self, text:str|None):
        """Initializes the lexer instance and gets the first
        position of the input text"""
        self.text = text
        self.pos = 0
        self._curr_char = text[0]

    def advance(self):
        """Advances the iteration along the characters of text"""
        self.pos += 1
        try:
            self._curr_char = self.text[self.pos]
        except IndexError:  # if there is no next character, you're on the EOI
            self._curr_char = None

    def look_ahead(self, x):
        """Look at the next x characters ahead of the current position"""
        if self.pos + x >= len(self.text):
            return None
        return self.text[self.pos+1:self.pos+x]
    
    def scan(self):
        """Read the given text and break it down into primitive tokens"""
        primitive_tokens = []
        while self.pos < len(self.text):
            # print(f"char is {self._curr_char}")
            # scan newlines
            if self._curr_char == '\n':
                primitive_tokens.append(Token(TokenType.NEWLINE, '\n'))
                self.advance()
                continue

            # skip whitespace
            if self._curr_char.isspace():   # NOTE: isspace consumes newlines, so put after that check
                self.advance()
                continue

            # scan letter sequences
            if self._curr_char.isalpha():
                # print("word found")
                primitive_tokens.append(self._tokenize_word())
                continue

            # scan number sequences
            if self._curr_char.isdigit():
                # print("number found")
                primitive_tokens.append(self._tokenize_number())
                continue

            if self._curr_char in [',', '*', ':', ';']:
                primitive_tokens.append(Token(TokenType.SYMBOL, self._curr_char))
                self.advance()
                continue
            
            # Unfamiliar token encountered
            raise LexerError(f"Found unknown token \"{self._curr_char}\"")
        
        primitive_tokens.append(Token(TokenType.EOI, None))

        return primitive_tokens

    def _tokenize_word(self):
        start_pos = self.pos

        while self.pos < len(self.text):    # iterate until you reach a non-letter
            if not self._curr_char.isalpha():
                break

            self.advance()

        word = self.text[start_pos:self.pos]
        return Token(TokenType.WORD, word)
    
    def _tokenize_number(self):
        start_pos = self.pos

        while self.pos < len(self.text):    # iterate until you reach a non-digit
            if not self._curr_char.isdigit():
                break

            self.advance()

        number = self.text[start_pos:self.pos]
        return Token(TokenType.NUMBER, number)
