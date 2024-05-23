import requests
from github import Github, GithubException
import json

output_file = "repo_info.json"
with open('.env', 'r') as file:
    github_token = file.read()
g = Github(github_token)
repositories = []
with open('../data/bigRepos.txt', 'r') as file:
    repositories = [line.strip() for line in file.readlines()]

def fetch_repo_data(repository):
    try:
        repo = g.get_repo(repository)
    except GithubException as e:
        if e.status == 404:
            print("Repository not found: ", repository)
            return
        else:
            print("An error occurred: ", e)
    return repo

if __name__ == "__main__":
    i = 0
    for repository in repositories:
        if i == 0:
            repo = fetch_repo_data(repository)
            print(repo)
        else:
            break
        i += i + 1
        