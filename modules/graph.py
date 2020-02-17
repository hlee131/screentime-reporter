from matplotlib import pyplot as plt

from log import to_dict


def create_bar_chart():
    data = to_dict()
    applications = data.keys()
    times = data.values()

    plt.style.use('seaborn-darkgrid')
    plt.title('What Apps Did You Use This Week?')
    


def create_pie_chart():
    pass