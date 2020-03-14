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
    path = os.path.dirname(Path(sys.argv[0]))
    config = path + '\config.txt'
    configs = log.to_dict(config)
    sleep_time = configs['frequency']
    subbed = bool(configs['subscribe'])
    week_num = date.today().isocalendar()[1]
    logging.basicConfig(level=logging.INFO, filename=f'{path}\logs.txt',
                                filemode='w', format='%(asctime)s - %(message)s')

    if len(sys.argv) > 1:
            logging.info('sys.argv detected')
            if sys.argv[1] == '-s': setup.setup(os.getcwd())

            if sys.argv[1] == '--unsub': send.sub(os.getcwd(), False)

            if sys.argv[1] == '--sub': send.sub(os.getcwd(), True)

            return
    else:  
        try: 
            if datetime.datetime.today().weekday() == 6 and not graph.check_graphs():
                graph.create_bar_chart(path)
                graph.create_pie_chart(path)
                logging.info('Charts created')

                if subbed: 
                    send.send(path)
                    logging.info('Sent email')

        except FileNotFoundError:
                logging.critical('No previous file for graphing, ignore if just setup.')
        except:
                logging.critical('Error in graphing or sending.')

        try: 
            logging.info('STR started')
            if not setup.checks(path):
                logging.error('STR not setup')
                raise Exception('Please setup') 

            new_file = log.file_creation(path)
            if new_file: logging.info('New file created')

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
