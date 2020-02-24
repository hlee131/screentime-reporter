from ctypes import wintypes
from datetime import date
import ctypes
import time
import os

import psutil


def _get_pid():
    """Gets process ID for foreground window"""
    user32 = ctypes.windll.user32
    hWnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
    return pid.value


def _get_active_processes():
    """Puts  the name of all processes and their PID's 
    in a dictionary
    """
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
    frequency = to_dict(os.getcwd() + '\config.txt')['frequency']
    active_application = get_active_application()
    latest_stats = to_dict()
    latest_stats = {k:int(v) for k,v in latest_stats.items()}
    log_file = os.getcwd() + f'\logs\{date.today().isocalendar()[1]}.txt'

    if active_application in latest_stats.keys():
        latest_stats[active_application] += int(frequency)
        with open(log_file, 'w') as file:
            for k, v in latest_stats.items():
                file.write(f'{k} : {v}\n')

    else:
        with open(log_file, 'a') as file:
            file.write(f'{active_application} : {frequency}\n')
            

def file_creation():
    """Checks day of week and directory to determine if new file is needed"""
    path = os.getcwd() + '\logs'
    supposed_file = f'\{date.today().isocalendar()[1]}.txt'
    supposed_file = path + supposed_file
    if not os.path.exists(supposed_file):
        with open(supposed_file, 'w'): pass


def to_dict(file=None):
    """Converts log or config txt to a Python dict"""
    if file == None:
        file = os.getcwd() + f'\logs\{date.today().isocalendar()[1]}.txt'
    
    else:
        pass

    with open(file, 'r') as file:
        lines = file.readlines()
        lines = [line.strip('\n') for line in lines]
        
        info = [line.split(':') for line in lines]
        keys = [element[0].strip() for element in info]
        values = [element[1].strip() for element in info]
        latest_stats = dict(zip(keys, values))

    return latest_stats
