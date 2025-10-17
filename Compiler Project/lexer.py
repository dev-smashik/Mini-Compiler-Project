"""
============================================
PHASE 1: LEXICAL ANALYZER (TOKENIZER)
CSE 430 - Compiler Design Lab
Name - Sheikh Muhammad Ashik
ID - 21201118
============================================
"""

import re
from typing import List


class Token:
    """Represents a single token"""
    def __init__(self, token_type: str, value: str, line: int):
        self.type = token_type
        self.value = value
        self.line = line
   
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', Line:{self.line})"


class Lexer:
    """Converts source code into tokens"""
   
    # Define token patterns
    TOKEN_PATTERNS = [
        ('COMMENT', r'//.*'),
        ('FLOAT_NUM', r'\d+\.\d+'),  # Must come before NUMBER
        ('NUMBER', r'\d+'),
        ('STRING', r'"[^"]*"'),  # String literals
        ('IF', r'\bif\b'),
        ('ELSE', r'\belse\b'),
        ('WHILE', r'\bwhile\b'),
        ('PRINT', r'\bprint\b'),
        ('INT', r'\bint\b'),
        ('FLOAT', r'\bfloat\b'),
        ('STRING_TYPE', r'\bstring\b'),
        ('RETURN', r'\breturn\b'),
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('EQ', r'=='),  # Must come before ASSIGN
        ('NEQ', r'!='),
        ('LTE', r'<='),
        ('GTE', r'>='),
        ('ASSIGN', r'='),
        ('LT', r'<'),
        ('GT', r'>'),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULT', r'\*'),
        ('DIV', r'/'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('SEMICOLON', r';'),
        ('WHITESPACE', r'[ \t]+'),
        ('NEWLINE', r'\n'),
    ]
   
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens = []
        self.line = 1
   
    def tokenize(self) -> List[Token]:
        """Tokenize the source code"""
        print("\n" + "="*50)
        print("PHASE 1: LEXICAL ANALYSIS")
        print("="*50)
       
        pos = 0
        while pos < len(self.source_code):
            match_found = False
           
            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source_code, pos)
               
                if match:
                    value = match.group(0)
                   
                    # Skip whitespace and comments
                    if token_type not in ['WHITESPACE', 'COMMENT']:
                        if token_type == 'NEWLINE':
                            self.line += 1
                        else:
                            token = Token(token_type, value, self.line)
                            self.tokens.append(token)
                    elif token_type == 'NEWLINE':
                        self.line += 1
                   
                    pos = match.end()
                    match_found = True
                    break
           
            if not match_found:
                raise SyntaxError(f"Invalid character '{self.source_code[pos]}' at line {self.line}")
       
        # Print tokens
        print("\nTokens Generated:")
        for token in self.tokens:
            print(f"  {token}")
       
        return self.tokens


# Testing function for Phase 1
def test_lexer(source_code: str):
    """Test lexical analyzer independently"""
    print("\n" + "="*60)
    print(" TESTING PHASE 1: LEXICAL ANALYZER")
    print("="*60)
    
    try:
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        print("\n✓ Lexical Analysis Successful!")
        return tokens
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None


if __name__ == "__main__":
    # Test code
    test_code = """
    float x = 10.7;
    int y = 20;
    string name = "Ashik";
    print(x + y);
    """
    
    test_lexer(test_code)
