import os
from github import Github, GithubException
import json
import requests

github_token = ''
g = Github(github_token)
repositories = []

with open('../data/repoListAuto.txt', 'r') as file:
    repositories = [line.strip() for line in file.readlines()]


def fetch_workflow_files(repository):
    try:
        repo = g.get_repo(repository)
    except GithubException as e:
        if e.status == 404:
            print("Repository not found: ", repository)
            return
        else:
            print("An error occurred: ", e)
    workflows = []
    try:
        for content in repo.get_contents(".github/workflows", ref="main"):
            if content.type == "file" and content.name.endswith(".yml"):
                workflows.append(content)
    except:
        try:
            for content in repo.get_contents(".github/workflows", ref="master"):
                if content.type == "file" and content.name.endswith(".yml"):
                    workflows.append(content)
        except:
            print('SKIPPING: Failed processing repository: ', repository)
    return workflows


def check_action_exists(action_name):
    url = f"https://github.com/marketplace/actions/{action_name}"
    response = requests.get(url)

    if response.status_code == 200:
        return True
    return False


def parse_workflow_files(workflows, repo):
    repoDict = {}
    repoDict[repo] = {}
    repoDict[repo]['localActions'] = 0
    repoDict[repo]['marketplaceActions'] = 0
    unique_actions = set()
    repoDict[repo]['actions'] = {}

    for workflow in workflows:

        #print(f"Processing workflow file: {workflow.path}")f
        workflow_content = workflow.decoded_content.decode("utf-8")
        lines = workflow_content.split('\n')

        for line in lines:
            if './.github' in line and "uses:" in line:
                line = line.replace(' ', '')
                if line.startswith('-'):
                    line = line[1:]

                action_name = line.replace('./.github','').replace('.yml','')
                action_name = action_name.split('/')[-1] + '-LOCAL'
                if action_name not in unique_actions:
                    unique_actions.add(action_name)
                    repoDict[repo]['localActions'] += 1
                    repoDict[repo]['actions'][action_name] = False

            elif "uses:" in line and '@' in line and './.github' not in line:
                line = line.replace('uses:','').replace(' ','')
                action_name  = line.split('/')

                if len(action_name) > 1:
                    action_name = action_name[1].split('@')[0]

                if action_name not in unique_actions:
                    unique_actions.add(action_name)
                    isMarketplace = check_action_exists(action_name)

                    if not isMarketplace:
                        repoDict[repo]['localActions'] += 1
                    else:
                        repoDict[repo]['marketplaceActions'] += 1

                    repoDict[repo]['actions'][action_name] = isMarketplace


    return repoDict


def main():
    repoListStat = []
    for repo in repositories:
        print(f"Processing repository: {repo}")
        workflows = fetch_workflow_files(repo)
        repoDict = parse_workflow_files(workflows, repo)
        repoListStat.append(repoDict)
        with open("../data/repo_parser.json", "w") as json_file:
            json.dump(repoListStat, json_file, indent=4)

    with open("../data/repo_parser.json", "w") as json_file:
        json.dump(repoListStat, json_file, indent=4)
    

if __name__ == "__main__":
    main()