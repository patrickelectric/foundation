import github
import json
import time

from datetime import datetime
from github import Github

class GithubIssueMover:
    def __init__(self, username: str, password: str):
        self._username = username
        self._github = Github(username, password)
        self._github.get_user('patrickelectric')

        self._issue_state = ['open']

    def move(self, name: str, name_out: str):
        if not name:
            return

        # nickname/repo
        if '/' not in name or '/' not in name_out:
            return

        nick, repo_name = name.split('/')
        user = self._github.get_user(nick)
        repo = user.get_repo(repo_name)

        nick, repo_name = name_out.split('/')
        user = self._github.get_user(nick)
        repo_out = user.get_repo(repo_name)

        self.search_repo(repo, repo_out)

    def search_repo(self, repo: github.Repository.Repository, repo_out: github.Repository.Repository):
        for issue_state in self._issue_state:
            issues = repo.get_issues(state=issue_state, sort='updated')
            total = 0
            for _ in issues:
                total = total + 1
            for i, issue in enumerate(issues):
                # GitHub's REST API v3 considers every pull request an issue, but not every issue is a pull request.
                # You can identify pull requests by the pull_request key.
                if issue.pull_request:
                    continue
                print('[ISSUE][%s][%d/%d]\t%s %s' % (issue_state, i + 1, total, repo.name, issue.title))
                print('Moved from: %s#%d' % (repo.full_name, issue.number))
                print('Original author: @%s' % (issue.user.login))
                print('Body: @%s' % (issue.body))
                title = 'Sub: %s' % (issue.title)
                body = \
'''
Moved from: %s#%d
Original author: @%s

### Feature request
%s

**Platform**
[ ] All
[ ] AntennaTracker
[ ] Copter
[ ] Plane
[ ] Rover
[x] Submarine
'''% (repo.full_name, issue.number, issue.user.login, issue.body)
                repo_out.create_issue(title=title, body=body)
