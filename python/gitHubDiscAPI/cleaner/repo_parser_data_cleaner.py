import json

def clean_counts():
    parsed_repo_data = {}
    cleaned_parsed_repo_data = {}
    with open('../data/repo_parserExtendedCleaned.json', 'r') as file:
        parsed_repo_data = json.load(file)
    for item in parsed_repo_data:
        for item in parsed_repo_data:
            repo_name = list(item.keys())[0]
            cleaned_parsed_repo_data[repo_name] = {}
            localActions = 0
            marketplaceActions = 0
            for action in item[repo_name]['actions']:
                ismarket = item[repo_name]['actions'][action]['isMarketplace']
                if ismarket:
                    marketplaceActions += 1
                else:
                    localActions += 1
            cleaned_parsed_repo_data[repo_name]['localActions'] = localActions
            cleaned_parsed_repo_data[repo_name]['marketplaceActions'] = marketplaceActions
            cleaned_parsed_repo_data[repo_name]['actions'] = item[repo_name]['actions']
            cleaned_parsed_repo_data[repo_name]['size'] = item[repo_name]['size']
            cleaned_parsed_repo_data[repo_name]['languages'] = item[repo_name]['languages']
            cleaned_parsed_repo_data[repo_name]['created_at'] = item[repo_name]['created_at']
            cleaned_parsed_repo_data[repo_name]['contributor_count'] = item[repo_name]['contributor_count']
    
    with open("../data/repo_parserExtendedCleaned1.json", "w") as json_file:
        json.dump(cleaned_parsed_repo_data, json_file, indent=4, default=str)

def clean_data():
    parsed_repo_data = {}
    with open('../data/repo_parserExtended.json', 'r') as file:
        parsed_repo_data = json.load(file)

    for item in parsed_repo_data:
        cleaned_parsed_repo_data = {}

        for item in parsed_repo_data:
            repo_name = list(item.keys())[0]
            cleaned_parsed_repo_data[repo_name] = {}
            cleaned_parsed_repo_data[repo_name]['localActions'] = item[repo_name]['localActions']
            cleaned_parsed_repo_data[repo_name]['marketplaceActions'] = item[repo_name]['marketplaceActions']
            cleaned_parsed_repo_data[repo_name]['actions'] = item[repo_name]['actions']

            for action in item[repo_name]['actions']:
                sameOwner = False
                repoOwner = repo_name.split('/')[0]

                actionOwner = item[repo_name]['actions'][action]['line'].split('/')[0]
                line = item[repo_name]['actions'][action]['line']
                times_used = item[repo_name]['actions'][action]['times_used']
                if 'version' in item[repo_name]['actions'][action]:
                    version = item[repo_name]['actions'][action]['version']

                if repoOwner == actionOwner:
                    sameOwner = True
                ismarket = item[repo_name]['actions'][action]['isMarketplace']
                if '-LOCAL' not in action and not ismarket and not sameOwner:
                    cleaned_parsed_repo_data[repo_name]['actions'][action] = {}

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['version'] = ''
                    cleaned_parsed_repo_data[repo_name]['actions'][action]['version'] = version

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['line'] = ''
                    cleaned_parsed_repo_data[repo_name]['actions'][action]['line'] = line

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['times_used'] = 0
                    cleaned_parsed_repo_data[repo_name]['actions'][action]['times_used'] = times_used

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['owner'] = ''
                    cleaned_parsed_repo_data[repo_name]['actions'][action]['owner'] = actionOwner

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['isMarketplace'] = True
                    cleaned_parsed_repo_data[repo_name]['localActions'] -= 1
                    cleaned_parsed_repo_data[repo_name]['marketplaceActions'] += 1

                elif sameOwner and ismarket:
                    cleaned_parsed_repo_data[repo_name]['actions'][action] = {}

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['version'] = ''
                    cleaned_parsed_repo_data[repo_name]['actions'][action]['version'] = version

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['line'] = ''
                    cleaned_parsed_repo_data[repo_name]['actions'][action]['line'] = line

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['times_used'] = 0
                    cleaned_parsed_repo_data[repo_name]['actions'][action]['times_used'] = times_used

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['owner'] = ''
                    cleaned_parsed_repo_data[repo_name]['actions'][action]['owner'] = actionOwner

                    cleaned_parsed_repo_data[repo_name]['actions'][action]['isMarketplace'] = False
                    cleaned_parsed_repo_data[repo_name]['localActions'] += 1
                    cleaned_parsed_repo_data[repo_name]['marketplaceActions'] -= 1
                else:
                    cleaned_parsed_repo_data[repo_name]['actions'][action] = item[repo_name]['actions'][action]
            
            cleaned_parsed_repo_data[repo_name]['size'] = item[repo_name]['size']
            cleaned_parsed_repo_data[repo_name]['languages'] = item[repo_name]['languages']
            cleaned_parsed_repo_data[repo_name]['created_at'] = item[repo_name]['created_at']
            cleaned_parsed_repo_data[repo_name]['contributor_count'] = item[repo_name]['contributor_count']


    with open("../data/repo_parserExtendedCleaned.json", "w") as json_file:
        json.dump(cleaned_parsed_repo_data, json_file, indent=4, default=str)

def test_data():
    parsed_repo_data = {}
    with open('../data/repo_parserExtendedCleaned.json', 'r') as file:
        parsed_repo_data = json.load(file)
    for item in parsed_repo_data:
        repo_name = list(item.keys())[0]
        for action in item[repo_name]['actions']:
            sameOwner = False
            repoOwner = repo_name.split('/')[0]
            actionOwner = item[repo_name]['actions'][action]['line'].split('/')[0]
            ismarket = item[repo_name]['actions'][action]['isMarketplace']
            if repoOwner == actionOwner:
                sameOwner = True
            ismarket = item[repo_name]['actions'][action]['isMarketplace']
            if sameOwner and ismarket:
                print(item[repo_name]['actions'][action])

test_data()
