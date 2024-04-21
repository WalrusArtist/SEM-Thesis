from github import Github

g = Github('')

# Search for public repositories using GitHub Actions
repositories = g.search_repositories(query="is:public actions")

# Print the list of repositories
repos=[]
for repo in repositories:
    print(repo.full_name)
    repos.append(repo.full_name)

with open('../data/repoListAuto.txt', 'w') as file:
    for item in repos:
        file.write(item + '\n')
print(repos)