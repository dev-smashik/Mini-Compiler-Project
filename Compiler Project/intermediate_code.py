"""
============================================
PHASE 4: INTERMEDIATE CODE GENERATOR
CSE 430 - Compiler Design Lab
Name - Sheikh Muhammad Ashik
ID - 21201118
============================================
"""

from typing import List, Dict
from parser import *


class IntermediateCode:
    """Generates Three-Address Code (TAC)"""
   
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0
        self.string_literals = {}
        self.string_count = 0
   
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
   
    def new_string_label(self, value):
        """Generate a label for string literal"""
        if value not in self.string_literals:
            label = f"str{self.string_count}"
            self.string_literals[value] = label
            self.string_count += 1
        return self.string_literals[value]
   
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
       
        if self.string_literals:
            print("\nString Literals:")
            print("-" * 50)
            for value, label in self.string_literals.items():
                print(f"{label}: \"{value}\"")
       
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
       
        elif isinstance(node, FloatNumber):
            return str(node.value)
       
        elif isinstance(node, StringLiteral):
            label = self.new_string_label(node.value)
            return label
       
        elif isinstance(node, Variable):
            return node.name
       
        elif isinstance(node, BinaryOp):
            left_temp = self.generate_expression(node.left)
            right_temp = self.generate_expression(node.right)
            result_temp = self.new_temp()
            self.emit(f"{result_temp} = {left_temp} {node.operator} {right_temp}")
            return result_temp
       
        return None


# Testing function for Phase 4
def test_intermediate_code(source_code: str, ast: Program = None):
    """Test intermediate code generator independently"""
    print("\n" + "="*60)
    print(" TESTING PHASE 4: INTERMEDIATE CODE GENERATOR")
    print("="*60)
    
    try:
        # If no AST provided, run previous phases
        if ast is None:
            from semantic_analyzer import test_semantic_analyzer
            symbol_table = test_semantic_analyzer(source_code)
            if symbol_table is None:
                return None, None
            # Get AST from parser
            from parser import test_parser
            from lexer import Lexer
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            from parser import Parser
            parser = Parser(tokens)
            ast = parser.parse()
        
        ic_generator = IntermediateCode()
        tac = ic_generator.generate(ast)
        print("\n✓ Intermediate Code Generation Successful!")
        return tac, ic_generator.string_literals
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None, None


if __name__ == "__main__":
    # Test code
    test_code = """
    float x = 10.7;
    int y = 20;
    float sum = x + y;
    print(sum);
    
    if (sum > 25) {
        print("Result is greater than 25");
    }
    """
    
    test_intermediate_code(test_code)
