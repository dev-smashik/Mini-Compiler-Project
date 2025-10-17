# 🚀 Mini Compiler Project

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Course](https://img.shields.io/badge/course-CSE%20430-orange.svg)](https://github.com)

A comprehensive educational compiler implementation demonstrating all major phases of compilation - from lexical analysis to assembly code generation. Built as part of CSE 430 - Compiler Design Lab.

**Creator:** Sheikh Muhammad Ashik  
**ID:** 21201118  
**Course:** CSE 430 - Compiler Design Lab
**University:** University of Asia Pacific

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Compiler Phases](#-compiler-phases)
- [Installation](#-installation)
- [Usage](#-usage)
- [Language Syntax](#-language-syntax)
- [Project Structure](#-project-structure)
- [Examples](#-examples)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This mini compiler translates a simple high-level programming language into x86 assembly code through five distinct phases. It supports basic data types, arithmetic operations, control structures, and demonstrates fundamental compiler construction principles.

---

## ✨ Features

- 🔍 **Complete Lexical Analysis** - Tokenizes source code with comprehensive pattern matching
- 🌳 **Abstract Syntax Tree** - Builds hierarchical program representation
- 🔬 **Semantic Analysis** - Type checking and symbol table management
- 📝 **Three-Address Code** - Generates intermediate representation (TAC)
- ⚙️ **Assembly Generation** - Produces x86 assembly output
- 🧪 **Modular Testing** - Test individual phases independently
- 📊 **Interactive CLI** - User-friendly command-line interface
- 🎨 **Detailed Output** - Comprehensive visualization of each phase

---

## 🔄 Compiler Phases

### Phase 1: Lexical Analysis (Tokenization)
Converts source code into a stream of tokens.

```python
Input:  float x = 10.7;
Output: [Token(FLOAT, 'float'), Token(ID, 'x'), Token(ASSIGN, '='), 
         Token(FLOAT_NUM, '10.7'), Token(SEMICOLON, ';')]
```

### Phase 2: Syntax Analysis (Parsing)
Builds an Abstract Syntax Tree (AST) from tokens.

```
Declaration: float x
  Float: 10.7
```

### Phase 3: Semantic Analysis
Validates types and manages symbol table.

```
Symbol Table:
Variable        Type       Initialized
x              float      True
```

### Phase 4: Intermediate Code Generation
Generates Three-Address Code (TAC).

```
1. t0 = x + y
2. sum = t0
3. print sum
```

### Phase 5: Code Generation (Assembly)
Produces x86 assembly code.

```asm
section .data
    x dd 0
section .text
    mov eax, [x]
    mov [sum], eax
```

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- Git (for cloning the repository)

### Clone Repository

```bash
git clone https://github.com/dev-smashik/Mini-Compiler-Project.git
cd mini-compiler
```

### Install Dependencies

This project uses only Python standard library - no external dependencies required!

```bash
# Optional: Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

## 🚀 Usage

### Interactive Mode

Run the main testing framework with an interactive menu:

```bash
python compiler_test.py
```

### Test Individual Phases

#### Phase 1: Lexical Analysis Only
```bash
python lexer.py
```

#### Phase 2: Syntax Analysis
```bash
python parser.py
```

#### Phase 3: Semantic Analysis
```bash
python semantic_analyzer.py
```

#### Phase 4: Intermediate Code Generation
```bash
python intermediate_code.py
```

#### Phase 5: Complete Compilation
```bash
python code_generator.py
```

### Programmatic Usage

```python
from compiler_test import Compiler

source_code = """
    int x = 10;
    int y = 20;
    int sum = x + y;
    print(sum);
"""

# Compile through all phases
compiler = Compiler(source_code)
result = compiler.compile(stop_at_phase=5)

# Or stop at specific phase
result = compiler.compile(stop_at_phase=3)  # Stop after semantic analysis
```

---

## 📖 Language Syntax

### Variable Declaration

```python
int x = 10;
float pi = 3.14;
string name = "Compiler";
```

### Arithmetic Operations

```python
int result = (x + y) * z - w / 2;
float average = (a + b) / 2;
```

### Comparison Operations

```python
if (x > 10) {
    print("Greater");
}

if (y == 5) {
    print("Equal");
}
```

### Control Structures

#### If-Else Statement
```python
if (x > 0) {
    print("Positive");
} else {
    print("Non-positive");
}
```

#### While Loop
```python
int i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### Print Statement

```python
print(variable);
print("String literal");
print(x + y);
```

### Comments

```python
// This is a single-line comment
int x = 5; // Inline comment
```

---

## 📁 Project Structure

```
mini-compiler/
│
├── lexer.py                 # Phase 1: Lexical Analyzer
├── parser.py                # Phase 2: Syntax Analyzer
├── semantic_analyzer.py     # Phase 3: Semantic Analyzer
├── intermediate_code.py     # Phase 4: Intermediate Code Generator
├── code_generator.py        # Phase 5: Assembly Code Generator
├── compiler_test.py         # Main Testing Framework
└── README.md               # Project Documentation
```

### Module Descriptions

| Module | Description | Key Classes |
|--------|-------------|-------------|
| `lexer.py` | Tokenizes source code | `Lexer`, `Token` |
| `parser.py` | Builds AST from tokens | `Parser`, AST node classes |
| `semantic_analyzer.py` | Type checking & symbol table | `SemanticAnalyzer`, `SymbolTable` |
| `intermediate_code.py` | Generates TAC | `IntermediateCode` |
| `code_generator.py` | Produces assembly | `AssemblyGenerator` |
| `compiler_test.py` | Testing framework | `Compiler` |

---

## 💡 Examples

### Example 1: Simple Arithmetic

**Input:**
```python
int a = 5;
int b = 10;
int sum = a + b;
print(sum);
```

**Output (TAC):**
```
1. a = 5
2. b = 10
3. t0 = a + b
4. sum = t0
5. print sum
```

### Example 2: Conditional Statement

**Input:**
```python
float score = 85.5;
if (score >= 80) {
    print("Excellent");
} else {
    print("Good");
}
```

**Output (TAC):**
```
1. score = 85.5
2. t0 = score >= 80
3. if_false t0 goto L0
4. print str0
5. goto L1
6. L0:
7. print str1
8. L1:
```

### Example 3: Loop

**Input:**
```python
int counter = 0;
while (counter < 5) {
    print(counter);
    counter = counter + 1;
}
```

**Output (TAC):**
```
1. counter = 0
2. L0:
3. t0 = counter < 5
4. if_false t0 goto L1
5. print counter
6. t1 = counter + 1
7. counter = t1
8. goto L0
9. L1:
```

---

## 🧪 Testing

### Run All Tests

```bash
python compiler_test.py
```

### Test Specific Phase

Each module includes standalone testing capabilities:

```bash
# Test lexer
python lexer.py

# Test parser
python parser.py

# Test semantic analyzer
python semantic_analyzer.py

# Test intermediate code generation
python intermediate_code.py

# Test assembly generation
python code_generator.py
```

### Custom Test Cases

Create a test file `test_code.txt`:

```python
float x = 10.5;
int y = 20;
float result = x + y;

if (result > 25) {
    print("Large result");
}
```

Run through compiler:

```python
from compiler_test import Compiler

with open('test_code.txt', 'r') as f:
    source_code = f.read()

compiler = Compiler(source_code)
compiler.compile(stop_at_phase=5)
```

---

## 🎓 Educational Value

This project demonstrates:

- **Lexical Analysis:** Pattern matching with regular expressions
- **Parsing Techniques:** Recursive descent parsing
- **AST Construction:** Building hierarchical data structures
- **Symbol Tables:** Scope management and type tracking
- **Intermediate Representation:** Platform-independent code generation
- **Code Optimization:** Basic optimization opportunities in TAC
- **Target Code Generation:** x86 assembly instruction selection

---

### Ideas for Contributions

- Add support for functions and procedures
- Implement arrays and advanced data structures
- Add more data types (char, boolean)
- Optimize intermediate code generation
- Improve error messages and recovery
- Add code optimization passes
- Support for multiple source files

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Sheikh Muhammad Ashik**  
Student ID: 21201118  
Course: CSE 430 - Compiler Design Lab
University: University of Asia Pacific
Email: 21201118@uap-bd.edu

---

<div align="center">

**⭐ Star this repository if you found it helpful! ⭐**

Made with ❤️ by Sheikh Muhammad Ashik

</div>
