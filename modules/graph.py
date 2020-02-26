from datetime import date
from collections import Counter
import math
import os

from matplotlib import pyplot as plt

from .log import to_dict


def create_bar_chart(wd):
    """Bar chart that compares two weeks' data

    1. Filters duplicate application
    2. Graphs app by app instead of providing an iterable
    """
    file = wd + f'\logs\{date.today().isocalendar()[1]}.txt'
    current_date = date.today().isocalendar()[1]
    current_data = to_dict(file)
    past_data = wd + f'\logs\{current_date - 1}.txt'
    past_data = to_dict(past_data)
    apps = list(current_data.keys())
    apps.extend(list(past_data.keys()))
    apps = _filter(apps)
    y_indexes = list(range(len(apps)))
    graphed = []
    current = 0
    current_color = ['#48e5c2']
    past_color = ['#5e5e5e']

    plt.title('What Apps Did You Use This Week?')
    plt.ylabel('Applications')
    plt.xlabel('Time in Minutes')

    for app in list(current_data.keys()):
        graphed.append(app)
        cur = plt.barh(y_indexes[current] + 0.12, math.floor(int(current_data[app])/60),
                height=0.24, color=current_color)

        try: 
            past = plt.barh(y_indexes[current] - 0.12, math.floor(int(past_data[app])/60), 
                    height=0.24, color=past_color)

        except KeyError:
            pass
        current += 1

    for app in list(past_data.keys()):
        if app in graphed: pass
    
        else: 
            index = apps.index(app)
            past = plt.barh(y_indexes[index] - 0.12, math.floor(int(past_data[app])/60),
                    height=0.24, color=past_color)

    save_destination = wd + f'\graphs\{current_date}bar'
    plt.yticks(ticks=y_indexes, labels=apps)
    plt.tight_layout()
    plt.legend([cur, past], ['This Week', 'Last Week'])
    plt.savefig(save_destination)
    plt.show()
    

def create_pie_chart(wd):
    """Creates pie chart for all time stats

    1. Data called using _get_top_five
    2. Graphed using plt.pie
    """
    current_date = date.today().isocalendar()[1]
    stats = _get_top_five(wd)
    times = [t[1] for t in stats]
    labels = [f'{t[0]}\n({math.floor(int(t[1])/60)} Minutes)' for t in stats]

    save_destination = wd + f'\graphs\{current_date}pie'
    colors = ['#333333', '#48e5c2', '#fcfaf9', '#f3d3bd', '#5e5e5e']
    plt.pie(times, wedgeprops={'edgecolor' : 'black'},
            labels=labels, colors=colors)
    plt.title('Top 5 Most Used Applications (All Time)')
    plt.tight_layout()
    plt.savefig(save_destination)
    plt.show()


def _get_top_five(wd):
    """Gets the top five applications of all time"""
    path = wd
    path = path + '\logs'
    directory = os.fsencode(path)
    all_time_stats = {}

    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        all_time_stats[file] = to_dict(os.path.join(path, file_name))

    dicts = list(all_time_stats.values())
    dic = _merge_dicts(dicts)
    dic = {k:int(v) for k,v in dic.items()}
    print(dic)
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
            print(type(v))
            base_dict[k] = int(base_dict.get(k, 0)) + int(v)

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


def check_graphs():
    """Checks whether graphs needed are present"""
    week_num = date.today().isocalendar()[1]
    pie_chart = os.getcwd() + f'\graphs\{week_num}pie.png'
    bar_chart = os.getcwd() + f'\graphs\{week_num}bar.png'

    if os.path.exists(bar_chart) and os.path.exists(pie_chart):
        return True

    else: return False