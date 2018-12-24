#!/usr/bin/env python3
import argparse
import fileinput
import json
import glob
import os
import re

parser = argparse.ArgumentParser(description="Check includes in Qt project.")
parser.add_argument('--path', action="store", type=str, default=os.getcwd(), help="Path.")
args = parser.parse_args()

def missing_types(src) -> dict:
    types = {}
    for line in src:
        matchObj = re.match(r"#include\s*<(?P<type>[A-z]*)>", line.decode("utf-8"))

        if matchObj != None:
            types[matchObj.group('type')] = False
            continue

        for key in list(types.keys()):
            if str(key) in str(line):
                del types[key]

    return types

for filename in glob.iglob(os.path.join(args.path, '**/*.h')):
    with open(filename, 'r+b') as src:
        output = missing_types(src)
        if output != {}:
            print('in file: ', filename)
            print(json.dumps(output))
            print('------------')
