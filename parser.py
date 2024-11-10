from lexer import Token

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = iter(lexer.tokenize())
        self.current_token = None
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        self.program()

    def program(self):
        print("<Program> -> <StatementList>")
        self.statement_list()

    def statement_list(self):
        print("<StatementList> -> <Statement> ; <StatementList> | ε")
        while self.current_token and self.current_token.type in {"IDENTIFIER", "KEYWORD"}:
            if self.current_token.lexeme == "else":
                break
            self.statement()
            if self.current_token and self.current_token.lexeme == ";":
                print(f"Token: Separator\tLexeme: {self.current_token.lexeme}")
                self.advance()
            else:
                break

    def statement(self):
        print("<Statement> -> <Assign> | <IfStatement> | <WhileStatement>")
        if self.current_token.type == "IDENTIFIER":
            self.assign()
        elif self.current_token.lexeme == "if":
            self.if_statement()
        elif self.current_token.lexeme == "while":
            self.while_statement()
        else:
            self.error("Expected a statement")

    def assign(self):
        print("<Assign> -> <Identifier> = <Expression>")
        if self.current_token.type == "IDENTIFIER":
            print(f"Token: Identifier\tLexeme: {self.current_token.lexeme}")
            self.advance()
            if self.current_token.lexeme == "=":
                print(f"Token: Operator\tLexeme: {self.current_token.lexeme}")
                self.advance()
                self.expression()
            else:
                self.error("Expected '=' after identifier in assignment")
        else:
            self.error("Expected identifier")

    def if_statement(self):
        print("<IfStatement> -> if (<Expression>) <Statement> [else <Statement>]")
        print(f"Token: Keyword\tLexeme: {self.current_token.lexeme}")
        self.advance()  # Skip 'if'
        if self.current_token.lexeme == "(":
            print(f"Token: Separator\tLexeme: {self.current_token.lexeme}")
            self.advance()
            self.expression()
            if self.current_token.lexeme == ")":
                print(f"Token: Separator\tLexeme: {self.current_token.lexeme}")
                self.advance()
                self.statement()
                if self.current_token and self.current_token.lexeme == "else":
                    print(f"Token: Keyword\tLexeme: {self.current_token.lexeme}")
                    self.advance()
                    self.statement()
            else:
                self.error("Expected ')' after expression in if statement")
        else:
            self.error("Expected '(' after 'if'")

    def while_statement(self):
        print("<WhileStatement> -> while (<Expression>) <Statement>")
        print(f"Token: Keyword\tLexeme: {self.current_token.lexeme}")
        self.advance()  # Skip 'while'
        if self.current_token.lexeme == "(":
            print(f"Token: Separator\tLexeme: {self.current_token.lexeme}")
            self.advance()
            self.expression()
            if self.current_token.lexeme == ")":
                print(f"Token: Separator\tLexeme: {self.current_token.lexeme}")
                self.advance()
                self.statement()
            else:
                self.error("Expected ')' after expression in while statement")
        else:
            self.error("Expected '(' after 'while'")

    def expression(self):
        print("<Expression> -> <Term> <ExpressionPrime>")
        self.term()
        self.expression_prime()

    def expression_prime(self):
        if self.current_token and self.current_token.lexeme in {"+", "-"}:
            print(f"Token: Operator\tLexeme: {self.current_token.lexeme}")
            print("<ExpressionPrime> -> + <Term> <ExpressionPrime>")
            self.advance()
            self.term()
            self.expression_prime()
        else:
            print("<ExpressionPrime> -> ε")

    def term(self):
        print("<Term> -> <Factor> <TermPrime>")
        self.factor()
        self.term_prime()

    def term_prime(self):
        if self.current_token and self.current_token.lexeme in {"*", "/"}:
            print(f"Token: Operator\tLexeme: {self.current_token.lexeme}")
            print("<TermPrime> -> * <Factor> <TermPrime>")
            self.advance()
            self.factor()
            self.term_prime()
        else:
            print("<TermPrime> -> ε")

    def factor(self):
        if self.current_token.lexeme == "(":
            print(f"Token: Separator\tLexeme: {self.current_token.lexeme}")
            self.advance()
            print("<Factor> -> (<Expression>)")
            self.expression()
            if self.current_token.lexeme == ")":
                print(f"Token: Separator\tLexeme: {self.current_token.lexeme}")
                self.advance()
            else:
                self.error("Expected ')' after expression in factor")
        elif self.current_token.type in {"IDENTIFIER", "INTEGER", "REAL"}:
            print(f"Token: {self.current_token.type}\tLexeme: {self.current_token.lexeme}")
            print("<Factor> -> <Identifier> | <Integer> | <Real>")
            self.advance()
        else:
            self.error("Expected a factor")

    def error(self, message):
        if self.current_token:
            print(f"Syntax error: {message} at '{self.current_token.lexeme}'")
        else:
            print("Syntax error: Unexpected end of input")
