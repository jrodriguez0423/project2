from lexer import Lexer
from parser import Parser

if __name__ == "__main__":
    source_code = "if (x) y = 3 + 5; else y = 4;"  # Replace with actual code input
    lexer = Lexer(source_code)
    parser = Parser(lexer)
    parser.parse()
