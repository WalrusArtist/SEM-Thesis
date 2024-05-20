import json
from scipy.stats import pearsonr, norm, spearmanr
import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime
import sys
import os

# Args
remove_outlier = "--remove-out" in sys.argv
invert_graph   = "--invert" in sys.argv
verbose        = "--verbose" in sys.argv
normal_dist    = "--normal" in sys.argv
do_market      = "--market" in sys.argv
save_graph     = "--save-graph" in sys.argv
help = "--help" in sys.argv

if help:
    print("   --remove-out   Removes outliers from lower 10\% upper 90%")
    print("   --invert       Inverts the x and y axis")
    print("   --verbose      Verbosity")
    print("   --normal       Gives you standard normal distributions on local actions")
    print("   --market       Measures for Marketplace Actions. Default is Local Actions")
    print("   --save-graph   Saves the graphs into a folder called graphs")
    exit()

parsed_repo_data = {}
with open('../data/repo_parserExtendedCleaned1.json', 'r') as file:
    parsed_repo_data = json.load(file)

print("Repo count: ",len(parsed_repo_data))

def min_max_values():
    sizes = np.array([item[1]['size'] for item in parsed_repo_data])
    print('Max size: ', max(sizes))

labelFix = "Local"
actionsCounts = "localActionsCount"
actionsUsedCounts = "localActionsUsedCount"
if do_market:
    labelFix = "Marketplace"
    actionsCounts = "marketActionsCount"
    actionsUsedCounts = "marketplaceActionsUsedCount"

def sort_and_plot(myDict, xVariableName='', yVariableName='', lineLabel='', x_label='', y_label='', inverted=False, remove_outliers=False):

    if remove_outliers:
        sizes = [value[yVariableName] for value in myDict.values()]
        Q1 = np.percentile(sizes, 20)
        Q3 = np.percentile(sizes, 80)
        IQR = Q3 - Q1
        multiplier = 1.5
        lower_threshold = Q1 - multiplier * IQR
        upper_threshold = Q3 + multiplier * IQR
        myDict = {key: value for key, value in myDict.items() if lower_threshold <= value[yVariableName] <= upper_threshold}

    if inverted:
        cp_xVariableName = xVariableName
        cp_yVariableName = yVariableName
        cp_x_label = x_label
        cp_y_label = y_label
        xVariableName = cp_yVariableName
        yVariableName = cp_xVariableName
        x_label = cp_y_label
        y_label = cp_x_label

    sorted_data = sorted(myDict.items(), key=lambda x: x[1][xVariableName])
    x_data = np.array([item[1][xVariableName] for item in sorted_data])
    if not normal_dist:
        y_data = np.array([item[1][yVariableName] for item in sorted_data])
    print('filtered count: ', len(x_data))

    if normal_dist:
        mu, sigma = 0, 1  # mean and standard deviation
        plt.hist(x_data, bins=30, density=True, alpha=0.6, color='g')  # histogram with 30 bins
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, sigma)
        plt.plot(x, p, 'k', linewidth=2)
        plt.title('Standard Normal Distribution')
        plt.xlabel(xVariableName)
        plt.ylabel('Density')
        if save_graph:
            folder_path = 'graphs'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, f"normal_{labelFix}_{xVariableName}_{yVariableName}.png")
            plt.savefig(file_path)
        else:
            plt.show()
        return

    if verbose:
        i = 0
        for i in range(0,len(sorted_data)):
            print(y_data[i], ' ', x_data[i])
            print(sorted_data[i][1][yVariableName], ' ', sorted_data[i][1][xVariableName])
            i += 1
        print('max y: ', max(y_data), ' ', yVariableName)

    cc, _ = pearsonr(x_data, y_data)
    plt.figure(figsize=(20, 10))
    plt.plot(x_data, y_data, label=lineLabel, color='red')
    plt.xlim(min(x_data), max(x_data))      # range x axis
    plt.ylim(min(y_data), max(y_data))  # range y axis
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f'Correlation Coefficience: {cc}')
    plt.legend()
    plt.grid(True)
    plt.scatter(x_data, y_data, alpha=0.5, s=20)
    if save_graph:
        folder_path = f'graphs/{labelFix}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, f"{labelFix}_{xVariableName}_{yVariableName}.png")
        if remove_outlier:
            file_path = os.path.join(folder_path, f"mid_range_{labelFix}_{xVariableName}_{yVariableName}.png")
        plt.savefig(file_path)
    else:
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
            if action['isMarketplace'] is False:
                total_local_times_used += action['times_used']
                size_used_dict[repo_name]['total_local_used'] += action['times_used']
                size_used_dict[repo_name]['total_total_used'] += action['times_used']
            else:
                total_marketplace_times_used += action['times_used']
                size_used_dict[repo_name]['total_marketplace_used'] += action['times_used']
                size_used_dict[repo_name]['total_total_used'] += action['times_used']
    total_used_actions = total_marketplace_times_used + total_local_times_used
    precentage_used_local = (total_local_times_used / total_used_actions) * 100
    percentage_used_market = (total_marketplace_times_used / total_used_actions) * 100
    print('precentage_used_local: ', "{:.2f}".format(precentage_used_local))
    print('percentage_used_market: ', "{:.2f}".format(percentage_used_market))

