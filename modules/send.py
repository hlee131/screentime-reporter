### adding new log file in log folder
import os
import smtplib
import imghdr
import math
from email.message import EmailMessage
from email.utils import make_msgid
from datetime import date

from .log import to_dict


def send(wd):
    """Sends message to email using smtplib"""
    config_path = f'{wd}/config.txt'
    config = to_dict(config_path)
    EMAIL_ADDRESS = config['email']
    EMAIL_PASSWORD = config['password']
    path = wd + r'\modules\template.txt'
    with open(path, 'r') as file:
        template = file.read()

    data = _get_values(wd)
    msg = EmailMessage()
    msg['Subject'] = 'Your Weekly Report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(f"""You are recieving this because you have disabled HTML emails.\n\n
                        You spent... {data[0]} hours this week, {data[1]} hours a day.\n
                        In total, you spent... {data[3]} hours, {data[4]} hours a week""")
    
    msg.add_alternative(template % data[:6], subtype='html')

    with open(data[6], 'rb') as image:
        bar_data = image.read()
        bar_type = imghdr.what(image.name)
        bar_name = image.name

    with open(data[7], 'rb') as image:
        pie_data = image.read()
        pie_type = imghdr.what(image.name)
        pie_name = image.name

    msg.add_attachment(bar_data, maintype='image', 
                        subtype=bar_type, filename=bar_name, cid=f'<{data[2]}>')
    msg.add_attachment(pie_data, maintype='image', 
                        subtype=pie_type, filename=pie_name, cid=f'<{data[5]}>')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def _get_values(wd):
    """Returns a tuple to insert into the HTML template"""
    pie_id = make_msgid()[1:-1]
    bar_id = make_msgid()[1:-1]
    week = date.today().isocalendar()[1]
    file = wd + f'\logs\{date.today().isocalendar()[1]}.txt'
    week_stats = to_dict(file)
    this_week = round(sum([int(num)/3600 for num in week_stats.values()]), 2)
    per_day = round(this_week/7, 2)
    path_bar = wd + f'\graphs\{week}bar.png'
    total_time = 0

    path = wd + '\logs'
    directory = os.fsencode(path)

    for file in os.listdir(directory):
        file_path = path + f'\{os.fsdecode(file)}'
        stats = to_dict(file_path)
        total_time += sum(int(num) for num in stats.values())

    total_time /= 3600
    time_per_week = total_time/len(os.listdir(path))
    path_pie = wd + f'\graphs\{week}pie.png'

    return this_week, per_day, bar_id, total_time, time_per_week, pie_id, path_bar, path_pie


def sub(wd, subscribed):
    """Unsubcribes from the weekly email by altering config.txt"""
    config_path = wd + '\config.txt'
    config = to_dict(config_path)
    config['subscribe'] = True if subscribed else False
    with open(config_path, 'w') as file:
        for k, v in config.items():
            file.write(f'{k} : {v}\n')
