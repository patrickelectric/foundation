#! /bin/env python3

import os
import re
import sys

import argparse

parser = argparse.ArgumentParser(
    description="Squash some commits based in regex input.",
    epilog="""You should use this program with git, E.g:
    GIT_SEQUENCE_EDITOR="./squash-regex.py --regex \".*[Pp]ing360:.*\"" git rebase -i --autostash origin/master"
    """
    )

parser.add_argument('--regex', action="store", type=str, help="Input regex.", required=True)
parser.add_argument('--limit', action="store", type=int, default=1, help="Max number of squashs.")
parser.add_argument('file', type=str, help='GIT_SEQUENCE_EDITOR input file.')
args = parser.parse_args()

print("Starting...")

file_path = args.file
print(file_path)

lines = None
matchLines = []
outLines = []

squash_times = 0

with open(file_path, "r+b") as f:
    lines = f.readlines()

for line in lines:
    match = re.match(args.regex, line.decode("utf-8"))
    if match == None:
        outLines += [line]
    else:
        if matchLines == []:
            matchLines += [line]
        else:
            if(squash_times < args.limit):
                matchLines += [b's' + line[4:]]
                squash_times += 1
            else:
                outLines += [line]

outLines = matchLines + outLines

with open(file_path, "w+b") as f:
    for line in outLines:
        f.write(line)

exit(0)

