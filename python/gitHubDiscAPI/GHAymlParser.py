import os
from github import Github, GithubException
import json

github_token = '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'

g = Github(github_token)

repositories = []

with open('data/repoListTesting.txt', 'r') as file:
    repositories = [line.strip() for line in file.readlines()]

print(repositories)

def fetch_workflow_files(repository):
    try:
        repo = g.get_repo(repository)
    except GithubException as e:
        if e.status == 404:
            print("Repository not found:", repository)
            return
        else:
            print("An error occurred:", e)
    workflows = []
    try:
        for content in repo.get_contents(".github/workflows", ref="main"):
            if content.type == "file" and content.name.endswith(".yml"):
                workflows.append(content)
    except:
        print('some error occured, skipping over ', repository)
    return workflows

def parse_workflow_files(workflows, repo):
    repoDict = {}
    repoDict[repo] = {}
    repoDict[repo]['localActions'] = 0
    repoDict[repo]['marketplaceActions'] = 0

    for workflow in workflows:
        print(f"Processing workflow file: {workflow.path}")
        workflow_content = workflow.decoded_content.decode("utf-8")
        if "uses: ./.github" in workflow_content:
            repoDict[repo]['localActions'] += 1
        elif "uses: actions/" in workflow_content:
            repoDict[repo]['marketplaceActions'] += 1
        else:
            print("Workflow does not specify any actions.")
    return repoDict

def main():
    repoListStat = []
    for repo in repositories:
        print(f"Fetching workflows for repository: {repo}")
        workflows = fetch_workflow_files(repo)
        if workflows is None:
            return
        repoDict = parse_workflow_files(workflows, repo)
        repoListStat.append(repoDict)
    
    with open("data/repoListStat.json", "w") as json_file:
        json.dump(repoListStat, json_file, indent=4)
    
if __name__ == "__main__":
    main()