from lexer import Lexer
from parser import Parser
from ast_generator import ASTGenerator

import argparse

def main():
    argparser = argparse.ArgumentParser(
        description='Generate an AST DOT file.'
    )
    argparser.add_argument(
        'file',
        help='Arithmetic expression (in quotes): "1 + 2 * 3"'
    )
    args = argparser.parse_args()
    file = args.file
    f = open(file,'r')
    text = f.read()
    program = text.replace("\n", ";")

    lexer = Lexer(program)
    parser = Parser(lexer)
    viz = ASTGenerator(parser)
    content = viz.gendot()
    print(content)


if __name__ == '__main__':
    main()