def size_to_local_actions():
    size_to_local_actions = {}
    for item in parsed_repo_data:
        repo_name = list(item.keys())[0]
        localActions = item[repo_name]['localActions']
        marketplaceActions = item[repo_name]['marketplaceActions']
        size = item[repo_name]['size']
        totalActions = localActions + marketplaceActions
        actionCondition = localActions
        if do_market:
            actionCondition = marketplaceActions
        if actionCondition > 0 and size > 0:
            size_to_local_actions[repo_name] = {}
            size_to_local_actions[repo_name]['localActionsCount'] = localActions
            size_to_local_actions[repo_name]['marketActionsCount'] = marketplaceActions
            size_to_local_actions[repo_name]['localActionsPercentage'] = localActions / totalActions
            size_to_local_actions[repo_name]['size'] = size
            size_to_local_actions[repo_name]['localActionsUsedCount'] = 0
            size_to_local_actions[repo_name]['marketplaceActionsUsedCount'] = 0
            for action in item[repo_name]['actions'].values():
                if action['isMarketplace'] == False:
                    size_to_local_actions[repo_name]['localActionsUsedCount'] += action['times_used']
                else:
                    size_to_local_actions[repo_name]['marketplaceActionsUsedCount'] += action['times_used']
            size_to_local_actions[repo_name]['localActionsUsedPercentage'] = size_to_local_actions[repo_name]['localActionsUsedCount'] / (size_to_local_actions[repo_name]['localActionsUsedCount'] + size_to_local_actions[repo_name]['marketplaceActionsUsedCount'])
    return size_to_local_actions


def contributor_to_local_actions():
    contributor_to_local_actions = {}
    for item in parsed_repo_data:
        repo_name = list(item.keys())[0]
        localActions = item[repo_name]['localActions']
        marketplaceActions = item[repo_name]['marketplaceActions']
        totalActions = localActions + marketplaceActions
        contributor_count = item[repo_name]['contributor_count']
        actionCondition = localActions
        if do_market:
            actionCondition = marketplaceActions
        if actionCondition > 0 and contributor_count > 0:
            contributor_to_local_actions[repo_name] = {}
            contributor_to_local_actions[repo_name]['localActionsCount'] = localActions
            contributor_to_local_actions[repo_name]['marketActionsCount'] = marketplaceActions
            contributor_to_local_actions[repo_name]['localActionsPercentage'] = localActions / totalActions
            contributor_to_local_actions[repo_name]['contributor_count'] = contributor_count
            contributor_to_local_actions[repo_name]['localActionsUsedCount'] = 0
            contributor_to_local_actions[repo_name]['marketplaceActionsUsedCount'] = 0
            for action in item[repo_name]['actions'].values():
                if action['isMarketplace'] == False:
                    contributor_to_local_actions[repo_name]['localActionsUsedCount'] += action['times_used']
                else:
                    contributor_to_local_actions[repo_name]['marketplaceActionsUsedCount'] += action['times_used']
            contributor_to_local_actions[repo_name]['localActionsUsedPercentage'] = contributor_to_local_actions[repo_name]['localActionsUsedCount'] / (contributor_to_local_actions[repo_name]['localActionsUsedCount'] + contributor_to_local_actions[repo_name]['marketplaceActionsUsedCount'])
    return contributor_to_local_actions

