import requests
from bs4 import BeautifulSoup
import json
from openai import OpenAI

# client = OpenAI()

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#   ]
# )

# print(completion.choices[0].message)

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
                disc_url = 'https://github.com/' + link['href']
                disc_response = requests.get(disc_url)

                if disc_response.status_code == 200:
                    disc_soup = BeautifulSoup(disc_response.text, 'html.parser')
                    discussion_links = disc_soup.find_all('td', class_='d-block color-fg-default comment-body markdown-body js-comment-body')

                    aggregated_p = ''
                    for x in discussion_links:
                        if x.find('p') is not None:
                            aggregated_p += x.find('p').text + '/n'

                discussion = {
                    'title': link.text.strip(),
                    'url': disc_url,
                    'upvotes': upvotes[i]['upvotes'],
                    'body': aggregated_p
                }
                discussions.append(discussion)
                i += 1
        else:
            print(f"Failed to fetch page {page}: {response.status_code}")

    return discussions

def main():
    url_template = "https://github.com/orgs/community/discussions/categories/actions?discussions_q=is%3Aopen+category%3AActions+sort%3Atop+is%3Aunanswered={}"
    pages = 1

    discussions = scrape_github_discussions(url_template, pages)
    
    with open("data/scraper.json", "w") as json_file:
        json.dump(discussions, json_file, indent=4)
    
    print("GitHub discussions saved to scraper.json.")

if __name__ == "__main__":
    main()