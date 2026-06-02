import re


KEYWORDS = {
    "fn": "FN",
    "let": "LET",
    "const": "CONST",
    "return": "RETURN",
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

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '(' + self.name + ', "' + str(self.value) + '"' + ')'

class TokenTemplate:
    def __init__(self, name, regexp, process=None):
        self.name = name
        r = re.compile(regexp)
        self.regexp = r
        self.process = process

    def match(self, string, start, line,col):
        matched = self.regexp.match(string, start)
        if not matched:
            return False

        end = matched.end()

        if self.process:
            value = self.process(matched.group())
        else:
            value = matched.group()

        for c in matched.group():
            if c == '\n':
                line += 1
                col = 1

        return Token(self.name, value, start, end, line,col)

def temp(name, regexp, process=None):
    return TokenTemplate(name, regexp, process)



def lex(string: str, lexer: list[TokenTemplate]):
    start = 0
    tokens = []
    line = 1
    col = 1

    if string == '':
        return []

    while True:
        valid = False

        for tp in lexer:

            token = tp.match(string, start, line, col)
            if not token:
                continue

            if token.value is not None:
                if token.name == "IDENTIFIER":
                    if token.value in KEYWORDS:
                        token.name = KEYWORDS[token.value]
                tokens.append(token)

            start = token.end
            valid = True
            if token.line != line:
                col = 1
            else:
                col += token.end - token.start
            line = token.line
            break

        if not valid:
            raise Exception("Token error at position " + str(col) + " on line " + str(line) + '.')
        if start == len(string): return tokens


LEXERS = [
    temp("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    temp("NUMBER", r"\d+", int),
    temp("STRING", r'"[^"]*"'),
    temp("CHAR", r"'[^']'"),

    temp("ARROW", r"->"),

    temp("EQ", r"=="),
    temp("NE", r"!="),
    temp("GTE", r">="),
    temp("LTE", r"<="),

    temp("AND", r"&&"),
    temp("OR", r"\|\|"),
    temp("NOT", r"!"),

    temp("ASSIGN", r"="),
    temp("GT", r">"),
    temp("LT", r"<"),

    temp("PLUS", r"\+"),
    temp("MINUS", r"-"),
    temp("STAR", r"\*"),
    temp("SLASH", r"/"),

    temp("COLON", r":"),
    temp("SEMICOLON", r";"),

    temp("LPAREN", r"\("),
    temp("RPAREN", r"\)"),

    temp("LBRACE", r"\{"),
    temp("RBRACE", r"\}"),

    temp("SPACE", r"\s+", lambda _: None),
    temp("COMMA", r","),
    temp("DOT", r"\."),
]

if __name__ == "__main__":
    language = \
        """
        fn main() -> void {
           let hello: string = "HELLO WORLD";
           print(hello);
        }
        """

    print(lex(language, LEXERS))