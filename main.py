import sys
import ctypes
import time
import datetime
from datetime import date

from modules import graph, log, send, setup


def main_loop():
    sleep_time = log.to_dict('config.txt')['frequency']
    week_num = date.today().isocalendar()[1]

    if not setup.checks():
        warning_box = ctypes.windll.user32.MessageBoxW
        warning_box(None, 'Please setup screentime-reporter first.',
                    'STR WARNING', 0)

        raise Exception('Please setup') 

    if len(sys.argv) > 1:
        if sys.argv[1] == '-s':
            setup.setup()

    log.file_creation()

    if datetime.datetime.today().weekday() == 6 and not graph.check_graphs():
        graph.create_bar_chart()
        graph.create_pie_chart()

    while True:
        log.log()
        time.sleep(int(sleep_time))

main_loop()
