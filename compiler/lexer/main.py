

class Token:
    def __init__(self, name: str, value: str, start: int, end: int, line: int, col: int):
        self.name = name