import sys
import json

from jats_injector import *

with open('boilder.xml') as f:
    boilder_content = f.readlines()

f = open(sys.argv[1])
data = json.load(f)
f.close()
xml_content = convert_jats(data)

output_file = open(sys.argv[2], 'w')

output_file.write("".join(boilder_content) + xml_content)
output_file.close()
