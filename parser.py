from token import Token
import lexer
from lexer import Lexer
from node import Num, BinOp, Assign, Var, Compound, Print, String

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            # print(self.current_token.value)
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        node = self.statement_list()
        # self.eat(lexer.EOL)
        return node

    def statement_list(self):
        nodes = self.statement()

        results = [nodes]

        while self.current_token.type == lexer.EOL:
            self.eat(lexer.EOL)
            tmp = self.statement()
            if tmp is not None:
                results.append(tmp)

        if self.current_token.type == lexer.ID:
            self.error()

        root = Compound()
        for node in results:
            root.children.append(node)

        return root

    def statement(self):
        if self.current_token.type == lexer.ID:
            node = self.assignment_statement()
        elif self.current_token.type == lexer.Print:
            token = self.current_token
            self.eat(lexer.Print)
            self.eat(lexer.LPAREN)
            if self.current_token.type == lexer.String:
                node = String(self.current_token)
                node = Print(token, node)
                self.eat(lexer.String)
            else:
                node = self.expr()
                node = Print(token, node)
            self.eat(lexer.RPAREN)
        elif self.current_token.type == lexer.INTEGER or self.current_token.type == lexer.LPAREN:
            node = self.expr()
        else:
            node = None
        # else:
        #     node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(lexer.ASSIGN)
        if self.current_token.type == lexer.String:
            right = String(self.current_token)
            self.eat(lexer.String)
        else:
            right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(lexer.ID)
        return node

    def factor(self):
        token = self.current_token
        if token.type == lexer.INTEGER:
            self.eat(lexer.INTEGER)
            return Num(token)
        elif token.type == lexer.LPAREN:
            self.eat(lexer.LPAREN)
            node = self.expr()
            self.eat(lexer.RPAREN)
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (lexer.MUL, lexer.DIV):
            token = self.current_token
            if token.type == lexer.MUL:
                self.eat(lexer.MUL)
            elif token.type == lexer.DIV:
                self.eat(lexer.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (lexer.PLUS, lexer.MINUS):
            token = self.current_token
            if token.type == lexer.PLUS:
                self.eat(lexer.PLUS)
            elif token.type == lexer.MINUS:
                self.eat(lexer.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != lexer.EOF:
            self.error()

        return node
