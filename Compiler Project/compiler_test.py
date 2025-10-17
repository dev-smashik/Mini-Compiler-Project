"""
============================================
PROJECT: MINI COMPILER TESTING FRAMEWORK
CSE 430 - Compiler Design Lab
Creator Name - Sheikh Muhammad Ashik
ID - 21201118
============================================

This module allows testing from any phase of the compiler:
- Phase 1: Lexical Analysis only
- Phase 2: Lexical + Syntax Analysis
- Phase 3: Up to Semantic Analysis
- Phase 4: Up to Intermediate Code Generation
- Phase 5: Complete compilation (all phases)
"""

from lexer import Lexer, test_lexer
from parser import Parser, test_parser
from semantic_analyzer import SemanticAnalyzer, test_semantic_analyzer
from intermediate_code import IntermediateCode, test_intermediate_code
from code_generator import AssemblyGenerator, test_code_generator


class Compiler:
    """Main compiler class that orchestrates all phases"""
   
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens = None
        self.ast = None
        self.symbol_table = None
        self.tac = None
        self.string_literals = None
        self.assembly = None
   
    def compile(self, stop_at_phase: int = 5):
        """
        Run compilation phases up to specified phase
        
        Parameters:
        -----------
        stop_at_phase : int
            1 = Lexical Analysis only
            2 = Up to Syntax Analysis
            3 = Up to Semantic Analysis
            4 = Up to Intermediate Code Generation
            5 = Complete compilation (all phases)
        """
        print("\n" + "="*60)
        print("MINI COMPILER - CSE 430 Project")
        print(f" Running up to Phase {stop_at_phase}")
        print("="*60)
       
        try:
            # Phase 1: Lexical Analysis
            if stop_at_phase >= 1:
                lexer = Lexer(self.source_code)
                self.tokens = lexer.tokenize()
                
                if stop_at_phase == 1:
                    print("\n" + "="*60)
                    print(" PHASE 1 COMPLETED SUCCESSFULLY!")
                    print("="*60)
                    return {'phase': 1, 'tokens': self.tokens}
           
            # Phase 2: Syntax Analysis
            if stop_at_phase >= 2:
                parser = Parser(self.tokens)
                self.ast = parser.parse()
                
                if stop_at_phase == 2:
                    print("\n" + "="*60)
                    print(" PHASES 1-2 COMPLETED SUCCESSFULLY!")
                    print("="*60)
                    return {
                        'phase': 2,
                        'tokens': self.tokens,
                        'ast': self.ast
                    }
           
            # Phase 3: Semantic Analysis
            if stop_at_phase >= 3:
                semantic_analyzer = SemanticAnalyzer()
                self.symbol_table = semantic_analyzer.analyze(self.ast)
                
                if stop_at_phase == 3:
                    print("\n" + "="*60)
                    print(" PHASES 1-3 COMPLETED SUCCESSFULLY!")
                    print("="*60)
                    return {
                        'phase': 3,
                        'tokens': self.tokens,
                        'ast': self.ast,
                        'symbol_table': self.symbol_table
                    }
           
            # Phase 4: Intermediate Code Generation
            if stop_at_phase >= 4:
                ic_generator = IntermediateCode()
                self.tac = ic_generator.generate(self.ast)
                self.string_literals = ic_generator.string_literals
                
                if stop_at_phase == 4:
                    print("\n" + "="*60)
                    print(" PHASES 1-4 COMPLETED SUCCESSFULLY!")
                    print("="*60)
                    return {
                        'phase': 4,
                        'tokens': self.tokens,
                        'ast': self.ast,
                        'symbol_table': self.symbol_table,
                        'intermediate_code': self.tac,
                        'string_literals': self.string_literals
                    }
           
            # Phase 5: Code Generation
            if stop_at_phase >= 5:
                asm_generator = AssemblyGenerator(self.tac, self.symbol_table, 
                                                  self.string_literals)
                self.assembly = asm_generator.generate()
           
                print("\n" + "="*60)
                print(" ALL PHASES COMPLETED SUCCESSFULLY!")
                print("="*60)
                return {
                    'phase': 5,
                    'tokens': self.tokens,
                    'ast': self.ast,
                    'symbol_table': self.symbol_table,
                    'intermediate_code': self.tac,
                    'string_literals': self.string_literals,
                    'assembly': self.assembly
                }
       
        except Exception as e:
            print(f"\n ERROR: {e}")
            return None



# ============================================
# MAIN MENU FOR INTERACTIVE TESTING
# ============================================

def main_menu():
    """Interactive menu for testing"""
    while True:
        print("\n" + "="*70)
        print(" COMPILER TESTING MENU")
        print("="*70)
        print("\nx. Enter Custom Code")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            print("\nExiting... Goodbye!")
            break
        elif choice in ["1", "2", "3", "4", "5"]:
            phase = int(choice)
            print("\nEnter your source code (type 'END' on a new line to finish):")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            code = "\n".join(lines)
            
            compiler = Compiler(code)
        elif choice == "x":
            print("\nEnter phase to run (1-5): ", end="")
            print("\n1. Test Phase 1 - Lexical Analysis Only")
            print("2. Test Phase 2 - Up to Syntax Analysis")
            print("3. Test Phase 3 - Up to Semantic Analysis")
            print("4. Test Phase 4 - Up to Intermediate Code Generation")
            print("5. Test Phase 5 - Complete Compilation (All Phases)")
            phase = int(input("Enter your choice: ").strip())
            print("\nEnter your source code (type 'END' on a new line to finish):")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            code = "\n".join(lines)
            
            compiler = Compiler(code)
            compiler.compile(stop_at_phase=phase)
        else:
            print("\nInvalid choice! Please try again.")
        
        input("\nPress Enter to continue...")


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    main_menu()