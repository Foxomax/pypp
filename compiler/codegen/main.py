import compiler.pypp_parser
import compiler.ast_nodes as ast


SOURCE_CODE = """
def main(hola: string) -> void {
    let hello: string = "HELLO";
}
"""

class BaseCodegen:
    def _generate(self, node: ast.Baseast):
        raise NotImplementedError


class PythonCodegen(BaseCodegen):
    def __init__(self, program: ast.Program):
        self._program = program
        self._hide_types = False

    def hide_types(self):
        self._hide_types = True
        return self

    def build(self) -> str:
        code = ""
        for f in self._program.functions:
            code += self._generate(f)

        return code

    def _generate(self, node: ast.Baseast):
        match node:
            case ast.VoidType(value=_):
                return "None"
            case ast.StringLiteral(value=value):
                return value
            case ast.String(value=_):
                return "str"
            case ast.Parameter(identifier=identifier, _type=_type):
                if not self.hide_types():
                    type__ = self._generate(_type)
                    return f"{identifier.name}: {type__}"
                return identifier.name
            case ast.VariableDeclaration(name=name, type_=_type, expression=expression):
                return f"{name}: {self._generate(_type)} = {self._generate(expression)}"
            case ast.Block(statements=statements):
                return "\n".join(self._generate(b) for b in statements)
            case ast.Function(identifier, parameters, return_typ, block):
                return f"""
def {identifier.name}({", ".join(self._generate(p) for p in parameters)}) -> {self._generate(return_typ)}:
    {self._generate(block)}
                """
            case _:
                raise NotImplementedError(f"No codegen rule for {type(node)}")


def generate_code(source_code: str, lang: str) -> str:
    program = compiler.pypp_parser.parse_source_code(source_code)
    if lang == "python":
        return PythonCodegen(program).build()

    raise NotImplementedError(f"Language: {lang} not supported by Py++ compiler")

