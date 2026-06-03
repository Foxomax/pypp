from lark import Lark
from compiler.lexer import TypeLexer
from compiler.ast import AstBuilder


SOURCE_CODE = """
def main(hola: string) -> void {
    let hello: string = "HELLO";
}  
"""

GRAMMAR = r"""
start: function*

function: _DEF IDENTIFIER _LPAREN parameters* _RPAREN _ARROW return_type block

block: _LBRACE statement* _RBRACE

?statement: variable_decl

?parameters: IDENTIFIER _COLON type

variable_decl: _LET IDENTIFIER _COLON type _ASSIGN expression _SEMICOLON

type: TYPE_STRING

expression: STRING

return_type: VOID
           | type

%declare _DEF
%declare IDENTIFIER
%declare _LPAREN
%declare _RPAREN
%declare _ARROW
%declare VOID
%declare _LET
%declare _COLON
%declare _ASSIGN
%declare _SEMICOLON
%declare _LBRACE
%declare _RBRACE
%declare STRING
%declare TYPE_STRING
"""


def main():
    parser = Lark(
        GRAMMAR,
        parser="lalr",
        lexer=TypeLexer
    )

    tree = parser.parse(SOURCE_CODE)
    print(tree.pretty())
    ast = AstBuilder().transform(tree)
    print(ast)


if __name__ == "__main__":
    main()