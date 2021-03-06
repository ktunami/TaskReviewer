# python3
# -*- coding: utf-8 -*-
# @Time : 2021/8/6 13:31 
# @Author : Kate
# @File : common_checks.py 

import datetime
import re


def get_checked_time(datetime_str):
    try:
        return datetime.datetime.strptime(datetime_str, '%H:%M')
    except ValueError:
        return None


def get_date(the_date):
    result = None
    if the_date != "":
        result = datetime.datetime.strptime(the_date, "%Y-%m-%d")
    return result


def get_num(the_str, default):
    try:
        return int(the_str)
    except:
        return default


def check_is_url(the_string):
    url_regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    result = False
    if re.match(url_regex, the_string):
        result = True
    return result