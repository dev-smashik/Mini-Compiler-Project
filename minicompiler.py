# ============================================
# MINI COMPILER PROJECT
# CSE 430 - Compiler Design Lab
# Name - SHEIKH MUHAMMAD ASHIK
# ID - 21201118
# Section - C1
# ============================================

import re
from typing import List, Dict, Tuple

# ============================================
# PHASE 1: LEXICAL ANALYZER (TOKENIZER)
# ============================================

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
        ('NUMBER', r'\d+'),
        ('IF', r'\bif\b'),
        ('ELSE', r'\belse\b'),
        ('WHILE', r'\bwhile\b'),
        ('PRINT', r'\bprint\b'),
        ('INT', r'\bint\b'),
        ('RETURN', r'\breturn\b'),
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('ASSIGN', r'='),
        ('EQ', r'=='),
        ('NEQ', r'!='),
        ('LT', r'<'),
        ('GT', r'>'),
        ('LTE', r'<='),
        ('GTE', r'>='),
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

# ============================================
# PHASE 2: SYNTAX ANALYZER (PARSER)
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
        
        if token.type == 'INT':
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
        """Parse variable declaration: int x = 5;"""
        self.eat('INT')
        var_name = self.eat('ID').value
        
        value = None
        if self.current_token() and self.current_token().type == 'ASSIGN':
            self.eat('ASSIGN')
            value = self.parse_expression()
        
        self.eat('SEMICOLON')
        return Declaration('int', var_name, value)
    
    def parse_assignment(self):
        """Parse assignment: x = 10;"""
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
        """Parse factor (number or variable or parenthesized expression)"""
        token = self.current_token()
        
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(token.value)
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

# ============================================
# PHASE 3: SEMANTIC ANALYZER & SYMBOL TABLE
# ============================================

