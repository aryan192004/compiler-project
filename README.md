# Customizable Mini Programming Language Compiler

## Project Objective
The project involves designing and implementing a customizable mini programming language compiler with dynamic keyword mapping. This allows developers to customize the surface-level keywords without changing the compiler's internal token categories or parsing logic.

## Review 1 Implementation Scope
This milestone covers approximately 25% of the overall compiler architecture. It includes:
1. **Keyword Configuration System:** A dynamic system that reads customizable mapping from a JSON file.
2. **Lexical Analyzer (Lexer):** A handwritten scanner that transforms source code into a stream of tokens independent of the customized keywords used.

### Pipeline Status
- [x] Keyword Configuration
- [x] Lexical Analyzer (CURRENT IMPLEMENTATION)
- [ ] Parser
- [ ] AST
- [ ] Semantic Analyzer
- [ ] TAC
- [ ] Optimizer
- [ ] Interpreter

## What is Dynamic Keyword Mapping?
Dynamic Keyword Mapping means that the lexical analyzer operates in a configuration-driven manner. Instead of hard-coding keywords like `let`, `if`, or `while` into the logic of the lexer, it loads the vocabulary mapping at runtime.

As a result, a program written with `create` and `repeat` will output the exact same internal token categories (`LET`, `WHILE`) as a program written with `let` and `while`. The parser receives identical internal structures regardless of the user's chosen syntax.

## Architecture
- **`lexer/tokens.py`**: Defines the `TokenType` and the `Token` objects structure.
- **`lexer/config.py`**: Defines the `KeywordConfig` class to load, validate, and manage keyword mappings from JSON.
- **`lexer/lexer.py`**: The `Lexer` class performing character-by-character analysis.
- **`main.py`**: Command-line interface to interact with the system.

## Configuration Format
Configurations are stored in JSON. Example `config/custom_keywords.json`:
```json
{
    "create": "LET",
    "show": "PRINT",
    "when": "IF",
    "otherwise": "ELSE",
    "repeat": "WHILE",
    "yes": "TRUE",
    "no": "FALSE"
}
```

## How to Run the Lexer
Run a custom configuration:
```bash
python main.py --source examples/custom_program.txt --keywords config/custom_keywords.json
```

Run the default configuration:
```bash
python main.py --source examples/default_program.txt --keywords config/default_keywords.json
```

Run the comparison demonstration (shows both default and custom lexers producing identical internal token streams):
```bash
python main.py --compare
```

## How to Run Tests
To run the automated unit tests covering everything from basic keywords to invalid configuration handling:
```bash
python -m unittest discover
```
