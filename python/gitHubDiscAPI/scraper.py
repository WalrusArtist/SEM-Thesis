import requests
from bs4 import BeautifulSoup
import json

def scrape_github_discussions(url_template, pages):
    discussions = []
    upvotes     = []

    for page in range(1, pages + 1):
        url = url_template.format(page)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            discussion_links = soup.find_all('a', attrs={'data-hovercard-type': 'discussion'})
            button_elements = soup.find_all('button', attrs={'aria-label': lambda value: value and value.startswith('Upvote:')})

            for button_element in button_elements:
                span_elements = button_element.find_all('span')
                for span_element in span_elements:
                    upvote = {
                        'upvotes': span_element.text.strip()
                    }
                    upvotes.append(upvote)

            i = 0
            for link in discussion_links:
                discussion = {
                    'title': link.text.strip(),
                    'url': link['href'],
                    'upvotes': upvotes[i]['upvotes']
                }
                discussions.append(discussion)
                i += 1
        else:
            print(f"Failed to fetch page {page}: {response.status_code}")

    return discussions

def main():
    url_template = "https://github.com/orgs/community/discussions?discussions_q=is%3Aopen+sort%3Atop&page={}"
    pages = 40

    discussions = scrape_github_discussions(url_template, pages)
    
    with open("data/scraper.json", "w") as json_file:
        json.dump(discussions, json_file, indent=4)
    
    print("GitHub discussions saved to scraper.json.")

if __name__ == "__main__":
    main()