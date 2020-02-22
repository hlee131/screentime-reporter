from ctypes import wintypes
from datetime import date
import ctypes
import time
import os 

import psutil

def _parse_config():
    """Parses config.txt for frequency information"""
    try:
        with open('../config.txt', 'r') as file:
            lines = file.readlines()
            _parse_config.freq = lines[1].split(':')[1].strip('\n').strip()
            
    except FileNotFoundError:
        raise FileNotFoundError(f'{os.getcwd()}Please setup with setup.py first! ')


def _get_pid():
    """Gets process ID for foreground window"""
    user32 = ctypes.windll.user32
    hWnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
    return pid.value


def _get_active_processes():
    """Puts  the name of all processes and their PID's in a dictionary"""
    _active_processes = [process.name().split('.')[0] for process in psutil.process_iter()]
    _active_pids = psutil.pids()
    active_processes = dict(zip(_active_pids, _active_processes))
    return active_processes


def get_active_application():
    """Returns active process

    Searches dictionary created in _get_active_processes for the PID found in _get_pid
    """
    pid = _get_pid()
    active_processes = _get_active_processes()
    return active_processes[pid]


def log():
    """Logs the current application using get_active_application

    Frequency is determined by user in setup.py. File Format:
    (Application name) : (time spent)
    (Application name) : (time spent)
    ...
    """
    active_application = get_active_application()
    latest_stats = to_dict()
    log_file = os.getcwd() + f'\logs\{date.today().isocalendar()[1]}.txt'

    if active_application in latest_stats.keys():
        latest_stats[active_application] += int(_parse_config.freq)
        with open(log_file, 'w') as file:
            for k, v in latest_stats.items():
                file.write(f'{k} : {v}\n')

    else:
        with open(log_file, 'a') as file:
            file.write(f'\n{active_application} : {_parse_config.freq}')
            

def file_creation():
    """Checks day of week and directory to determine if new file is needed"""
    supposed_file = f'{date.today().isocalendar()[1]}.txt'
    if supposed_file not in f'{os.getcwd()}\logs':
        with open(supposed_file, 'w'): pass


def to_dict(log_file=None):
    """Converts log txt to a Python dict"""
    if log_file == None:
        log_file = os.path.dirname(os.getcwd()) + f'\logs\{date.today().isocalendar()[1]}.txt'
    
    else:
        log_file = os.path.dirname(os.getcwd()) + f'\logs\{log_file}'

    with open(log_file, 'r') as file:
        stats = file.readlines()
        stats = [line.strip('\n') for line in stats]
        
        latest_stats = [stat.split(':') for stat in stats]
        app_names = [element[0].strip() for element in latest_stats]
        app_times = [int(element[1]) for element in latest_stats]
        latest_stats = dict(zip(app_names, app_times))

    return latest_stats

if __name__ == '__main__':
    time.sleep(5)
    _parse_config()
    log()
