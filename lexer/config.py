import json
import os
from .tokens import TokenType

class KeywordConfig:
    """
    Loads and validates dynamic keyword configurations.
    """
    def __init__(self, config_path: str = None):
        self.keywords: dict[str, TokenType] = {}
        if config_path:
            self.load_from_file(config_path)

    def load_from_file(self, config_path: str):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            try:
                raw_config = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in {config_path}: {e}")
        
        self.validate_and_load(raw_config)

    def validate_and_load(self, raw_config: dict[str, str]):
        self.keywords = {}
        seen_token_types = set()

        if not isinstance(raw_config, dict):
            raise ValueError("Configuration must be a JSON object mapping strings to strings.")

        for surface_word, internal_type_str in raw_config.items():
            surface_word = surface_word.strip()
            internal_type_str = internal_type_str.strip()

            # Empty keyword check
            if not surface_word:
                raise ValueError("Keyword configuration contains empty surface word.")

            # Duplicate surface keywords are naturally handled by JSON/dict overriding,
            # but if they passed through, we just enforce one-to-one or valid logic.
            # However, mapping two words to the SAME token type (e.g. `when`->IF, `if`->IF) 
            # is acceptable unless restricted. The user requirement states:
            # "Duplicate surface keywords" as a problem, but json.load inherently deduplicates identical keys.
            
            # Check for invalid characters in keyword (must be alpha)
            if not surface_word.isalpha():
                raise ValueError(f"Keyword '{surface_word}' contains invalid characters (only letters allowed).")

            # Check supported internal token type
            try:
                token_type = TokenType[internal_type_str]
            except KeyError:
                raise ValueError(f"Unknown token type: {internal_type_str}")

            # Check if this token type was already mapped (we assume 1-to-1 mapping for simplicity, 
            # though many-to-1 might be valid, it's safer to flag conflict in a simple compiler)
            if token_type in seen_token_types:
                # Find the conflicting word
                conflict_word = [k for k, v in self.keywords.items() if v == token_type][0]
                raise ValueError(f"Keyword '{surface_word}' conflicts with another keyword definition ('{conflict_word}') for token type {internal_type_str}.")

            seen_token_types.add(token_type)
            self.keywords[surface_word] = token_type

    def get_token_type(self, word: str) -> TokenType | None:
        """
        Returns the TokenType if the word is a configured keyword, else None.
        """
        return self.keywords.get(word)
