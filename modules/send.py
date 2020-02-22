### adding new log file in log folder
import os
import smtplib
import imghdr
import math
from email.message import EmailMessage
from email.utils import make_msgid
from datetime import date

from log import to_dict


def send():
    # EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    # EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    EMAIL_ADDRESS = 'scriptingtesting197@gmail.com'
    EMAIL_PASSWORD = 'JHSL1415'
    with open('template.txt', 'r') as file:
        template = file.read()

    data = _get_values()
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


def _get_values():
    pie_id = make_msgid()[1:-1]
    bar_id = make_msgid()[1:-1]
    week = date.today().isocalendar()[1]
    week_stats = to_dict()
    this_week = round(sum([int(num)/3600 for num in week_stats.values()]), 2)
    per_day = round(this_week/7, 2)
    path_bar = os.path.dirname(os.getcwd()) + f'\graphs\{week}bar.png'
    total_time = 0

    path = os.getcwd()
    parent = os.path.dirname(path)
    path = parent + '\logs'
    directory = os.fsencode(path)

    for file in os.listdir(directory):
        stats = to_dict(os.fsdecode(file))
        total_time += sum(int(num) for num in stats.values())

    total_time /= 3600
    time_per_week = total_time/len(os.listdir(path))
    path_pie = os.path.dirname(os.getcwd()) + f'\graphs\{week}pie.png'

    return this_week, per_day, bar_id, total_time, time_per_week, pie_id, path_bar, path_pie

send()