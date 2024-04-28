import json
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np

parsed_repo_data = {}
with open('../data/repo_parser.json', 'r') as file:
    parsed_repo_data = json.load(file)

def plot(x, y, cc):
    plt.plot(x, y, label='SizeToActionsUsed', color='blue')

    plt.xlim(min(x), max(x))      # range x axis
    plt.ylim(min(y), max(y))  # range y axis

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'Correlation Coefficience: {cc}')
    plt.legend()

    # display
    plt.grid(True)
    plt.show()

def get_total_actions_times_used():
    total_local_times_used = 0
    total_marketplace_times_used = 0
    size_used_dict = {}

    for item in parsed_repo_data:
        repo_name = list(item.keys())[0]
        size_used_dict[repo_name] = {}
        size_used_dict[repo_name]['size'] = item[repo_name]['size']
        size_used_dict[repo_name]['localActions'] = item[repo_name]['localActions']
        size_used_dict[repo_name]['marketplaceActions'] = item[repo_name]['marketplaceActions']

        size_used_dict[repo_name]['total_local_used'] = 0
        size_used_dict[repo_name]['total_marketplace_used'] = 0
        size_used_dict[repo_name]['total_total_used'] = 0
        action_dict = item[repo_name]['actions']
        for action in action_dict.values():
            if action['isMarketplace'] is True:
                total_local_times_used += action['times_used']
                size_used_dict[repo_name]['total_local_used'] += action['times_used']
                size_used_dict[repo_name]['total_total_used'] += action['times_used']
            else:
                total_marketplace_times_used += action['times_used']
                size_used_dict[repo_name]['total_marketplace_used'] += action['times_used']
                size_used_dict[repo_name]['total_total_used'] += action['times_used']
    

    sorted_data = sorted(size_used_dict.items(), key=lambda x: x[1]['total_local_used'])
    sizes = np.array([item[1]['size'] for item in sorted_data])
    total_local_used = np.array([item[1]['total_local_used'] for item in sorted_data])
    local_correlation_coefficient, _ = pearsonr(sizes, total_local_used)

    total_used_actions = total_marketplace_times_used + total_local_times_used
    precentage_used_local = (total_local_times_used / total_used_actions) * 100
    percentage_used_market = (total_marketplace_times_used / total_used_actions) * 100

    print('precentage_used_local: ', "{:.2f}".format(precentage_used_local))
    print('percentage_used_market: ', "{:.2f}".format(percentage_used_market))

    return total_local_used, sizes, local_correlation_coefficient, precentage_used_local, percentage_used_market, size_used_dict

def size_to_local_actions():
    size_to_local_actions_dict = {}
    for item in parsed_repo_data:
        repo_name = list(item.keys())[0]

        localActions = item[repo_name]['localActions']
        marketplaceActions = item[repo_name]['marketplaceActions']
        totalActions = localActions + marketplaceActions
        size = item[repo_name]['size']
        if totalActions > 0:
            size_to_local_actions_dict[repo_name] = {}
            size_to_local_actions_dict[repo_name]['local_perc'] = (localActions / totalActions) * 100
            size_to_local_actions_dict[repo_name]['size'] = size

    sorted_data = sorted(size_to_local_actions_dict.items(), key=lambda x: x[1]['local_perc'])
    sizes = np.array([item[1]['size'] for item in sorted_data])
    local_percs = np.array([item[1]['local_perc'] for item in sorted_data])
    correlation_coefficient, _ = pearsonr(sizes, local_percs)

    return sizes, local_percs, correlation_coefficient


def calculate_percentage_actions():
    total_actions = 0
    sum_tot_local_actions = 0
    sum_tot_market_actions = 0
    for item in parsed_repo_data:
        repo_name = list(item.keys())[0]
        sum_tot_local_actions += item[repo_name]['localActions']
        sum_tot_market_actions += item[repo_name]['marketplaceActions']

    total_actions = sum_tot_local_actions + sum_tot_market_actions

    precentage_local = (sum_tot_local_actions / total_actions) * 100
    percentage_market = (sum_tot_market_actions / total_actions) * 100

    print('precentage_local: ', "{:.2f}".format(precentage_local))
    print('percentage_market: ', "{:.2f}".format(percentage_market))

    return precentage_local, percentage_market

def main():
    precentage_local, percentage_market = calculate_percentage_actions()
    #sizes, local_percs, size_localprc_correlation_coefficient = size_to_local_actions()
    total_local_times_used, size_used_dict, local_correlation_coefficient,  precentage_used_local, percentage_used_market, size_used_dict = get_total_actions_times_used()

    sorted_data = sorted(size_used_dict.items(), key=lambda x: x[1]['total_local_used'])
    localActions = np.array([item[1]['localActions'] for item in sorted_data])
    total_local_used = np.array([item[1]['total_local_used'] for item in sorted_data])
    local_correlation_coefficient, _ = pearsonr(localActions, total_local_used)

    plot(total_local_used,localActions, local_correlation_coefficient)
    #plot(sizes, local_percs, size_localprc_correlation_coefficient)
    #plot(total_local_times_used, size_used_dict, local_correlation_coefficient)

main()