import enum
import re
class OperatorType(str, enum.Enum):
    FIND = "FIND",
    REPLACE = "REPLACE"

class Operator():
    type: OperatorType = None
    def apply(self, input:str) -> str:
        raise NotImplemented()

    def to_dict(self) -> dict:
        raise NotImplemented()

    def from_dict(dict:dict):
        raise NotImplemented()

class OperatorFind(Operator):
    def __init__(self, pattern:str):
        self.type = OperatorType.FIND
        self.pattern = pattern
    def apply(self, input:str ) -> str:
        matches = re.findall(self.pattern, input, re.MULTILINE)
        _matches = []
        for m in matches:
            l = ''.join(list(m))
            _matches += [l]
        return "\n".join(_matches)

    def to_dict(self) -> dict:
        return { "type": self.type.value, "pattern":self.pattern}

class OperatorReplace(Operator):
    def __init__(self, pattern:str, replace:str):
        self.type = OperatorType.REPLACE
        self.pattern = pattern
        self.replace = replace
    def apply(self, input:str) -> str:
        result = re.sub(self.pattern, self.replace, input)
        return result

    def to_dict(self) -> dict:
        return { "type": self.type.value, "pattern":self.pattern, "replace":self.replace}

if __name__ == "__main__":
    s = "Black, blue and brown \n Black aaaa"
    pattern = r'(bl(\w+))'
    pattern="Black.*"
    op = OperatorFind(pattern)
    matches = op.apply(s)
    print(matches)
    