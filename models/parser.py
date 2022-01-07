from models.operators import Operator
from models.configuration import *

class ParsingItem(object):
    input: str
    output: str
    op: Operator
    def __init__(self, op:Operator, input:str, output:str):
        self.op = op
        self.input = input
        self.output = output

    def data(self):
        return str(self.op)

class Parser():
    def __init__(self, operations:list = []):
        self.operations = operations

    def apply(self, input_text:str):
        text = input_text
        parsing_items = []
        for o in self.operations:
            output_text = o.apply(text)
            parsing_items.append(ParsingItem(o, text, output_text))
            text = output_text 
        return parsing_items
