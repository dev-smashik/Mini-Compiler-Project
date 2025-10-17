"""
============================================
PHASE 5: CODE GENERATOR (ASSEMBLY)
CSE 430 - Compiler Design Lab
Name - Sheikh Muhammad Ashik
ID - 21201118
============================================
"""

from typing import List, Dict
from semantic_analyzer import SymbolTable


class AssemblyGenerator:
    """Generates simple assembly code from intermediate code"""
   
    def __init__(self, tac: List[str], symbol_table: SymbolTable, string_literals: Dict):
        self.tac = tac
        self.symbol_table = symbol_table
        self.string_literals = string_literals
        self.assembly = []
   
    def generate(self):
        """Generate assembly code"""
        print("\n" + "="*50)
        print("PHASE 5: CODE GENERATION (ASSEMBLY)")
        print("="*50)
       
        # Data section - declare variables and strings
        self.assembly.append("; Data Section")
        self.assembly.append("section .data")
       
        # String literals
        for value, label in self.string_literals.items():
            self.assembly.append(f"    {label} db \"{value}\", 0")
       
        if self.string_literals:
            self.assembly.append("")
       
        # Variables
        for var_name, info in self.symbol_table.symbols.items():
            if info['type'] == 'int':
                self.assembly.append(f"    {var_name} dd 0    ; int variable")
            elif info['type'] == 'float':
                self.assembly.append(f"    {var_name} dq 0.0  ; float variable")
            elif info['type'] == 'string':
                self.assembly.append(f"    {var_name} dd 0    ; string pointer")
       
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
            # Simple assignment: x = y or x = str0
            dest, _, src = parts
           
            # Check if source is a string literal
            if src.startswith('str'):
                self.assembly.append(f"    lea eax, [{src}]")
                self.assembly.append(f"    mov [{dest}], eax")
            else:
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
            if var.startswith('str'):
                self.assembly.append(f"    lea eax, [{var}]")
            else:
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


# Testing function for Phase 5
def test_code_generator(source_code: str, tac: List[str] = None, 
                       symbol_table: SymbolTable = None, 
                       string_literals: Dict = None):
    """Test assembly code generator independently"""
    print("\n" + "="*60)
    print(" TESTING PHASE 5: ASSEMBLY CODE GENERATOR")
    print("="*60)
    
    try:
        # If no inputs provided, run all previous phases
        if tac is None or symbol_table is None:
            from intermediate_code import test_intermediate_code
            from semantic_analyzer import test_semantic_analyzer
            
            # Get symbol table
            symbol_table = test_semantic_analyzer(source_code)
            if symbol_table is None:
                return None
            
            # Get TAC and string literals
            tac, string_literals = test_intermediate_code(source_code)
            if tac is None:
                return None
        
        asm_generator = AssemblyGenerator(tac, symbol_table, string_literals)
        assembly = asm_generator.generate()
        print("\n✓ Assembly Code Generation Successful!")
        return assembly
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
    
    if (sum > 25) {
        print("Result is greater");
    }
    """
    
    test_code_generator(test_code)
