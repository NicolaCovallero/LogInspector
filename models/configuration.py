import json
import traceback
from models.operators import *
import logging 

class ConfigurationJson():

    def __init__(self):
        self.config = {"ops":[], "header": ""}
        pass

    def set_header(self, header:str):
        self.config["header"] = header

    def from_operations(ops:list):
        op : Operator
        c = ConfigurationJson()
        for op in ops:
            c["ops"].append(op.to_dict())
        return c

    def to_operations(self) -> list :
        ops = []
        for o in self["ops"]:
            if o["type"] == OperatorType.FIND:
                ops.append(OperatorFind(o["pattern"]))
            elif o["type"] == OperatorType.REPLACE:
                ops.append(OperatorReplace(o["pattern"], o["replace"]))
        return ops

    def from_file(filename:str):
        c = ConfigurationJson()
        try:
            with open(filename) as f:
                c.config = json.load(f)
                if not "header" in c.config.keys():
                     c.config["header"] = ""
            ok = True    
        except Exception as e:
            log = logging.getLogger()
            log.error(traceback.print_exc())
            log.error("Error parsing the configuration file")
            ok = False
        return c, ok

    def write(self, filename: str):
        # Serializing json 
        json_object = json.dumps(self.config, indent = 4)
        
        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)

    def serialize(self):
        return json.dumps(self.config, indent = 4)

    def __getitem__(self, index):
        return self.config[index]

if __name__ == "__main__":
    c2 = ConfigurationJson.from_operations([OperatorFind("rect"), OperatorReplace("aa", "bb")])
    c2.write("test_config.json")
    c1 = ConfigurationJson.from_file("test_config.json")
    print(c1.serialize())
    print(c1.to_operations())
    pass