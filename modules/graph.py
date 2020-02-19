from datetime import date
from collections import Counter
import math
import os


from matplotlib import pyplot as plt
import numpy as np

from log import to_dict


def create_bar_chart():
    """Creates Bar Chart for distribution at end of week

    1. Parses data from past and current file
    2.Graphs data using matplotlib    
    """
    data = to_dict()
    applications = list(data.keys())
    last_week_data = date.today().isocalendar()[1] - 1
    past_file = os.path.dirname(os.getcwd()) + f'\logs\{last_week_data}.txt'
    past_data = to_dict(past_file)
    past_applications = list(past_data.keys())
    applications.extend(past_applications)
    applications = list(set(applications))
    x_indexes = np.arange(len(applications))
    current_times = []
    past_times = []

    for app in applications:
        if app in data.keys():
            current_times.append(math.floor(data[app]/60))

        else: current_times.append(0)

        if app in past_data.keys():
            past_times.append(math.floor(past_data[app]/60))

        else: past_times.append(0)

    width = 0.25
    plt.style.use('seaborn-darkgrid')
    plt.title('What Apps Did You Use This Week?')
    plt.xlabel('Applications')
    plt.ylabel('Time in Minutes')
    plt.bar(x_indexes, current_times, label='This Week', 
            width=width)
    plt.bar(x_indexes + width, past_times, 
            label='Last Week', width=width)
    plt.xticks(ticks=x_indexes, labels=applications)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
def create_pie_chart():
    pass


def get_top_five():
    path = os.getcwd()
    parent = os.path.dirname(path)
    path = parent + '\logs'
    directory = os.fsencode(path)
    all_time_stats = {}
    applications = []
    times = []

    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        all_time_stats[file] = to_dict(os.path.join(path, file_name))

    dicts = list(all_time_stats.values())
    dic = _merge_dicts(dicts)
    dic = Counter(dic)
    dic = dic.most_common(5)
    print(dic)

def _merge_dicts(dicts):
    base_dict = dicts.pop(0)

    for dic in dicts:
        for k,v in dic.items():
            base_dict[k] = base_dict.get(k, 0) + v

    return base_dict

get_top_five()



