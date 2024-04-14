import json

parsed_repo_data = {}
with open('../data/repo_parser.json', 'r') as file:
    parsed_repo_data = json.load(file)

total_actions = 0
sum_tot_local_actions = 0
sum_tot_market_actions = 0
for item in parsed_repo_data:
    key = list(item.keys())[0]
    sum_tot_local_actions += item[key]['localActions']
    sum_tot_market_actions += item[key]['marketplaceActions']

total_actions = sum_tot_local_actions + sum_tot_market_actions

precentage_local = (sum_tot_local_actions / total_actions) * 100
percentage_actions = (sum_tot_market_actions / total_actions) * 100

print('precentage_local: ', "{:.2f}".format(precentage_local))
print('percentage_actions: ', "{:.2f}".format(percentage_actions))