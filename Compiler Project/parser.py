"""
============================================
PHASE 2: SYNTAX ANALYZER (PARSER)
CSE 430 - Compiler Design Lab
Name - Sheikh Muhammad Ashik
ID - 21201118
============================================
"""

from typing import List
from lexer import Token, Lexer


# ============================================
# AST NODE CLASSES
# ============================================

class ASTNode:
    """Base class for Abstract Syntax Tree nodes"""
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class Declaration(ASTNode):
    def __init__(self, var_type, var_name, value=None):
        self.var_type = var_type
        self.var_name = var_name
        self.value = value


class Assignment(ASTNode):
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression


class BinaryOp(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Number(ASTNode):
    def __init__(self, value):
        self.value = int(value)


class FloatNumber(ASTNode):
    def __init__(self, value):
        self.value = float(value)


class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value.strip('"')  # Remove quotes


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name


class IfStatement(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block


class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class PrintStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression


# ============================================
# PARSER CLASS
# ============================================

class Parser:
    """Parses tokens into Abstract Syntax Tree"""
   
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
   
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
   
    def eat(self, token_type: str):
        """Consume a token of expected type"""
        token = self.current_token()
        if token and token.type == token_type:
            self.pos += 1
            return token
        raise SyntaxError(f"Expected {token_type}, got {token.type if token else 'EOF'}")
   
    def parse(self) -> Program:
        """Parse the entire program"""
        print("\n" + "="*50)
        print("PHASE 2: SYNTAX ANALYSIS (PARSING)")
        print("="*50)
       
        statements = []
        while self.current_token():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
       
        ast = Program(statements)
        print("\nAbstract Syntax Tree (AST) created successfully!")
        self.print_ast(ast)
        return ast
   
    def parse_statement(self):
        """Parse a single statement"""
        token = self.current_token()
       
        if not token:
            return None
       
        if token.type in ['INT', 'FLOAT', 'STRING_TYPE']:
            return self.parse_declaration()
        elif token.type == 'ID':
            return self.parse_assignment()
        elif token.type == 'IF':
            return self.parse_if()
        elif token.type == 'WHILE':
            return self.parse_while()
        elif token.type == 'PRINT':
            return self.parse_print()
        else:
            raise SyntaxError(f"Unexpected token {token.type}")
   
    def parse_declaration(self):
        """Parse variable declaration"""
        type_token = self.current_token()
        var_type = type_token.value
        self.eat(type_token.type)
       
        var_name = self.eat('ID').value
       
        value = None
        if self.current_token() and self.current_token().type == 'ASSIGN':
            self.eat('ASSIGN')
            value = self.parse_expression()
       
        self.eat('SEMICOLON')
        return Declaration(var_type, var_name, value)
   
    def parse_assignment(self):
        """Parse assignment"""
        var_name = self.eat('ID').value
        self.eat('ASSIGN')
        expression = self.parse_expression()
        self.eat('SEMICOLON')
        return Assignment(var_name, expression)
   
    def parse_if(self):
        """Parse if statement"""
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
       
        true_block = []
        while self.current_token() and self.current_token().type != 'RBRACE':
            true_block.append(self.parse_statement())
        self.eat('RBRACE')
       
        false_block = None
        if self.current_token() and self.current_token().type == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            false_block = []
            while self.current_token() and self.current_token().type != 'RBRACE':
                false_block.append(self.parse_statement())
            self.eat('RBRACE')
       
        return IfStatement(condition, true_block, false_block)
   
    def parse_while(self):
        """Parse while loop"""
        self.eat('WHILE')
        self.eat('LPAREN')
        condition = self.parse_expression()
        self.eat('RPAREN')
        self.eat('LBRACE')
       
        body = []
        while self.current_token() and self.current_token().type != 'RBRACE':
            body.append(self.parse_statement())
        self.eat('RBRACE')
       
        return WhileLoop(condition, body)
   
    def parse_print(self):
        """Parse print statement"""
        self.eat('PRINT')
        self.eat('LPAREN')
        expression = self.parse_expression()
        self.eat('RPAREN')
        self.eat('SEMICOLON')
        return PrintStatement(expression)
   
    def parse_expression(self):
        """Parse expression with operators"""
        left = self.parse_term()
       
        while self.current_token() and self.current_token().type in ['PLUS', 'MINUS', 'LT', 'GT', 'EQ', 'NEQ', 'LTE', 'GTE']:
            op = self.eat(self.current_token().type).value
            right = self.parse_term()
            left = BinaryOp(left, op, right)
       
        return left
   
    def parse_term(self):
        """Parse term (multiplication/division)"""
        left = self.parse_factor()
       
        while self.current_token() and self.current_token().type in ['MULT', 'DIV']:
            op = self.eat(self.current_token().type).value
            right = self.parse_factor()
            left = BinaryOp(left, op, right)
       
        return left
   
    def parse_factor(self):
        """Parse factor"""
        token = self.current_token()
       
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(token.value)
        elif token.type == 'FLOAT_NUM':
            self.eat('FLOAT_NUM')
            return FloatNumber(token.value)
        elif token.type == 'STRING':
            self.eat('STRING')
            return StringLiteral(token.value)
        elif token.type == 'ID':
            self.eat('ID')
            return Variable(token.value)
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {token.type}")
   
    def print_ast(self, node, indent=0):
        """Print AST structure"""
        prefix = "  " * indent
        if isinstance(node, Program):
            print(f"\n{prefix}Program:")
            for stmt in node.statements:
                self.print_ast(stmt, indent + 1)
        elif isinstance(node, Declaration):
            print(f"{prefix}Declaration: {node.var_type} {node.var_name}")
            if node.value:
                self.print_ast(node.value, indent + 1)
        elif isinstance(node, Assignment):
            print(f"{prefix}Assignment: {node.var_name} =")
            self.print_ast(node.expression, indent + 1)
        elif isinstance(node, BinaryOp):
            print(f"{prefix}BinaryOp: {node.operator}")
            self.print_ast(node.left, indent + 1)
            self.print_ast(node.right, indent + 1)
        elif isinstance(node, Number):
            print(f"{prefix}Number: {node.value}")
        elif isinstance(node, FloatNumber):
            print(f"{prefix}Float: {node.value}")
        elif isinstance(node, StringLiteral):
            print(f"{prefix}String: \"{node.value}\"")
        elif isinstance(node, Variable):
            print(f"{prefix}Variable: {node.name}")
        elif isinstance(node, PrintStatement):
            print(f"{prefix}Print:")
            self.print_ast(node.expression, indent + 1)
        elif isinstance(node, IfStatement):
            print(f"{prefix}If Statement:")
            self.print_ast(node.condition, indent + 1)
            for stmt in node.true_block:
                self.print_ast(stmt, indent + 1)
        elif isinstance(node, WhileLoop):
            print(f"{prefix}While Loop:")
            self.print_ast(node.condition, indent + 1)
            for stmt in node.body:
                self.print_ast(stmt, indent + 1)


# Testing function for Phase 2
def test_parser(source_code: str, tokens: List[Token] = None):
    """Test syntax analyzer independently"""
    print("\n" + "="*60)
    print(" TESTING PHASE 2: SYNTAX ANALYZER")
    print("="*60)
    
    try:
        # If no tokens provided, run lexer first
        if tokens is None:
            from lexer import test_lexer
            tokens = test_lexer(source_code)
            if tokens is None:
                return None
        
        parser = Parser(tokens)
        ast = parser.parse()
        print("\n✓ Syntax Analysis Successful!")
        return ast
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None


if __name__ == "__main__":
    # Test code
    test_code = """
    float x = 10.7;
    int y = 20;
    print(x + y);
    """
    
    test_parser(test_code)
