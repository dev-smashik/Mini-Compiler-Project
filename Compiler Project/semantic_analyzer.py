"""
============================================
PHASE 3: SEMANTIC ANALYZER & SYMBOL TABLE
CSE 430 - Compiler Design Lab
Name - Sheikh Muhammad Ashik
ID - 21201118
============================================
"""

from parser import *


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
   
    def get_type(self, name: str):
        """Get the type of a variable"""
        if name in self.symbols:
            return self.symbols[name]['type']
        return None
   
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
        if isinstance(node, (Number, FloatNumber, StringLiteral)):
            return
        elif isinstance(node, Variable):
            self.symbol_table.lookup(node.name)
        elif isinstance(node, BinaryOp):
            self.analyze_expression(node.left)
            self.analyze_expression(node.right)


# Testing function for Phase 3
def test_semantic_analyzer(source_code: str, ast: Program = None):
    """Test semantic analyzer independently"""
    print("\n" + "="*60)
    print(" TESTING PHASE 3: SEMANTIC ANALYZER")
    print("="*60)
    
    try:
        # If no AST provided, run lexer and parser first
        if ast is None:
            from parser import test_parser
            ast = test_parser(source_code)
            if ast is None:
                return None
        
        analyzer = SemanticAnalyzer()
        symbol_table = analyzer.analyze(ast)
        print("\n✓ Semantic Analysis Successful!")
        return symbol_table
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None


if __name__ == "__main__":
    # Test code
    test_code = """
    float x = 10.7;
    int y = 20;
    float sum = x + y;
    print(sum);
    """
    
    test_semantic_analyzer(test_code)
