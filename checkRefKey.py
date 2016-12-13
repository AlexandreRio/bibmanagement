"""
Look for missing grav citation formated as follow [^key] in a JSON bib file
"""

import re
import json

filename = "./04.soa/docs.md"
bibname = "04.soa/icae.json"

keys = set()
missing = set()

with open(bibname) as f:
    data = json.load(f)
    for key in data:
        keys.add(key)

with open(filename) as f:
    for line in f:
        for key in re.findall('\[\^(.+?)\]', line):
            if key not in keys:
                missing.add(key)

print(missing)
# print(keys)
