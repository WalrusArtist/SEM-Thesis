import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_github_discussions(url_template, pages):
    discussions = []
    upvotes     = []

    # These titles are announcements made by GitHub. We avoid em
    avoid_titles = ["Actions FAQs", "Public Beta Feedback - Actions streaming logs with backscroll", 
                    "GitHub-hosted runners: Double the power for open source", 
                    "Feedback Requested: Actions Usage Metrics", 
                    "Take Action this April! [Actions Check-in]"]

    for page in range(1, pages + 1):
        print('page: ', page)
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
                    buttons = disc_soup.find_all('button', attrs={'name': 'input[content]'})
                    commentCount = disc_soup.find_all('h2', attrs={'id': 'discussion-comment-count'})
                    tag_elements = disc_soup.find_all('span', class_="css-truncate css-truncate-target")

                    print("Procession post: ", disc_url)

                    tags = []
                    for tag_element in tag_elements:
                        tags.append(tag_element.text.replace(' ',''))

                    commentsAmount = 0
                    repliesAmount = 0
                    for x in commentCount:
                        if x.find('span') is not None:
                            spans = x.find_all('span')
                            for y in spans:
                                if any(char.isdigit() for char in y.text):
                                    cleaned_y_text = ''.join(y.text.split())
                                    if 'repl' in cleaned_y_text:
                                        cleaned_y_text = re.sub(r"\D", "", cleaned_y_text)
                                        text2int = int(cleaned_y_text)
                                        repliesAmount = text2int

                                    if 'comment' in cleaned_y_text:
                                        cleaned_y_text = cleaned_y_text = re.sub(r"\D", "", cleaned_y_text)
                                        text2int = int(cleaned_y_text)
                                        commentsAmount = text2int
                    
                    filtered_buttons = []
                    for button in buttons:
                        parent_div = button.find_parent('div', class_='edit-comment-hide')
                        if parent_div:
                            filtered_buttons.append(button)

                    aggregated_reactions = 0
                    for x in filtered_buttons:
                        if x.find('span') is not None:
                            try:
                                text2int = int(x.find('span').text)
                                aggregated_reactions += text2int
                            except ValueError:
                                print("Cannot convert the text to an integer. Value: ", x.find('span').text)

                    aggregated_p = ''
                    for x in discussion_links:
                        if x.find('p') is not None:
                            aggregated_p += x.find('p').text + '/n'

                discussion = {
                    'title': link.text.strip(),
                    'url': disc_url,
                    'upvotes': upvotes[i]['upvotes'],
                    'tags': tags,
                    'rections' : aggregated_reactions,
                    'replies': repliesAmount,
                    'comments': commentsAmount,
                    'body': aggregated_p
                }
                if discussion['title'] not in avoid_titles:
                    discussions.append(discussion)
                    with open("../data/github_scraper.json", "w") as json_file:
                        json.dump(discussions, json_file, indent=4)
                i += 1
        else:
            print(f"Failed to fetch page {page}: {response.status_code}")

    return discussions

def main():
    url_template = "https://github.com/orgs/community/discussions/categories/actions?discussions_q=is%3Aopen+category%3AActions+sort%3Atop+is%3Aunanswered%3D%7B40%7D&page={}"
    pages = 40

    discussions = scrape_github_discussions(url_template, pages)
    
    with open("../data/github_scraper.json", "w") as json_file:
        json.dump(discussions, json_file, indent=4)
    
    print("GitHub discussions saved to scraper.json.")

if __name__ == "__main__":
    main()