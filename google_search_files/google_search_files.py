#!/usr/bin/env python3

import argparse

# from https://github.com/abenassi/Google-Search-API
from google.google import search

parser = argparse.ArgumentParser(
    description="Find files in google.",
    epilog='python google_search_files --format=pdf datasheet 555'
)
parser.add_argument('--formats', action="store", type=str, nargs='+', required=True, default='pdf',
    help="Format to be searched."
)
parser.add_argument('text', nargs='*')

args = parser.parse_args()

def find(text, formats):
    filetype = ''

    msg = "\U0001F4C4 Hey there, champs! I found these files on Google:\n------------------------------\n"

    filetype = ' filetype:'.join(formats)

    text += filetype
    results = search(text)

    for result in results:
        msg = msg + '{:<70s}\n\t> {}\n'.format(result.name[:70].split('...')[0], result.link)
    return msg

if __name__ == '__main__':
    print(find(' '.join(args.text), args.formats))
