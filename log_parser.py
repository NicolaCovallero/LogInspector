from models.parser import *
from models.configuration import *
import logging
import argparse

parser = argparse.ArgumentParser(description='Parse a log file given a configuration')
parser.add_argument('-i', '--input', type=str, help='input file', required=True)
parser.add_argument('-o', '--output', type=str, help='output file', required=True)
parser.add_argument('-c', '--config', type=str, help='configuration json file', required=True)

args = parser.parse_args()
log = logging.getLogger()
config, _ = ConfigurationJson.from_file(args.config)
print(config.serialize())
print(config.to_operations())
try:
    parser = Parser(config.to_operations())
except:
    log.error("Error reading the configuration file {}".format(args.config))
    exit(-1)

if args.input == args.output:
    log.error("Input and output files are equal, be sure to specify different names in order to avoid overwriting the input file")

f = open(args.input, 'r')   
with f:
    input = f.read()

log.info("Parsing the file {} ....".format(args.input))
res = parser.apply(input)
log.info("File {} parsed.".format(args.input))
f = open(args.output, 'w')   
with f:
    if len(config["header"]) > 0:
        f.writelines( [config["header"] + "\n", res[-1].output ] )
    else:
        f.write(res[-1].output)