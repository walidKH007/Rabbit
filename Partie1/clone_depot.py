#!/usr/bin/python
from git import Repo

def clone(git_url,repo_dir):
    Repo.clone_from(git_url, repo_dir, branch="master")

if __name__ == "__main__":
    url="https://github.com/walidKH007/TP-RT0704.git"
    repo_dir="/home/walid/projects/makanch"
    clone(url,repo_dir)


