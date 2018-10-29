#!/usr/bin/env python3

import argparse
import psutil
import os
import sys

if os.name != 'posix':
    sys.exit('platform not supported')

parser = argparse.ArgumentParser(description="Get machine info")
parser.add_argument('--cpu', action="store_true", default=False, help="Get cpu usage")
parser.add_argument('--disk', action="store_true", default=False, help="Get disk usage")
parser.add_argument('--mem', action="store_true", default=False, help="Get mem usage")
args = parser.parse_args()

def main():
    if args.cpu:
        print(psutil.cpu_percent(interval=1), end=' ')
    if args.mem:
        print(psutil.virtual_memory().percent, end=' ')
    if args.disk:
        print(psutil.disk_usage('/').percent, end=' ')
    return 0

if __name__ == '__main__':
    main()
