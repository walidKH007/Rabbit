#!/usr/bin/python3
import git
from git import Repo

def Add_To_Depot(Depo_path,file_name):
    repo = git.Repo(Depo_path)
    repo.git.add(file_name)
    repo.git.commit('-m', 'commit new File', author='walid.khlouf@hotmail.com')
    repo.remotes.origin.push(refspec='master:master')

if __name__ == "__main__":
    Depo_path="TP-RT0704"
    file_name="read.py"
    Add_To_Depot(Depo_path,file_name)