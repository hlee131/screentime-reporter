import os
import getpass
import sys
from datetime import date

def setup(wd):
    """Setup process for user

    1. Logs user into their email for weekly reports
    2. Asks how often they would like to be checked
    3. Creates folder for log files
    4. Adds main.py to startup folder
    """
    # Prompts user for information
    print('Please log into your email account to get started.\n')
    print('Please enable less secure apps on your email account, \nor get an application password for Python to use this script.\n')
    EMAIL = input('Email: ').strip()
    PASSWORD = getpass.getpass('Password: ')
    FREQUENCY = input('How often would you like us to get your active application (in seconds)? ')

    # Creates log files and folders
    log_path = wd + '\logs' 
    start_week = date.today().isocalendar()[1]
    try:
        os.mkdir(log_path)
        with open(f'{log_path}\{start_week}.txt', 'w'): pass

    except FileExistsError: pass

    # Creates graphs folders
    graph_path = wd + '\graphs'
    try:
        os.mkdir(graph_path)

    except FileExistsError: pass

    # Compiles info into a config file
    with open(f'{wd}\config.txt', 'w') as file: 
        file.write(f'email : {EMAIL}\n')
        file.write(f'password : {PASSWORD}\n')
        file.write(f'frequency : {FREQUENCY}\n')
        file.write('subscribe : True')
        file.write(f'CWD : {wd}')


def checks(path):
    """Runs all the necessary checks during every startup"""
    log_path = path + '\logs'
    graph_path = path + '\graphs'
    config_path = f'{path}\config.txt'

    if os.path.exists(log_path) and os.path.exists(graph_path) and os.path.exists(config_path):
        return True

    else: return False