def created_to_local_actions():
    created_to_local_actions = {}
    for item in parsed_repo_data:
        repo_name = list(item.keys())[0]
        localActions = item[repo_name]['localActions']
        marketplaceActions = item[repo_name]['marketplaceActions']
        created_at = item[repo_name]['created_at']
        totalActions = localActions + marketplaceActions
        actionCondition = localActions
        if do_market:
            actionCondition = marketplaceActions
        if actionCondition > 0:
            created_to_local_actions[repo_name] = {}
            created_to_local_actions[repo_name]['localActionsCount'] = localActions
            created_to_local_actions[repo_name]['marketActionsCount'] = marketplaceActions
            created_to_local_actions[repo_name]['localActionsPercentage'] = localActions / totalActions
            created_to_local_actions[repo_name]['created_at'] =  int(datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S%z").timestamp())
            created_to_local_actions[repo_name]['localActionsUsedCount'] = 0
            created_to_local_actions[repo_name]['marketplaceActionsUsedCount'] = 0
            for action in item[repo_name]['actions'].values():
                if action['isMarketplace'] == False:
                    created_to_local_actions[repo_name]['localActionsUsedCount'] += action['times_used']
                else:
                    created_to_local_actions[repo_name]['marketplaceActionsUsedCount'] += action['times_used']
            created_to_local_actions[repo_name]['localActionsUsedPercentage'] = created_to_local_actions[repo_name]['localActionsUsedCount'] / (created_to_local_actions[repo_name]['localActionsUsedCount'] + created_to_local_actions[repo_name]['marketplaceActionsUsedCount'])
    return created_to_local_actions

def languages_to_local_actions():
    languages_to_local_actions = {}
    for item in parsed_repo_data:
        repo_name = list(item.keys())[0]
        localActions = item[repo_name]['localActions']
        marketplaceActions = item[repo_name]['marketplaceActions']
        languages = item[repo_name]['languages']
        totalActions = localActions + marketplaceActions
        actionCondition = localActions
        if do_market:
            actionCondition = marketplaceActions
        if actionCondition > 0:
            languages_to_local_actions[repo_name] = {}
            languages_to_local_actions[repo_name]['localActionsCount'] = localActions
            languages_to_local_actions[repo_name]['marketActionsCount'] = marketplaceActions
            languages_to_local_actions[repo_name]['localActionsPercentage'] = localActions / totalActions
            languages_to_local_actions[repo_name]['languagesCount'] = len(languages)
            languages_to_local_actions[repo_name]['codeSize'] = sum(languages.values())
            languages_to_local_actions[repo_name]['localActionsUsedCount'] = 0
            languages_to_local_actions[repo_name]['marketplaceActionsUsedCount'] = 0
            for action in item[repo_name]['actions'].values():
                if action['isMarketplace'] == False:
                    languages_to_local_actions[repo_name]['localActionsUsedCount'] += action['times_used']
                else:
                    languages_to_local_actions[repo_name]['marketplaceActionsUsedCount'] += action['times_used']
            languages_to_local_actions[repo_name]['localActionsUsedPercentage'] = languages_to_local_actions[repo_name]['localActionsUsedCount'] / (languages_to_local_actions[repo_name]['localActionsUsedCount'] + languages_to_local_actions[repo_name]['marketplaceActionsUsedCount'])
    return languages_to_local_actions

def owners_with_local_v_market():
    parsed_repo_data = {}
    owners = set()
    local_per_owner = {}
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
            if sameOwner is not ismarket:
                owners.add(repoOwner)

    local_owner_count_map = {}
    for owner in owners:
        local_owner_count = 0
        for item in parsed_repo_data:
            repo_name = list(item.keys())[0]
            if owner == repo_name.split('/')[0] and item[repo_name]['localActions'] > 0:
                local_owner_count += item[repo_name]['localActions']
                market_owner_count += item[repo_name]['marketplaceActions']
        local_owner_count_map[owner]['localActions'] = local_owner_count
        local_owner_count_map[owner]['marketplaceActions'] = local_owner_count

    local_owner_count_map = dict(sorted(local_owner_count_map.items(), key=lambda item: item[1], reverse=True))    
    with open("../data/local_owner_count_map.json", "w") as json_file:
        json.dump(local_owner_count_map, json_file, indent=4, default=str)
    print(owners)


                


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

def main():
    #min_max_values()
    calculate_percentage_actions()
    get_total_actions_times_used()
    owners_with_local_v_market()

    if normal_dist:
        size_to_local_actions_dict = size_to_local_actions()
        sort_and_plot(myDict=size_to_local_actions_dict, 
            xVariableName='localActionsCount')
        sort_and_plot(myDict=size_to_local_actions_dict, 
            xVariableName='localActionsPercentage')
        sort_and_plot(myDict=size_to_local_actions_dict, 
            xVariableName='localActionsUsedCount')
        sort_and_plot(myDict=size_to_local_actions_dict, 
            xVariableName='localActionsUsedPercentage')
        exit()


    # SIZE
    size_to_local_actions_dict = size_to_local_actions()
    sort_and_plot(myDict=size_to_local_actions_dict, 
                  xVariableName=actionsCounts, 
                  yVariableName='size', 
                  lineLabel=f'Size and {labelFix} Actions', 
                  x_label=f'Number of {labelFix} Actions', 
                  y_label='Repository Size',
                  inverted=invert_graph,
                  remove_outliers=remove_outlier)

    sort_and_plot(myDict=size_to_local_actions_dict, 
                xVariableName=actionsUsedCounts, 
                yVariableName='size', 
                lineLabel=f'size and {labelFix} actions Used', 
                x_label=f'Number of {labelFix} Actions Used', 
                y_label='Repository Size',
                inverted=invert_graph,
                remove_outliers=remove_outlier)
    
    # CONTRIBUTORS
    contributor_to_local_actions_dict = contributor_to_local_actions()
    sort_and_plot(myDict=contributor_to_local_actions_dict, 
                  xVariableName=actionsCounts, 
                  yVariableName='contributor_count', 
                  lineLabel=f'contributor and {labelFix} actions', 
                  x_label=f'Number of {labelFix} Actions', 
                  y_label='Number of Contributors',
                  inverted=invert_graph,
                  remove_outliers=remove_outlier)
    
    sort_and_plot(myDict=contributor_to_local_actions_dict, 
                  xVariableName=actionsUsedCounts, 
                  yVariableName='contributor_count', 
                  lineLabel=f'Contributors and {labelFix} Actions used', 
                  x_label=f'Number of {labelFix} Actions used', 
                  y_label='Number of contributors',
                  inverted=invert_graph,
                  remove_outliers=remove_outlier)
    
    # CREATED AT
    created_to_local_actions_dict = created_to_local_actions()
    sort_and_plot(myDict=created_to_local_actions_dict, 
                  xVariableName=actionsCounts, 
                  yVariableName='created_at', 
                  lineLabel=f'Repo created and {labelFix} actions', 
                  x_label=f'Number of {labelFix} Actions', 
                  y_label='Repo created (Unix Epoch)',
                  inverted=invert_graph,
                  remove_outliers=remove_outlier)

    sort_and_plot(myDict=created_to_local_actions_dict, 
                  xVariableName=actionsUsedCounts, 
                  yVariableName='created_at', 
                  lineLabel=f'Repo created and {labelFix} Actions used', 
                  x_label=f'Number of {labelFix} Actions Used', 
                  y_label='Repo created (Unix Epoch)',
                  inverted=invert_graph,
                  remove_outliers=remove_outlier)
    
    # Languages
    languages_to_local_actions_dict = languages_to_local_actions()
    sort_and_plot(myDict=languages_to_local_actions_dict, 
                  xVariableName=actionsCounts, 
                  yVariableName='languagesCount', 
                  lineLabel=f'Number of languages and {labelFix} actions', 
                  x_label=f'Number of {labelFix} Actions', 
                  y_label='Number of different languages',
                  inverted=invert_graph,
                  remove_outliers=remove_outlier)

    sort_and_plot(myDict=languages_to_local_actions_dict, 
                  xVariableName=actionsUsedCounts, 
                  yVariableName='languagesCount', 
                  lineLabel=f'Number of languages and {labelFix} Actions used', 
                  x_label=f'Number of {labelFix} Actions Used', 
                  y_label='Number of different languages',
                  inverted=invert_graph,
                  remove_outliers=remove_outlier)


    # Bytes of source code
    sort_and_plot(myDict=languages_to_local_actions_dict, 
                  xVariableName=actionsCounts, 
                  yVariableName='codeSize', 
                  lineLabel=f'Number of languages and {labelFix} actions', 
                  x_label=f'Number of {labelFix} Actions', 
                  y_label='Bytes of code',
                  inverted=invert_graph,
                  remove_outliers=remove_outlier)
    
    sort_and_plot(myDict=languages_to_local_actions_dict, 
                xVariableName=actionsUsedCounts, 
                yVariableName='codeSize', 
                lineLabel=f'Number of languages and {labelFix} Actions used', 
                x_label=f'Number of {labelFix} Actions Used', 
                y_label='Bytes of code',
                inverted=invert_graph,
                remove_outliers=remove_outlier)

main()