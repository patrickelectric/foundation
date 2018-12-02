import github
import json
import time

from datetime import datetime
from github import Github
from subprocess import call

class GithubPrMover:
    def __init__(self, username: str, password: str):
        self._username = username
        self._github = Github(username, password)
        self._github.get_user('patrickelectric')

        self._pr_state = ['open']

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
        repo_path = "/tmp/%s" % (repo.name)
        call(["git", "clone", "https://github.com/%s" % (repo.full_name), repo_path])
        call(("git --git-dir %s/.git remote add output https://github.com/%s" % (repo_path, repo_out.full_name)).split(' '))
        call(["ls", "-l", repo_path])

        for pr_state in self._pr_state:
            prs = repo.get_pulls(state=pr_state, sort='updated')
            total = 0
            for _ in prs:
                total = total + 1
            for i, pr in enumerate(prs):
                print('[PR][%s][%d/%d]\t%s %s' % (pr_state, i + 1, total, repo.name, pr.title))
                #print('Moved from: %s#%d' % (repo.full_name, pr.number))
                #print('Original author: @%s' % (pr.user.login))
                #print('Body: %s' % (pr.body))

                call(("git --git-dir %s/.git fetch origin pull/%d/head:%d" % (repo_path, pr.number, pr.number)).split(' '))
                call(("git --git-dir %s/.git push output %d" % (repo_path, pr.number)).split(' '))
                head = "%s:%d" % (repo_out.owner.login, pr.number)
                body = \
'''
%s

Moved from: %s#%d
Original author: @%s
''' % (pr.body, repo.full_name, pr.number, pr.user.login)

                repo_out.create_pull(title=pr.title, head=head, base="master", body=body)
