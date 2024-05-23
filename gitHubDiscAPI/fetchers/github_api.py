import requests
import json
import os

def fetch_github_discussions(token):
    url = 'https://api.github.com/graphql'
    headers = {
        'Authorization': f'bearer {token}',
        'Accept': 'application/vnd.github.v4+json',
    }

    query = """
    query {
      search(query: "GitHub Actions", type: DISCUSSION, first: 100) {
        nodes {
          ... on Discussion {
            title
            body
            url
            createdAt
            updatedAt
            comments(first: 1) {
              totalCount
              nodes {
                reactions(first: 100) {
                  totalCount
                }
              }
            }
          }
        }
      }
    }
    """
    
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch discussions: {response.status_code} - {response.text}")
        return None

def main():
    token = '' # os.environ.get('GITHUB_TOKEN')''
    if token is None:
        print("GitHub token not found. Set the GITHUB_TOKEN environment variable.")
        return

    discussions = fetch_github_discussions(token)
    if discussions:
        with open("../data/main.json", "w") as json_file:
            json.dump(discussions, json_file, indent=4)
        print("GitHub Actions discussions saved to main.json")
    else:
        print("No discussions found or error occurred.")

if __name__ == "__main__":
    main()