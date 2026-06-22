import textwrap
from typing import Any
from .base import BaseAst, BaseType, BaseStatement
from lark import Transformer


def indent(text: str, spaces: int = 4) -> str:
    return textwrap.indent(text, " " * spaces)


class Program(BaseAst):
    def __init__(self, functions: list["Function"]):
        self.functions = functions

    def __repr__(self):
        body = "\n".join(repr(f) for f in self.functions)
        return f"Program(\n{indent(body)}\n)"


class Parameter(BaseAst):
    def __init__(self, identifier: "Identifier", _type: BaseType):
        self.identifier = identifier
        self._type = _type

    def __repr__(self):
        return f"Parameter({self.identifier}, {self._type})"


class Function(BaseAst):
    def __init__(self, identifier: "Identifier", parameters: list[Parameter], return_type: BaseType, block: "Block"):
        self.identifier = identifier
        self.parameters = parameters
        self.return_type = return_type
        self.block = block

    def __repr__(self):
        params_repr = f"[{', '.join(repr(p) for p in self.parameters)}]" if self.parameters else "[]"
        content = (
            f"identifier={self.identifier},\n"
            f"parameters={params_repr},\n"
            f"return_type={self.return_type},\n"
            f"block={self.block}"
        )
        return f"Function(\n{indent(content)}\n)"


class Block(BaseAst):
    def __init__(self, statements: list[BaseStatement]):
        self.statements = statements

    def __repr__(self):
        body = "\n".join(repr(s) for s in self.statements)
        return f"Block(\n{indent(body)}\n)"


class VariableDeclaration(BaseStatement):
    def __init__(self, identifier: "Identifier", type_: BaseType, expression: StringLiteral):
        self.name = identifier.name
        self.type_ = type_
        self.expression = expression

    def __repr__(self):
        content = (
            f"name={self.name},\n"
            f"type={self.type_},\n"
            f"expression={self.expression}"
        )
        return f"VariableDeclaration(\n{indent(content)}\n)"


class VoidType(BaseType):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Void()"


class String(BaseType):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value})"


class StringLiteral(String):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringLiteral({self.value})"


class Identifier(BaseAst):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class AstBuilder(Transformer):
    def IDENTIFIER(self, token: Any) -> Identifier:
        return Identifier(str(token))

    def TYPE_STRING(self, token):
        return String(str(token))

    def STRING(self, token):
        return StringLiteral(token)

    def VOID(self, token):
        return VoidType(token)

    def function(self, items):
        identifier = items[0]
        params = items[1:-2]
        return_type = items[-2]
        block = items[-1]
        return Function(identifier, params, return_type, block)

    def block(self, items):
        return Block(items)

    def parameters(self, items):
        return Parameter(items[0], items[1])

    def start(self, items):
        return Program(items)

    def type(self, items):
        return items[0]

    def expression(self, items):
        return items[0]

    def return_type(self, items):
        return items[0]

    def variable_decl(self, items):
        return VariableDeclaration(*items)