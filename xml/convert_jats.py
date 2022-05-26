import sys
import json

from jats_injector import *

f = open(sys.argv[1])
data = json.load(f)
f.close()
xml_content = convert_jats(data)

output_file = open(sys.argv[2], 'w')
output_file.write(xml_content)
output_file.close()
