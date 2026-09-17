from .tokens import Token, TokenType
from .config import KeywordConfig

class LexicalError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"Lexical Error:\n{message}\nLine: {line}\nColumn: {column}")
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, source: str, keyword_config: KeywordConfig):
        self.source = source
        self.keyword_config = keyword_config
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[self.pos] if self.pos < len(self.source) else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.source):
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
            self.current_char = self.source[self.pos]
            self.column += 1
        else:
            self.current_char = None

    def peek(self) -> str | None:
        peek_pos = self.pos + 1
        if peek_pos < len(self.source):
            return self.source[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def number(self) -> Token:
        start_col = self.column
        result = ''
        dot_count = 0
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                dot_count += 1
                if dot_count > 1:
                    # Malformed number like 12.34.56
                    # Collect the rest to form a full malformed token for error
                    while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
                        result += self.current_char
                        self.advance()
                    raise LexicalError(f"Malformed number '{result}'", self.line, start_col)
            
            result += self.current_char
            self.advance()
            
        return Token(type=TokenType.NUMBER, lexeme=result, line=self.line, column=start_col)

    def identifier_or_keyword(self) -> Token:
        start_col = self.column
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
            
        # Check if it's a keyword
        token_type = self.keyword_config.get_token_type(result)
        if token_type is not None:
            return Token(type=token_type, lexeme=result, line=self.line, column=start_col)
            
        return Token(type=TokenType.IDENTIFIER, lexeme=result, line=self.line, column=start_col)

    def get_next_token(self) -> Token:
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char == '/' and self.peek() == '/':
                self.advance() # consume first '/'
                self.advance() # consume second '/'
                self.skip_comment()
                continue
                
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier_or_keyword()
                
            if self.current_char.isdigit():
                return self.number()
                
            # Operators and punctuation
            start_col = self.column
            char = self.current_char
            
            if char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQUAL_EQUAL, '==', self.line, start_col)
                return Token(TokenType.ASSIGN, '=', self.line, start_col)
                
            if char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LESS_EQUAL, '<=', self.line, start_col)
                return Token(TokenType.LESS_THAN, '<', self.line, start_col)
                
            if char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GREATER_EQUAL, '>=', self.line, start_col)
                return Token(TokenType.GREATER_THAN, '>', self.line, start_col)
                
            if char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NOT_EQUAL, '!=', self.line, start_col)
                raise LexicalError(f"Unexpected character '!'", self.line, start_col)

            # Single char operators and punctuation
            single_char_tokens = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '(': TokenType.LEFT_PAREN,
                ')': TokenType.RIGHT_PAREN,
                '{': TokenType.LEFT_BRACE,
                '}': TokenType.RIGHT_BRACE,
                ';': TokenType.SEMICOLON
            }
            
            if char in single_char_tokens:
                self.advance()
                return Token(single_char_tokens[char], char, self.line, start_col)
                
            # Unknown character
            error_char = self.current_char
            error_col = self.column
            self.advance() # advance to avoid infinite loop if called again
            raise LexicalError(f"Unexpected character '{error_char}'", self.line, error_col)
            
        return Token(TokenType.EOF, 'EOF', self.line, self.column)

    def tokenize(self) -> list[Token]:
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
