from typing import TypedDict

from lark import Lark

from compiler.ast.base import BaseType
from compiler.ast.main import Program, Parameter, Block, VariableDeclaration, String
from compiler.lexer import TypeLexer
from compiler.ast import AstBuilder
from compiler.parser.exceptions import PyPPSyntaxError

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


def parse_source_code(source_code: str, /) -> Program:
    parser = Lark(
        GRAMMAR,
        parser="lalr",
        lexer=TypeLexer
    )

    tree = parser.parse(source_code)
    ast = AstBuilder().transform(tree)
    SyntacticAnalyzer(ast).analyze()
    return ast


class CallableTable(TypedDict):
    identifier: str
    return_type: BaseType
    parameters: list[Parameter]


class SyntacticAnalyzer:
    AllowedTypes: list[BaseType] = [
        String
    ]

    def __init__(self, program: Program):
        self._callable_objects: list[dict] = []
        self._var_table: dict = {}

        self._program = program

    def _init_callables_table(self):
        for f in self._program.functions:
            self._callable_objects.append({
                "identifier": f.identifier,
                "parameters": f.parameters,
                "return_type": f.return_type
            })

    def _read_block(self, block: Block):
        for s in block.statements:
            if isinstance(s, VariableDeclaration):
                if s.name in self._var_table.keys():
                    raise PyPPSyntaxError("Error: variables redeclaration not allowed")

                if not any([isinstance(s.type_, t) for t in self.AllowedTypes]):
                    raise PyPPSyntaxError(
                        f"Error: Type {repr(s.type_)} not allowed, available types are: {[t for t in self.AllowedTypes]}")

                self._var_table[s.name] = {
                    "type": s.type_,
                    "expression": s.expression
                }
                continue


    def analyze(self):
        self._init_callables_table()
        for f in self._program.functions:
            self._read_block(f.block)
        return
