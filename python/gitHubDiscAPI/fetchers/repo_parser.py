import os
from github import Github, GithubException
import json
import requests

github_token = ''
g = Github(github_token)
repositories = []

with open('../data/bigRepos.txt', 'r') as file:
    repositories = [line.strip() for line in file.readlines()]


def check_action_exists(action_version):
    if action_version.startswith('v'):
        return True
    return False

# def get_versions_behind(action_owner, action_name, current_version):
#     def get_latest_release():
#         url = f"https://api.github.com/repos/{action_owner}/{action_name}/releases/latest"
#         response = requests.get(url)
#         response.raise_for_status()
#         return response.json()['tag_name']
#     def get_all_releases():
#         url = f"https://api.github.com/repos/{action_owner}/{action_name}/releases"
#         response = requests.get(url)
#         response.raise_for_status()
#         return [release['tag_name'] for release in response.json()]
#     def compare_versions(current_version, all_versions):
#         try:
#             current_index = all_versions.index(current_version)
#         except ValueError:
#             return -1  # The current version is not in the list of all versions
#         return len(all_versions) - current_index - 1
#     try:
#         all_versions = get_all_releases()
#         all_versions.sort()  # Ensure versions are sorted in ascending order
#         versions_behind = compare_versions(current_version, all_versions)
#         if versions_behind == -1:
#             return "The current version is not found in the list of releases."
#         return versions_behind
#     except requests.exceptions.RequestException as e:
#         return f"An error occurred: {e}"



def parse_workflow_files(workflows, repoDict, unique_actions, repo):
    for workflow in workflows:
        #print(f"Processing workflow file: {workflow.path}")f
        workflow_content = workflow.decoded_content.decode("utf-8")
        lines = workflow_content.split('\n')

        for line in lines:
            if '/.github' in line and "uses:" in line:
                line = line.replace(' ', '')
                if line.startswith('-'):
                    line = line[1:]

                action_name = line.replace('/.github','').replace('.yml','').replace('.yml','')
                action_name = action_name.split('/')[-1] + '-LOCAL'
                if action_name not in unique_actions:
                    unique_actions.add(action_name)
                    repoDict[repo]['localActions'] += 1
                    repoDict[repo]['actions'][action_name] = {}
                    repoDict[repo]['actions'][action_name]['isMarketplace'] = False
                    repoDict[repo]['actions'][action_name]['times_used'] = 1
                    repoDict[repo]['actions'][action_name]['line'] = line
                else:
                    repoDict[repo]['actions'][action_name]['times_used'] += 1

            elif "uses:" in line and '@' in line and '/.github' not in line:
                line = line.replace('- uses:','').replace('uses:','').replace(' ','')
                action_name  = line.split('/')

                if len(action_name) == 2:
                    action_owner = action_name[0]
                    action_version = action_name[1].split('@')[1]
                    action_name = action_name[1].split('@')[0]
                    if action_name not in unique_actions:
                        repoDict[repo]['actions'][action_name] = {}
                        repoDict[repo]['actions'][action_name]['times_used'] = 1 
                        repoDict[repo]['actions'][action_name]['line'] = line
                        unique_actions.add(action_name)
                        isMarketplace = check_action_exists(action_version)
                        if not isMarketplace:
                            repoDict[repo]['localActions'] += 1
                        else:
                            repoDict[repo]['actions'][action_name]['version'] = action_version
                            repoDict[repo]['actions'][action_name]['owner'] = action_owner
                            repoDict[repo]['marketplaceActions'] += 1
                        repoDict[repo]['actions'][action_name]['isMarketplace'] = isMarketplace
                    else:
                        repoDict[repo]['actions'][action_name]['times_used'] += 1 
    return repoDict


def construct_repo_data(workflows, repo, size, languages, contributor_count, created_at):
    repoDict = {}
    repoDict[repo] = {}
    repoDict[repo]['localActions'] = 0
    repoDict[repo]['marketplaceActions'] = 0
    unique_actions = set()
    repoDict[repo]['actions'] = {}
    repoDict[repo]['size'] =  size
    repoDict[repo]['languages'] = languages
    repoDict[repo]['created_at'] = created_at
    repoDict = parse_workflow_files(workflows, repoDict, unique_actions, repo)
    repoDict[repo]['contributor_count'] = contributor_count
    return repoDict


def fetch_repo_data(repository):
    try:
        repo = g.get_repo(repository)
    except GithubException as e:
        if e.status == 404:
            print("Repository not found: ", repository)
            return
        else:
            print("An error occurred: ", e)
    workflows = []
    size = 0
    languages = []
    contributor_count = 0
    created_at = 0
    try:
        size = repo.size
        languages = repo.get_languages()
        contributor_count = repo.get_contributors().totalCount
        created_at = repo.created_at
        for content in repo.get_contents(".github/workflows", ref="main"):
            if content.type == "file" and content.name.endswith(".yml"):
                workflows.append(content)
    except:
        try:
            size = repo.size
            languages = repo.get_languages()
            contributor_count = repo.get_contributors().totalCount
            created_at = repo.created_at
            for content in repo.get_contents(".github/workflows", ref="master"):
                if content.type == "file" and content.name.endswith(".yml"):
                    workflows.append(content)
        except:
            print('SKIPPING: Failed processing repository: ', repository)
    return workflows, size, languages, contributor_count, created_at


def main():
    repoListStat = []
    for repo in repositories:
        print(f"Processing repository: {repo}")
        workflows, size, languages, contributor_count, created_at = fetch_repo_data(repo)
        repoDict = construct_repo_data(workflows, repo, size, languages, contributor_count, created_at)
        repoListStat.append(repoDict)
        with open("../data/repo_parserExtended.json", "w") as json_file:
            json.dump(repoListStat, json_file, indent=4, default=str)

    with open("../data/repo_parserExtended.json", "w") as json_file:
        json.dump(repoListStat, json_file, indent=4, default=str)
    

if __name__ == "__main__":
    main()