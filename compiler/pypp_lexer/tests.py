from .main import tokenize


def test_lexer():
    language = """
        fn main() -> void {
           let hello: string = "HELLO";
        }
    """

    tokens = tokenize(language)

    result = [(t.name, t.value) for t in tokens]

    expected = [
        ("FN", "fn"),
        ("IDENTIFIER", "main"),
        ("LPAREN", "("),
        ("RPAREN", ")"),
        ("ARROW", "->"),
        ("VOID", "void"),
        ("LBRACE", "{"),
        ("LET", "let"),
        ("IDENTIFIER", "hello"),
        ("COLON", ":"),
        ("TYPE_STRING", "string"),
        ("ASSIGN", "="),
        ("STRING", '"HELLO"'),
        ("SEMICOLON", ";"),
        ("RBRACE", "}"),
    ]

    assert result == expected