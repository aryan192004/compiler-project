from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    # Keywords
    LET = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    TRUE = auto()
    FALSE = auto()

    # Types
    IDENTIFIER = auto()
    NUMBER = auto()      # Used for both integers and floats in this simple lexer

    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    
    # Assignment
    ASSIGN = auto()

    # Relational Operators
    LESS_THAN = auto()
    GREATER_THAN = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    # Punctuation
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    SEMICOLON = auto()

    # End of File
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

    def __str__(self):
        return f"{self.type.name:<12} {self.lexeme}"

    def detailed_str(self):
        return f"{self.type.name:<12} \"{self.lexeme}\" line={self.line} column={self.column}"
