import argparse
import sys

from getpass import getpass
from githubChecker import GithubChecker

parser = argparse.ArgumentParser(
    description="Check for PRs and issue in repositories or organizations."
)
parser.add_argument('--age', action="store", type=int, default=7,
    help="check for PRs or issues not older than n days."
)
parser.add_argument('--source', action="store", required=True, nargs='+',
    help="repositories should have org/repo_name, user_name/repo_name or only org or user_name. This last ones will check all repositories of user and organization."
)
parser.add_argument('--issue', action="store_true", default=False,
    help="check for issues."
)
parser.add_argument('--pr', action="store_true", default=False,
    help="check for PRs [this will be used if neither issue or pr is used as argument]."
)
parser.add_argument('--mk', action="store_false", default=True,
    help="output my personal markdown style. 🖳"
)
parser.add_argument('--date', action="store", type=str,
    help="PRs or issues from time until today. (\"03 03 1992\")"
)
parser.add_argument('--user', action="store", type=str, nargs='+',
    help="Change user to search for. (user1 user2)"
)

parser.add_argument('--forks', action="store_true", default=False,
    help="User or organization to find for forks."
)

args = parser.parse_args()

# Get user and password
print("This script uses github api, please provide username and password.")
username = input("Nickname: ")
password = getpass('Password: ')
try:
    checker = GithubChecker(username, password)
except Exception as e:
    print('Something wrong with user and password.')
    print(e)
    sys.exit(1)
if args.date:
    checker.set_max_age_from_time(args.date)
else:
    checker.set_max_age(args.age)
checker.set_mk(args.mk)
checker.set_pr(args.pr)
checker.set_issue(args.issue)

if args.forks:
    checker.get_forks_parents()
else:
    if args.user:
        for user in args.user:
            checker.set_user(user)
            checker.search(args.source)
    else:
        checker.search(args.source)
