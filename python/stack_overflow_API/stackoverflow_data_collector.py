import requests
import json

def fetch_stackoverflow_questions():
    api_url = 'https://api.stackexchange.com/2.3/questions'
    params = {
        'site': 'stackoverflow',
        'tagged': 'github-actions',
        'sort': 'votes',
        'order': 'desc',
        'pagesize': 100,
        'key': 'afokvFZneYSK5X4okTNnow(('
    }
    
    #sort_fields = ["creation", "votes", "answers", "score", "activity"]
    
    response = requests.get(api_url, params=params)
    data = response.json()
    '''
    for sort_field in sort_fields:
        params["sort"] = sort_field
        response = requests.get(api_url, params=params)
        data = response.json()
    '''   
    if response.status_code == 200:
        # Process the JSON response and store the data
        questions = []
        for item in data['items']:
            question = {
                'title': item['title'],
                'score': item['score'],
                'link': item['link'],
                'number_of_answers':  item['answer_count'],
                'last_updated':  item['last_activity_date']  
            }
            questions.append(question)

        # Save the data to a JSON file
        with open('github-actions-stack.json', 'w') as file:
            json.dump(questions, file, indent=4)

        print('Stackoverflow posts for collecting questions tagged "github-actions" successful.')
        
    else:
        print("Error:", data["error_message"])
        
# Call the function to fetch Stack Overflow questions and store them locally
fetch_stackoverflow_questions()