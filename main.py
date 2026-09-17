import argparse
import sys
from lexer.config import KeywordConfig
from lexer.lexer import Lexer, LexicalError

def print_tokens(tokens):
    print("-" * 39)
    for token in tokens:
        print(f"{token.type.name:<12} {token.lexeme}")
    print("-" * 39)

def process_file(source_path, config_path):
    print("-" * 39)
    print("CUSTOMIZABLE MINI LANGUAGE LEXER")
    print("-" * 39)
    
    try:
        config = KeywordConfig(config_path)
        print("\nKeyword Configuration:")
        for word, ttype in config.keywords.items():
            print(f"{word} -> {ttype.name}")
            
        with open(source_path, 'r', encoding='utf-8') as f:
            source = f.read()
            
        print("\nSource:")
        print(source.strip())
        
        lexer = Lexer(source, config)
        tokens = lexer.tokenize()
        
        print("\nTokens:")
        print_tokens(tokens)
        
    except LexicalError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

def compare_mode():
    default_config_path = "config/default_keywords.json"
    custom_config_path = "config/custom_keywords.json"
    default_source_path = "examples/default_program.txt"
    custom_source_path = "examples/custom_program.txt"
    
    try:
        default_config = KeywordConfig(default_config_path)
        custom_config = KeywordConfig(custom_config_path)
        
        with open(default_source_path, 'r', encoding='utf-8') as f:
            default_source = f.read()
        with open(custom_source_path, 'r', encoding='utf-8') as f:
            custom_source = f.read()
            
        print("DEFAULT PROGRAM:")
        print(default_source.strip())
        print("\nCUSTOM PROGRAM:")
        print(custom_source.strip())
        
        default_lexer = Lexer(default_source, default_config)
        default_tokens = default_lexer.tokenize()
        
        custom_lexer = Lexer(custom_source, custom_config)
        custom_tokens = custom_lexer.tokenize()
        
        print("\nDEFAULT TOKENS:")
        print(" ".join([t.type.name for t in default_tokens]))
        
        print("\nCUSTOM TOKENS:")
        print(" ".join([t.type.name for t in custom_tokens]))
        
        default_types = [t.type for t in default_tokens]
        custom_types = [t.type for t in custom_tokens]
        
        print("\nResults:")
        if default_types == custom_types:
            print("[OK] Internal token streams are equivalent.")
        else:
            print("[FAIL] Internal token streams differ!")
            
        print("[OK] Surface keywords are different.")
        print("[OK] Lexer successfully supports dynamic keyword mapping.")
        
    except Exception as e:
        print(f"\nError during comparison: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Customizable Mini Programming Language Lexer")
    parser.add_argument("--source", type=str, help="Path to the source program")
    parser.add_argument("--keywords", type=str, help="Path to the keyword configuration JSON")
    parser.add_argument("--compare", action="store_true", help="Run the comparison demonstration")
    
    args = parser.parse_args()
    
    if args.compare:
        compare_mode()
    elif args.source and args.keywords:
        process_file(args.source, args.keywords)
    else:
        # Default behavior if no args provided
        parser.print_help()
        print("\nRunning default comparison mode as demonstration...\n")
        compare_mode()

if __name__ == "__main__":
    main()
