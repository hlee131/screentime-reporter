import sys
import ctypes
import time
import datetime
import logging
import os 
from datetime import date
from pathlib import Path

from modules import graph, log, send, setup


def main_loop():
    try: 
        path = os.path.dirname(Path(sys.argv[0]))
        logging.basicConfig(level=logging.INFO, filename=f'{path}\logs.txt',
                            filemode='w', format='%(asctime)s - %(message)s')
        logging.info('STR started')
        
        if len(sys.argv) > 1:
            logging.info('sys.argv detected')
            if sys.argv[1] == '-s': setup.setup(path)

            if sys.argv[1] == '--unsub': send.sub(path, False)

            if sys.argv[1] == '--sub': send.sub(path, True)

            return

        config = path + '\config.txt'
        configs = log.to_dict(config)
        sleep_time = configs['frequency']
        subbed = bool(configs['subscribe'])
        week_num = date.today().isocalendar()[1]

        if not setup.checks(path):
            logging.error('STR not setup')
            raise Exception('Please setup') 

        new_file = log.file_creation(path)
        if new_file: logging.info('New file created')

        if datetime.datetime.today().weekday() == 6 and not graph.check_graphs():
            graph.create_bar_chart(path)
            graph.create_pie_chart(path)
            logging.info('Charts created')

            if subbed: 
                send.send(path)
                logging.info('Sent email')

        while True:
            log.log(path)
            logging.info('Logged')
            time.sleep(int(sleep_time))

    except Exception as e:
        warning_box = ctypes.windll.user32.MessageBoxW
        warning_box(None, str(e),
                    'STR WARNING', 0)
        print(e)
        logging.critical(e)
        

main_loop()
