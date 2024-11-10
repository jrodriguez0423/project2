import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        # Define your token patterns (adjust to your requirements)
        token_specification = [
            ("KEYWORD", r'\b(if|else|while|return)\b'),
            ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ("INTEGER", r'\b\d+\b'),
            ("REAL", r'\b\d+\.\d+\b'),
            ("ASSIGN", r'='),
            ("OPERATOR", r'[+\-*/]'),
            ("DELIMITER", r'[;{},()]'),
            ("WHITESPACE", r'[ \t\n]+'),
        ]

        token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
        for match in re.finditer(token_regex, self.code):
            kind = match.lastgroup
            value = match.group(kind)
            if kind != "WHITESPACE":  # Ignore whitespace
                self.tokens.append(Token(kind, value))
        return iter(self.tokens)

class Token:
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme
