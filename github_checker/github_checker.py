import github
import json
import time

from datetime import datetime
from github import Github

class github_checker:
    def __init__(self, username: str, password: str):
        self._username = username
        self._github = Github(username, password)
        self._github.get_user('patrickelectric')
        self._search_username = self._username

        self._age = 7

        self._issue = False
        self._pr = False
        self._mk = True

        self._pr_state = ['open', 'closed']
        self._issue_state = ['open', 'closed']
        self._state_to_utf = {'open': '✗', 'closed': '✔'}
        self._cl_size = 0


        self._stats = {}

    def set_pr(self, on):
        self._pr = on
    def pr(self) -> bool:
        return self._pr

    def set_issue(self, on):
        self._issue = on
    def issue(self) -> bool:
        return self._issue

    def set_max_age(self, age: int):
        if age < 1:
            print('Incorrect age: %d' % age)
            return

        self._age = age
    def max_age(self) -> int:
        return self._age

    def set_max_age_from_time(self, date: str):
        self.set_max_age((datetime.now().date() - datetime.strptime(date, "%d %m %Y").date()).days)

    def set_mk(self, on: bool):
        self._mk = on
    def mk(self) -> bool:
        return self._mk

    def set_user(self, user: str):
        self._search_username = user
    def user(self) -> str:
        return self._search_username

    def print_pr(self, pr: github.PullRequest.PullRequest):
        if self._search_username not in self._stats:
            self._stats[self._search_username] = {}

        if 'number_of_prs' not in self._stats[self._search_username]:
            self._stats[self._search_username]['number_of_prs'] = 0

        self._stats[self._search_username]['number_of_prs'] = \
            int(self._stats[self._search_username]['number_of_prs']) + 1

        if self._mk:
            text = \
'''
\t\tCreated in: %s
\t\tLast update in: %s
\t\t%s
\t\t\tNew PR [#%d](%s)
'''
            print(text % (
                pr.created_at.strftime("(%A) %d-%m-%Y"),
                pr.updated_at.strftime("(%A) %d-%m-%Y"),
                pr.title, pr.number, pr.html_url
            ))
        else:
            print('Class only prints mk for now.')
            pass

    def print_issue(self, issue: github.Issue.Issue):
        if self._search_username not in self._stats:
            self._stats[self._search_username] = {}

        if 'number_of_issues' not in self._stats[self._search_username]:
            self._stats[self._search_username]['number_of_issues'] = 0

        self._stats[self._search_username]['number_of_issues'] = \
            int(self._stats[self._search_username]['number_of_issues']) + 1

        if self._mk:
            text = \
'''
\t\tCreated in: %s
\t\tLast update in: %s
\t\t%s
\t\t\tNew issue [#%d](%s)
'''
            print(text % (
                issue.created_at.strftime("(%A) %d-%m-%Y"),
                issue.updated_at.strftime("(%A) %d-%m-%Y"),
                issue.title, issue.number, issue.html_url
            ))
        else:
            print('Class only prints mk for now.')
            pass

    def print_stats(self):
        print('\n\n%s' % (16*'-'))
        print(json.dumps(self._stats, sort_keys=True, indent=4))
        print(16*'-')

    def printcl(self, text: str):
        if self._cl_size:
            print('%s' % (self._cl_size*' '), end='\r')
        self._cl_size = len(text.expandtabs())
        print('%s' % text, end='\r')

    def search(self, paths: list):
        print('Searching for PRs and issues related to user: %s' % self._search_username)
        for name in paths:
            if not name:
                continue

            # nickname/repo
            if '/' in name:
                nick, repo_name = name.split('/')
                user = self._github.get_user(nick)
                repo = user.get_repo(repo_name)
                self.search_repo(repo)
            else: # nickname
                if 'User' in self._github.get_user(name).type:
                    usr = self._github.get_user(name)
                    print('Check repositories in user: %s' % name)
                    for repo in usr.get_repos(sort='updated'):
                        self.search_repo(repo)
                else:
                    org = self._github.get_organization(name)
                    print('Check repositories in org: %s' % name)
                    for repo in org.get_repos():
                        self.search_repo(repo)

        self.print_stats()

    def search_repo(self, repo: github.Repository.Repository):
        if not self._pr and not self._issue:
            self._pr = True

        if self._pr:
            for pr_state in self._pr_state:
                prs = repo.get_pulls(state=pr_state, sort='updated')
                # totalCount does not work
                # https://github.com/PyGithub/PyGithub/issues/870
                total = 0
                for _ in prs:
                    total = total + 1
                for i, pr in enumerate(prs):
                    self.printcl('[PR][%s][%d/%d]\t\t%s' % (self._state_to_utf[pr_state], i, total, repo.name))
                    # It's not me
                    if self._search_username not in pr.user.login:
                        continue

                    # Check for max age
                    if (datetime.now().date() - pr.updated_at.date()).days > self._age:
                        break

                    self.print_pr(pr)

        if self._issue:
            for issue_state in self._issue_state:
                issues = repo.get_issues(state=issue_state, sort='updated')
                total = 0
                for _ in issues:
                    total = total + 1
                for i, issue in enumerate(issues):
                    self.printcl('[ISSUE][%s][%d/%d]\t%s' % (self._state_to_utf[issue_state], i + 1, total, repo.name))
                    # It's not me
                    check_for_name_in = [issue.user.login]
                    if issue.closed_by:
                        check_for_name_in.append(issue.closed_by.login)
                    if issue.assignee:
                        check_for_name_in.append(issue.assignee.login)
                    if self._search_username not in check_for_name_in:
                        continue

                    # Check for max age
                    if (datetime.now().date() - issue.updated_at.date()).days > self._age:
                        break

                    self.print_issue(issue)

    def get_forks_parents(self, name=None):
        if not name:
            name = self._search_username

        usr = self._github.get_user(name)
        print('Check parents in repositories of user: %s' % name)
        repos = usr.get_repos(sort='updated')
        total = 0
        forks = []
        for _ in repos:
            total = total + 1
        for i, repo in enumerate(repos):
            if not repo.fork:
                continue
            self.printcl('[FORKS][%d/%d]\t%s' % (i + 1, total, repo.name))
            if repo.parent.owner.login not in forks:
                forks.append(repo.parent.owner.login)

        print('\n\n%s' % (16*'-'))
        for fork in forks:
            print(fork)