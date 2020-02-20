import os
import getpass
from datetime import date


"""Setup process for user

1. Logs user into their email for weekly reports
2. Asks how often they would like to be checked
3. Creates folder for log files
"""
print('Please log into your email account to get started.\n')
print('Please enable less secure apps on your email account, \nor get an application password for Python to use this script.\n')
email = input('Email: ').strip()
password = getpass.getpass('Password: ')
frequency = input('How often would you like us to get your active application (in seconds)? ')

log_path = os.path.dirname(os.getcwd()) + '\logs' 
start_week = date.today().isocalendar()[1]
try:
    os.mkdir(log_path)
    with open(f'{log_path}\{start_week}.txt', 'w'): pass

except FileExistsError: pass


graph_path = os.path.dirname(os.getcwd()) + '\graphs'
try:
    os.mkdir(graph_path)

except FileExistsError: pass

with open(f'{os.getcwd()}\config.txt', 'w') as file: 
    file.write(f'email: {email}\n')
    file.write(f'frequency: {frequency}\n')

