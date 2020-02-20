from datetime import date
from collections import Counter
import math
import os

from matplotlib import pyplot as plt

from log import to_dict


def create_bar_chart():
    """Bar chart that compares two weeks' data

    1. Filters duplicate application
    2. Graphs app by app instead of providing an iterable
    """
    current_date = date.today().isocalendar()[1]
    current_data = to_dict()
    past_data = os.path.dirname(os.getcwd()) + f'\logs\{current_date - 1}.txt'
    past_data = to_dict(past_data)
    apps = list(current_data.keys())
    apps.extend(list(past_data.keys()))
    apps = _filter(apps)
    y_indexes = list(range(len(apps)))
    graphed = []
    current = 0
    current_color = ['#6e44ff']
    past_color = ['#ef7a85']

    plt.title('What Apps Did You Use This Week?')
    plt.ylabel('Applications')
    plt.xlabel('Time in Minutes')

    for app in list(current_data.keys()):
        graphed.append(app)
        cur = plt.barh(y_indexes[current] + 0.12, math.floor(current_data[app]/60),
                height=0.24, color=current_color)

        try: 
            past = plt.barh(y_indexes[current] - 0.12, math.floor(past_data[app]/60), 
                    height=0.24, color=past_color)

        except KeyError:
            pass
        current += 1

    for app in list(past_data.keys()):
        if app in graphed: pass
    
        else: 
            index = apps.index(app)
            past = plt.barh(y_indexes[index] - 0.12, math.floor(past_data[app]/60),
                    height=0.24, color=past_color)

    save_destination = os.path.dirname(os.getcwd()) + f'\graphs\{current_date}bar'
    plt.yticks(ticks=y_indexes, labels=apps)
    plt.tight_layout()
    plt.legend([cur, past], ['This Week', 'Last Week'])
    plt.savefig(save_destination)
    plt.show()
    

def create_pie_chart():
    """Creates pie chart for all time stats

    1. Data called using _get_top_five
    2. Graphed using plt.pie
    """
    current_date = date.today().isocalendar()[1]
    stats = _get_top_five()
    times = [t[1] for t in stats]
    labels = [f'{t[0]}\n({math.floor(t[1]/60)} Minutes)' for t in stats]

    save_destination = os.path.dirname(os.getcwd()) + f'\graphs\{current_date}pie'
    colors = ['#6e44ff', '#b892ff', '#ffc2e2', '#ff90b3', '#ef7a85']
    plt.pie(times, wedgeprops={'edgecolor' : 'black'},
            labels=labels, colors=colors)
    plt.title('Top 5 Most Used Applications (All Time)')
    plt.tight_layout()
    plt.savefig(save_destination)
    plt.show()


def _get_top_five():
    """Gets the top five applications of all time"""
    path = os.getcwd()
    parent = os.path.dirname(path)
    path = parent + '\logs'
    directory = os.fsencode(path)
    all_time_stats = {}

    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        all_time_stats[file] = to_dict(os.path.join(path, file_name))

    dicts = list(all_time_stats.values())
    dic = _merge_dicts(dicts)
    dic = Counter(dic)
    dic = dic.most_common(5)
    return dic


def _merge_dicts(dicts):
    """Merges dictionaries into a single dictionary
    
    Used for merging data from multiple log files,
    then using merged data for get_top_five.
    """
    base_dict = dicts.pop(0)

    for dic in dicts:
        for k,v in dic.items():
            base_dict[k] = base_dict.get(k, 0) + v

    return base_dict


def _filter(iterable):
    """Simple filter function because elements needed in specific order"""
    used = []
    r = []
    for i in iterable:
        if i in used: pass
        else: 
            used.append(i)
            r.append(i)
    return r
