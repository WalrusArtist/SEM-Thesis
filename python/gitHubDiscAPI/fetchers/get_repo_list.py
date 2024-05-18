import requests

def get_top_repositories(year, count=1000):
    # GitHub API endpoint for searching repositories
    url = "https://api.github.com/search/repositories"
    
    # Query parameters for searching repositories created in the specified year
    params = {
        "q": f"created:{year}-01-01..{year}-12-31",
        "sort": "stars",  # Sort by popularity (stars)
        "order": "desc",  # Sort in descending order
        "per_page": min(count, 100),  # Maximum results per page (100)
        "page": 1,        # Initial page number
    }
    
    top_repositories = []
    
    # Make requests until the desired number of repositories are fetched or no more results are available
    while len(top_repositories) < count:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # Extract repository names from the search results
            for item in data.get("items", []):
                top_repositories.append(item["full_name"])
            # Move to the next page
            if "next" in response.links:
                next_url = response.links["next"]["url"]
                params["page"] += 1
            else:
                break  # Stop if there are no more pages
        else:
            print(f"Failed to fetch repositories. Status code: {response.status_code}")
            break
    
    return top_repositories[:count]

def save_to_file(file_path, data):
    with open(file_path, "w") as file:
        for item in data:
            file.write(item + "\n")

if __name__ == "__main__":
    year = 2020
    count = 1000
    file_path = "top_repositories_2020.txt"

    top_repositories = get_top_repositories(year, count)
    print(f"Top {len(top_repositories)} popular repositories created in {year}:")
    for repo in top_repositories:
        print(repo)

    # Save the list of repositories to a file
    save_to_file(file_path, top_repositories)
    print(f"Repository names saved to '{file_path}'")
