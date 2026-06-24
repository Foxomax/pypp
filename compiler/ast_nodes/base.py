class BaseAst:
    def __repr__(self):
        return f"<{self.__class__}>"


class BaseType(BaseAst):
    pass


class BaseStatement(BaseAst):
    pass
