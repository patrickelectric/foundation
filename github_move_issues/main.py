import argparse
import sys

from getpass import getpass
from githubIssueMover import GithubIssueMover

parser = argparse.ArgumentParser(
    description="Move open issues between repositories."
)
parser.add_argument('--input', action="store", required=True,
    help="Issues source: org/repo_name or user_name/repo_name."
)
parser.add_argument('--output', action="store", required=True,
    help="Move issues to: org/repo_name or user_name/repo_name."
)

args = parser.parse_args()

# Get user and password
print("This script uses github api, please provide username and password.")
username = input("Nickname: ")
password = getpass('Password: ')
try:
    mover = GithubIssueMover(username, password)
except Exception as e:
    print('Something wrong with user and password.')
    print(e)
    sys.exit(1)

if not args.input or not args.output :
    print('--input and --output should be used.')
    sys.exit(1)

mover.move(args.input, args.output)
