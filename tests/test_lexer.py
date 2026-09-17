import unittest
import os
from lexer.tokens import TokenType
from lexer.config import KeywordConfig
from lexer.lexer import Lexer, LexicalError

class TestLexer(unittest.TestCase):
    def setUp(self):
        # Create temporary config files for testing
        self.default_config_data = {
            "let": "LET", "print": "PRINT", "if": "IF", 
            "else": "ELSE", "while": "WHILE", "true": "TRUE", "false": "FALSE"
        }
        self.custom_config_data = {
            "create": "LET", "show": "PRINT", "when": "IF", 
            "otherwise": "ELSE", "repeat": "WHILE", "yes": "TRUE", "no": "FALSE"
        }
        
        # We can just manually inject dicts into KeywordConfig instead of writing files for unit testing
        self.default_config = KeywordConfig()
        self.default_config.validate_and_load(self.default_config_data)
        
        self.custom_config = KeywordConfig()
        self.custom_config.validate_and_load(self.custom_config_data)

    def test_1_default_keywords(self):
        source = "let print if else while true false"
        lexer = Lexer(source, self.default_config)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertEqual(types, [
            TokenType.LET, TokenType.PRINT, TokenType.IF, 
            TokenType.ELSE, TokenType.WHILE, TokenType.TRUE, 
            TokenType.FALSE, TokenType.EOF
        ])

    def test_2_custom_keywords(self):
        source = "create show when otherwise repeat yes no"
        lexer = Lexer(source, self.custom_config)
        tokens = lexer.tokenize()
        types = [t.type for t in tokens]
        self.assertEqual(types, [
            TokenType.LET, TokenType.PRINT, TokenType.IF, 
            TokenType.ELSE, TokenType.WHILE, TokenType.TRUE, 
            TokenType.FALSE, TokenType.EOF
        ])

    def test_3_identifiers(self):
        source = "x total my_var2"
        lexer = Lexer(source, self.default_config)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].lexeme, "x")
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].lexeme, "total")
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].lexeme, "my_var2")

    def test_4_integers(self):
        source = "10 0 999"
        lexer = Lexer(source, self.default_config)
        tokens = lexer.tokenize()
        self.assertEqual([t.lexeme for t in tokens[:-1]], ["10", "0", "999"])
        self.assertTrue(all(t.type == TokenType.NUMBER for t in tokens[:-1]))

    def test_5_floating_point_numbers(self):
        source = "10.5 3.14 0.25"
        lexer = Lexer(source, self.default_config)
        tokens = lexer.tokenize()
        self.assertEqual([t.lexeme for t in tokens[:-1]], ["10.5", "3.14", "0.25"])
        self.assertTrue(all(t.type == TokenType.NUMBER for t in tokens[:-1]))
        
        # Test malformed number
        lexer = Lexer("12.34.56", self.default_config)
        with self.assertRaisesRegex(LexicalError, "Malformed number"):
            lexer.tokenize()

    def test_6_arithmetic_operators(self):
        source = "+ - * /"
        lexer = Lexer(source, self.default_config)
        types = [t.type for t in lexer.tokenize()]
        self.assertEqual(types, [
            TokenType.PLUS, TokenType.MINUS, 
            TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.EOF
        ])

    def test_7_relational_operators(self):
        source = "< > == != <= >="
        lexer = Lexer(source, self.default_config)
        types = [t.type for t in lexer.tokenize()]
        self.assertEqual(types, [
            TokenType.LESS_THAN, TokenType.GREATER_THAN, 
            TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL, 
            TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL, TokenType.EOF
        ])

    def test_8_assignment(self):
        source = "x = 5;"
        lexer = Lexer(source, self.default_config)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[1].type, TokenType.ASSIGN)

    def test_9_parentheses_and_braces(self):
        source = "( ) { }"
        lexer = Lexer(source, self.default_config)
        types = [t.type for t in lexer.tokenize()]
        self.assertEqual(types, [
            TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN, 
            TokenType.LEFT_BRACE, TokenType.RIGHT_BRACE, TokenType.EOF
        ])

    def test_10_semicolons(self):
        source = "; ;"
        lexer = Lexer(source, self.default_config)
        types = [t.type for t in lexer.tokenize()]
        self.assertEqual(types, [TokenType.SEMICOLON, TokenType.SEMICOLON, TokenType.EOF])

    def test_11_whitespace(self):
        source = "  \n\t  let  \t \n x = 5 ;  "
        lexer = Lexer(source, self.default_config)
        types = [t.type for t in lexer.tokenize()]
        self.assertEqual(types, [
            TokenType.LET, TokenType.IDENTIFIER, 
            TokenType.ASSIGN, TokenType.NUMBER, 
            TokenType.SEMICOLON, TokenType.EOF
        ])

    def test_12_comments(self):
        source = "let x = 5; // this is a comment\n let y = 10;"
        lexer = Lexer(source, self.default_config)
        types = [t.type for t in lexer.tokenize()]
        self.assertEqual(types, [
            TokenType.LET, TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.NUMBER, TokenType.SEMICOLON,
            TokenType.LET, TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.NUMBER, TokenType.SEMICOLON,
            TokenType.EOF
        ])

    def test_13_invalid_characters(self):
        source = "let x = 10 @ 20;"
        lexer = Lexer(source, self.default_config)
        with self.assertRaisesRegex(LexicalError, "Unexpected character '@'"):
            lexer.tokenize()

    def test_14_invalid_keyword_configuration(self):
        config = KeywordConfig()
        
        # Test unknown token type
        with self.assertRaisesRegex(ValueError, "Unknown token type: LOOP"):
            config.validate_and_load({"repeat": "LOOP"})
            
        # Test conflicting keywords
        with self.assertRaisesRegex(ValueError, "conflicts with another keyword definition"):
            config.validate_and_load({"create": "LET", "let": "LET"})
            
        # Test empty keyword
        with self.assertRaisesRegex(ValueError, "contains empty surface word"):
            config.validate_and_load({"": "LET"})
            
        # Test invalid character in keyword
        with self.assertRaisesRegex(ValueError, "contains invalid characters"):
            config.validate_and_load({"cre@te": "LET"})

    def test_15_same_program_semantics(self):
        default_source = "let x = 10; while (x > 0) { print x; x = x - 1; }"
        custom_source = "create x = 10; repeat (x > 0) { show x; x = x - 1; }"
        
        default_lexer = Lexer(default_source, self.default_config)
        custom_lexer = Lexer(custom_source, self.custom_config)
        
        default_types = [t.type for t in default_lexer.tokenize()]
        custom_types = [t.type for t in custom_lexer.tokenize()]
        
        self.assertEqual(default_types, custom_types)

if __name__ == '__main__':
    unittest.main()
