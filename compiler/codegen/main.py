import parser


SOURCE_CODE = """
def main(hola: string) -> void {
    let hello: string = "HELLO";
}
"""

def main() -> str:
    program = parser.parse_source_code(SOURCE_CODE)
    converted_code = []
    


if __name__ == "__main__":
    main()
