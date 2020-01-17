class Node(object):
    pass

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(Node):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Compound(Node):
    def __init__(self):
        self.children = []

class Assign(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(Node):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Print(Node):
    def __init__(self, token, child):
        self.token = token
        self.value = token.value
        self.child = child

class String(Node):
    def __init__(self, token):
        self.token = token
        self.value = token.value
