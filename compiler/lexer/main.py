import re
from typing import Optional, Callable, Any, Iterator
from lark import Token as LarkToken
from lark.lexer import Lexer, LexerState

KEYWORDS = {
    "def": "_DEF",
    "let": "_LET",
    "const": "CONST",
    "return": "RETURN",
    "void": "VOID",
    "string": "TYPE_STRING",
    "int64": "TYPE_I64",
    "int32": "TYPE_I32",
    "int16": "TYPE_I16",
    "int8": "TYPE_I8",
}


class Token:
    def __init__(self, name: str, value: str, start: int, end: int, line: int, col: int):
        self.name = name
        self.value = value
        self.start = start
        self.end = end
        self.line = line
        self.col = col

    def __eq__(self, other):
        return self.name == other

    def __repr__(self):
        return f'({self.name}, "{self.value}", L:{self.line}, C:{self.col})'


class TokenTemplate:
    def __init__(self, name: str, regexp: str, process: Optional[Callable[[str], Any]] = None):
        self.name = name
        self.regexp = re.compile(regexp)
        self.process = process

    def match(self, string: str, start: int):
        return self.regexp.match(string, start)


def temp(name: str, regexp: str, process: Optional[Callable[[str], Any]] = None) -> TokenTemplate:
    return TokenTemplate(name, regexp, process)


LEXERS = [
    temp("COMMENT", r"//.*", lambda _: None),
    temp("SPACE", r"\s+", lambda _: None),

    temp("NUMBER", r"\d+\.\d+|\d+", lambda v: float(v) if '.' in v else int(v)),
    temp("STRING", r'"([^"\\]|\\.)*"'),
    temp("CHAR", r"'([^'\\]|\\.)'"),

    temp("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),

    temp("_ARROW", r"->"),
    temp("EQ", r"=="),
    temp("NE", r"!="),
    temp("GTE", r">="),
    temp("LTE", r"<="),
    temp("AND", r"&&"),
    temp("OR", r"\|\|"),
    temp("NOT", r"!"),
    temp("_ASSIGN", r"="),
    temp("GT", r">"),
    temp("LT", r"<"),
    temp("PLUS", r"\+"),
    temp("MINUS", r"-"),
    temp("STAR", r"\*"),
    temp("SLASH", r"/"),
    temp("_COLON", r":"),
    temp("_SEMICOLON", r";"),
    temp("_LPAREN", r"\("),
    temp("_RPAREN", r"\)"),
    temp("_LBRACE", r"\{"),
    temp("_RBRACE", r"\}"),
    temp("COMMA", r","),
    temp("DOT", r"\."),
]


def tokenizer(string: str, lexer: list[TokenTemplate]) -> list[Token]:
    start = 0
    tokens = []
    line = 1
    col = 1
    length = len(string)

    while start < length:
        valid = False
        for tp in lexer:
            match = tp.match(string, start)
            if not match:
                continue

            lexeme = match.group()
            end = match.end()

            value = tp.process(lexeme) if tp.process else lexeme

            if value is not None:
                name = tp.name
                if name == "IDENTIFIER" and lexeme in KEYWORDS:
                    name = KEYWORDS[lexeme]
                tokens.append(Token(name, value, start, end, line, col))

            for char in lexeme:
                if char == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1

            start = end
            valid = True
            break

        if not valid:
            raise Exception(f"Token error at position {col} on line {line} near '{string[start:start + 10]}'.")

    return tokens

def tokenize(language: str):
    return tokenizer(language, LEXERS)


# This implementation is created about this:
# https://lark-parser.readthedocs.io/en/stable/examples/advanced/custom_lexer.html#sphx-glr-examples-advanced-custom-lexer-py
class TypeLexer(Lexer):
    def __init__(self, lexer_conf=None):
        pass

    def lex(self, data) -> Iterator[LarkToken]:
        tokens = tokenizer(str(data), LEXERS)

        for t in tokens:
            yield LarkToken(t.name, t.value, start_pos=t.start, end_pos=t.end, line=t.line, column=t.col)
