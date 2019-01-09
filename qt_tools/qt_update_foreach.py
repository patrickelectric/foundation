import argparse
import fileinput
import glob
import os
import re

parser = argparse.ArgumentParser(description="Move from foreach to c++11 for.")
parser.add_argument('--path', action="store", type=str, default=os.getcwd(), help="Path.")
args = parser.parse_args()

for filename in glob.iglob(os.path.join(args.path, '**/*.c*')):
    if '.cpp' not in filename and '.cc' not in filename:
        continue

    '''
    for line in fileinput.input(filename, inplace=True):
        print(line, end='\n')
        pass
        #print(filename, line)
    '''
    lines = []
    with open(filename, 'r+b') as src:
        for line in src:
            if 'foreach' in line:
                matchObj = re.match("^\s*foreach\s*\((.*?)(\)(\s*{|)\s*$)", line.decode("utf-8"))
                line = line.replace(matchObj.group(1), ':'.join(matchObj.group(1).split(',')))
                line = line.replace('foreach', 'for')
                print(line)
                lines += line
            else:
                lines += line


    with open(filename, 'w') as dst:
        for line in lines:
            dst.write(line)