class SymbolTable:
    """Manages variable declarations and scope"""
    
    def __init__(self):
        self.symbols = {}
    
    def declare(self, name: str, var_type: str):
        if name in self.symbols:
            raise SemanticError(f"Variable '{name}' already declared")
        self.symbols[name] = {'type': var_type, 'initialized': False}
    
    def assign(self, name: str):
        if name not in self.symbols:
            raise SemanticError(f"Variable '{name}' not declared")
        self.symbols[name]['initialized'] = True
    
    def lookup(self, name: str):
        if name not in self.symbols:
            raise SemanticError(f"Variable '{name}' not declared")
        return self.symbols[name]
    
    def display(self):
        print("\nSymbol Table:")
        print("-" * 50)
        print(f"{'Variable':<15} {'Type':<10} {'Initialized':<15}")
        print("-" * 50)
        for name, info in self.symbols.items():
            print(f"{name:<15} {info['type']:<10} {str(info['initialized']):<15}")

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    """Performs semantic analysis and type checking"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
    
    def analyze(self, ast: Program):
        """Analyze the AST"""
        print("\n" + "="*50)
        print("PHASE 3: SEMANTIC ANALYSIS")
        print("="*50)
        
        for statement in ast.statements:
            self.analyze_statement(statement)
        
        self.symbol_table.display()
        print("\nSemantic Analysis completed successfully!")
        return self.symbol_table
    
    def analyze_statement(self, node):
        if isinstance(node, Declaration):
            self.symbol_table.declare(node.var_name, node.var_type)
            if node.value:
                self.analyze_expression(node.value)
                self.symbol_table.assign(node.var_name)
        elif isinstance(node, Assignment):
            self.symbol_table.lookup(node.var_name)
            self.analyze_expression(node.expression)
            self.symbol_table.assign(node.var_name)
        elif isinstance(node, IfStatement):
            self.analyze_expression(node.condition)
            for stmt in node.true_block:
                self.analyze_statement(stmt)
            if node.false_block:
                for stmt in node.false_block:
                    self.analyze_statement(stmt)
        elif isinstance(node, WhileLoop):
            self.analyze_expression(node.condition)
            for stmt in node.body:
                self.analyze_statement(stmt)
        elif isinstance(node, PrintStatement):
            self.analyze_expression(node.expression)
    
    def analyze_expression(self, node):
        if isinstance(node, Number):
            return
        elif isinstance(node, Variable):
            self.symbol_table.lookup(node.name)
        elif isinstance(node, BinaryOp):
            self.analyze_expression(node.left)
            self.analyze_expression(node.right)

# ============================================
# PHASE 4: INTERMEDIATE CODE GENERATOR
# ============================================

class IntermediateCode:
    """Generates Three-Address Code (TAC)"""
    
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0
    
    def new_temp(self):
        """Generate a new temporary variable"""
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def new_label(self):
        """Generate a new label"""
        label = f"L{self.label_count}"
        self.label_count += 1
        return label
    
    def emit(self, instruction):
        """Add instruction to code list"""
        self.code.append(instruction)
    
    def generate(self, ast: Program):
        """Generate intermediate code"""
        print("\n" + "="*50)
        print("PHASE 4: INTERMEDIATE CODE GENERATION")
        print("="*50)
        
        for statement in ast.statements:
            self.generate_statement(statement)
        
        print("\nThree-Address Code (TAC):")
        print("-" * 50)
        for i, instruction in enumerate(self.code, 1):
            print(f"{i:3d}. {instruction}")
        
        return self.code
    
    def generate_statement(self, node):
        if isinstance(node, Declaration):
            if node.value:
                temp = self.generate_expression(node.value)
                self.emit(f"{node.var_name} = {temp}")
        
        elif isinstance(node, Assignment):
            temp = self.generate_expression(node.expression)
            self.emit(f"{node.var_name} = {temp}")
        
        elif isinstance(node, PrintStatement):
            temp = self.generate_expression(node.expression)
            self.emit(f"print {temp}")
        
        elif isinstance(node, IfStatement):
            cond_temp = self.generate_expression(node.condition)
            false_label = self.new_label()
            end_label = self.new_label()
            
            self.emit(f"if_false {cond_temp} goto {false_label}")
            
            for stmt in node.true_block:
                self.generate_statement(stmt)
            
            self.emit(f"goto {end_label}")
            self.emit(f"{false_label}:")
            
            if node.false_block:
                for stmt in node.false_block:
                    self.generate_statement(stmt)
            
            self.emit(f"{end_label}:")
        
        elif isinstance(node, WhileLoop):
            start_label = self.new_label()
            end_label = self.new_label()
            
            self.emit(f"{start_label}:")
            cond_temp = self.generate_expression(node.condition)
            self.emit(f"if_false {cond_temp} goto {end_label}")
            
            for stmt in node.body:
                self.generate_statement(stmt)
            
            self.emit(f"goto {start_label}")
            self.emit(f"{end_label}:")
    
    def generate_expression(self, node):
        if isinstance(node, Number):
            return str(node.value)
        
        elif isinstance(node, Variable):
            return node.name
        
        elif isinstance(node, BinaryOp):
            left_temp = self.generate_expression(node.left)
            right_temp = self.generate_expression(node.right)
            result_temp = self.new_temp()
            self.emit(f"{result_temp} = {left_temp} {node.operator} {right_temp}")
            return result_temp
        
        return None

# ============================================
# PHASE 5: CODE GENERATOR (ASSEMBLY)
# ============================================

class AssemblyGenerator:
    """Generates simple assembly code from intermediate code"""
    
    def __init__(self, tac: List[str], symbol_table: SymbolTable):
        self.tac = tac
        self.symbol_table = symbol_table
        self.assembly = []
        self.data_section = []
    
    def generate(self):
        """Generate assembly code"""
        print("\n" + "="*50)
        print("PHASE 5: CODE GENERATION (ASSEMBLY)")
        print("="*50)
        
        # Data section - declare variables
        self.assembly.append("; Data Section")
        self.assembly.append("section .data")
        
        for var_name in self.symbol_table.symbols:
            self.assembly.append(f"    {var_name} dd 0    ; int variable")
        
        self.assembly.append("")
        self.assembly.append("; BSS Section (temporary variables)")
        self.assembly.append("section .bss")
        
        # Count temporaries
        temp_count = max([int(instr.split('t')[1].split()[0]) 
                         for instr in self.tac 
                         if 't' in instr and instr.split()[0].startswith('t')], default=-1) + 1
        
        for i in range(temp_count):
            self.assembly.append(f"    t{i} resd 1")
        
        # Code section
        self.assembly.append("")
        self.assembly.append("; Code Section")
        self.assembly.append("section .text")
        self.assembly.append("global _start")
        self.assembly.append("")
        self.assembly.append("_start:")
        
        # Convert TAC to assembly
        for instruction in self.tac:
            self.convert_instruction(instruction)
        
        # Exit program
        self.assembly.append("")
        self.assembly.append("    ; Exit program")
        self.assembly.append("    mov eax, 1      ; sys_exit")
        self.assembly.append("    xor ebx, ebx    ; exit code 0")
        self.assembly.append("    int 0x80")
        
        # Print assembly
        print("\nGenerated Assembly Code:")
        print("-" * 50)
        for line in self.assembly:
            print(line)
        
        return self.assembly
    
    def convert_instruction(self, instruction: str):
        """Convert single TAC instruction to assembly"""
        parts = instruction.split()
        
        if '=' in instruction and len(parts) == 3:
            # Simple assignment: x = y
            dest, _, src = parts
            self.assembly.append(f"    mov eax, [{src}]")
            self.assembly.append(f"    mov [{dest}], eax")
        
        elif '=' in instruction and len(parts) == 5:
            # Binary operation: t0 = x + y
            dest, _, left, op, right = parts
            
            self.assembly.append(f"    mov eax, [{left}]")
            self.assembly.append(f"    mov ebx, [{right}]")
            
            if op == '+':
                self.assembly.append(f"    add eax, ebx")
            elif op == '-':
                self.assembly.append(f"    sub eax, ebx")
            elif op == '*':
                self.assembly.append(f"    imul eax, ebx")
            elif op == '/':
                self.assembly.append(f"    cdq")
                self.assembly.append(f"    idiv ebx")
            elif op in ['<', '>', '==', '!=', '<=', '>=']:
                self.assembly.append(f"    cmp eax, ebx")
                if op == '<':
                    self.assembly.append(f"    setl al")
                elif op == '>':
                    self.assembly.append(f"    setg al")
                elif op == '==':
                    self.assembly.append(f"    sete al")
                elif op == '!=':
                    self.assembly.append(f"    setne al")
                elif op == '<=':
                    self.assembly.append(f"    setle al")
                elif op == '>=':
                    self.assembly.append(f"    setge al")
                self.assembly.append(f"    movzx eax, al")
            
            self.assembly.append(f"    mov [{dest}], eax")
        
        elif instruction.startswith('print'):
            # Print statement
            var = parts[1]
            self.assembly.append(f"    ; Print {var}")
            self.assembly.append(f"    mov eax, [{var}]")
            self.assembly.append(f"    ; (print syscall would go here)")
        
        elif instruction.startswith('if_false'):
            # Conditional jump
            _, cond, _, label = parts
            self.assembly.append(f"    mov eax, [{cond}]")
            self.assembly.append(f"    cmp eax, 0")
            self.assembly.append(f"    je {label}")
        
        elif instruction.startswith('goto'):
            # Unconditional jump
            label = parts[1]
            self.assembly.append(f"    jmp {label}")
        
        elif instruction.endswith(':'):
            # Label
            self.assembly.append(f"{instruction}")

# ============================================
# MAIN COMPILER DRIVER
# ============================================

class Compiler:
    """Main compiler class that orchestrates all phases"""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
    
    def compile(self):
        """Run all compilation phases"""
        print("\n" + "="*60)
        print(" MINI COMPILER - CSE 430 Project")
        print("="*60)
        
        try:
            # Phase 1: Lexical Analysis
            lexer = Lexer(self.source_code)
            tokens = lexer.tokenize()
            
            # Phase 2: Syntax Analysis
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Phase 3: Semantic Analysis
            semantic_analyzer = SemanticAnalyzer()
            symbol_table = semantic_analyzer.analyze(ast)
            
            # Phase 4: Intermediate Code Generation
            ic_generator = IntermediateCode()
            tac = ic_generator.generate(ast)
            
            # Phase 5: Code Generation
            asm_generator = AssemblyGenerator(tac, symbol_table)
            assembly = asm_generator.generate()
            
            print("\n" + "="*60)
            print(" COMPILATION SUCCESSFUL!")
            print("="*60)
            
            return {
                'tokens': tokens,
                'ast': ast,
                'symbol_table': symbol_table,
                'intermediate_code': tac,
                'assembly': assembly
            }
        
        except (SyntaxError, SemanticError) as e:
            print(f"\n ERROR: {e}")
            return None

# ============================================
# TEST PROGRAM
# ============================================

if __name__ == "__main__":
    # Sample program in our custom language
    source_code = """
    int x = 10;
    int y = 20;
    int sum = x + y;
    print(sum);
    
    int i = 0;
    while (i < 5) {
        print(i);
        i = i + 1;
    }
    
    if (sum > 25) {
        print(sum);
        print(sum+15);
    }
    """
    
    # Compile the source code
    compiler = Compiler(source_code)
    result = compiler.compile()
